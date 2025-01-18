"""RecycleApp sensor."""

import logging
from datetime import date, datetime, timedelta
from typing import Any, final

from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import slugify

from .api import FostPlusApi
from .const import DEFAULT_DATE_FORMAT, DOMAIN, MANUFACTURER, WEBSITE, get_icon
from .helpers import get_localized_date
from .info import AppInfo
from .opening_hours_entity import DAYS_OF_WEEK, OpeningHoursEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    app_info: AppInfo = hass.data[DOMAIN][config_entry.entry_id]
    fractions: dict[str, tuple[str, str]] = config_entry.options.get("fractions")
    unique_id = app_info["unique_id"]
    date_format: str = config_entry.options.get("format", DEFAULT_DATE_FORMAT)
    language: str = config_entry.options.get("language", "fr")
    entity_id_prefix: str = config_entry.options.get("entity_id_prefix", "")

    entities = [
        RecycleAppEntity(
            app_info["collect_coordinator"],
            f"{unique_id}-{fraction}",
            fraction,
            color,
            name,
            app_info["collect_device"],
            date_format,
            entity_id_prefix,
            language,
        )
        for (fraction, (color, name)) in fractions.items()
    ]

    entities += [
        RecycleAppUpcomingSensor(
            app_info["collect_coordinator"],
            f"{unique_id}-upcoming",
            fractions,
            app_info["collect_device"],
            date_format,
            entity_id_prefix,
            language,
        ),
        RecycleAppTodaySensor(
            app_info["collect_coordinator"],
            f"{unique_id}-today",
            fractions,
            app_info["collect_device"],
            date_format,
            entity_id_prefix,
        ),
        RecycleAppTomorrowSensor(
            app_info["collect_coordinator"],
            f"{unique_id}-tomorrow",
            fractions,
            app_info["collect_device"],
            date_format,
            entity_id_prefix,
        ),
    ]

    recycling_park_zip_code: str = config_entry.options.get(
        "recyclingParkZipCode", None
    )
    parks: list[str] = config_entry.options.get("parks", [])

    if len(parks) > 0 and recycling_park_zip_code:
        api = FostPlusApi()
        parks_found = await hass.async_add_executor_job(
            api.get_recycling_parks, recycling_park_zip_code, language
        )
        for park_id, park_info in parks_found.items():
            if park_id not in parks:
                continue
            device_info = DeviceInfo(
                entry_type=DeviceEntryType.SERVICE,
                identifiers={(DOMAIN, f"{unique_id}-{park_id}")},
                name=park_info["name"].capitalize(),
                manufacturer=MANUFACTURER,
                model="Recycling park",
                configuration_url=WEBSITE,
            )

            entities += [
                OpeningHoursEntity(
                    app_info["recycling_park_coordinator"],
                    f"{unique_id}-{park_id}-{day_of_week}",
                    park_id,
                    day_of_week,
                    device_info,
                    entity_id_prefix,
                )
                for day_of_week in DAYS_OF_WEEK
            ]

    async_add_entities(entities)
    # Call async_update on the sensor immediately after setup
    for sensor in entities:
        await sensor.async_update()


class RecycleAppEntity(
    CoordinatorEntity[DataUpdateCoordinator[dict[str, list[date]]]], SensorEntity
):
    """Base class for all RecycleApp entities."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, list[date]]],
        unique_id: str,
        fraction: str,
        color: str,
        name: str,
        device_info: dict[str, Any] | None = None,
        date_format=DEFAULT_DATE_FORMAT,
        entity_id_prefix: str = "",  # Default to an empty string
        language: str = None,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        is_timestamp = date_format == "TIMESTAMP"
        self.entity_description = SensorEntityDescription(
            key="RecycleAppEntity",
            name=name,
            icon="mdi:trash-can",
            translation_key=name.lower(),
            device_class=(
                SensorDeviceClass.TIMESTAMP if is_timestamp else SensorDeviceClass.DATE
            ),
        )
        self._attr_unique_id = unique_id
        self._language = language
        self._fraction = fraction
        self._attr_entity_picture = get_icon(fraction, color)
        self._attr_device_info = device_info
        self._attr_extra_state_attributes = {"days": None}
        self._date_format = date_format if not is_timestamp else DEFAULT_DATE_FORMAT
        self._formatted_date = None

        # Handle entity_id prefix using slugify
        prefix = (
            slugify(entity_id_prefix) if entity_id_prefix else ""
        )  # Slugify the prefix
        base_name = slugify(name)  # Slugify the base name
        self.entity_id = (
            f"sensor.{prefix}_{base_name}" if prefix else f"sensor.{base_name}"
        )

    async def async_update(self):
        """Update the state with a fully localized date."""
        value = self.native_value
        _LOGGER.debug(f"Native value for {self.entity_id}: {value}")  # Log the value
        if value is None:
            _LOGGER.debug(f"No value for {self.entity_id}, skipping update")
            return None

        # Retrieve and localize the date
        localized_date = await get_localized_date(
            self.hass, value, self._date_format, language=self._language, domain=DOMAIN
        )

        _LOGGER.debug(
            f"Localized Date for {self.entity_id}: {localized_date}"
        )  # Log the localized date

        # Set the localized state
        self._formatted_date = localized_date

        # Inform Home Assistant of the state change (no 'await' here)
        _LOGGER.debug(
            f"State for {self.entity_id} set to: {self._formatted_date}"
        )  # Log the new state
        self.async_write_ha_state()  # Inform Home Assistant (no await)

    @property
    @final
    def state(self):
        """Return the entity state."""
        if self.native_value is None:
            return None
        return self._formatted_date

    @property
    def native_value(self) -> date | None:
        if not self.coordinator.data or self._fraction not in self.coordinator.data:
            _LOGGER.debug(f"No data for fraction {self._fraction} in {self.entity_id}")
            return None
        return self.coordinator.data[self._fraction][0]

    @property
    def available(self) -> bool:
        return (
            self.coordinator.data is not None
            and self._fraction in self.coordinator.data
        )

    @callback
    def async_write_ha_state(self) -> None:
        value = self.native_value
        if value:
            delta: timedelta = value - datetime.now().date()
            self._attr_extra_state_attributes["days"] = delta.days
        else:
            self._attr_extra_state_attributes["days"] = None

        super().async_write_ha_state()


class RecycleAppDateSensor(RecycleAppEntity):
    """Base class for sensors that are date-based (Today, Tomorrow, Upcoming)."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, list[date]]],
        unique_id: str,
        fraction_key: str,
        fractions: dict[str, tuple[str, str]],
        device_info: dict[str, Any] | None = None,
        date_format=DEFAULT_DATE_FORMAT,
        entity_id_prefix: str = "",
        language: str = None,
    ) -> None:
        """Initialize the DateSensor."""
        super().__init__(
            coordinator,
            unique_id,
            fraction_key,
            "transparent",
            fraction_key.capitalize(),
            device_info,
            date_format,
            entity_id_prefix,
            language,
        )
        self._fractions = fractions
        self.fraction_key = fraction_key

    @property
    def native_value(self) -> date | None:
        """Return the specific date for today, tomorrow, or upcoming."""
        if self.fraction_key == "collection_today":
            return datetime.now().date()
        elif self.fraction_key == "collection_tomorrow":
            return datetime.now().date() + timedelta(days=1)
        elif self.fraction_key == "collection_upcoming":
            return self.get_upcoming_date()
        return None

    def get_upcoming_date(self):
        """Helper method to get the upcoming date for the upcoming sensor."""
        if self.coordinator.data:
            upcoming_dates = sorted(
                [
                    d
                    for dates in self.coordinator.data.values()
                    for d in dates
                    if d > datetime.now().date()
                ]
            )
            return upcoming_dates[0] if upcoming_dates else None
        return None

    @property
    def state(self) -> str | None:
        """Return the state as 'fractions' without the date prefixed."""
        date_value = self.native_value
        if not date_value:
            return None

        # Collect fractions for the upcoming date
        fractions_on_date = [
            name
            for fraction_id, (color, name) in self._fractions.items()
            if fraction_id in self.coordinator.data
            and date_value in self.coordinator.data[fraction_id]
        ]

        if not fractions_on_date:
            return None

        # Set extra state attributes
        self._attr_extra_state_attributes["date"] = self._formatted_date
        self._attr_extra_state_attributes["fractions"] = fractions_on_date

        # If the fraction_key is 'collection_upcoming', we prefix with the date
        if self.fraction_key == "collection_upcoming":
            return f"{self._formatted_date}: {', '.join(fractions_on_date)}"

        # For other fraction keys, just return the fractions without the date prefix
        return ", ".join(fractions_on_date)

    @property
    def available(self) -> bool:
        """Return whether the sensor is available or not."""
        # Check if the fraction_key is valid and data exists for the corresponding fraction
        if self.fraction_key == "collection_today":
            return any(
                dates and dates[0] == datetime.now().date()
                for dates in self.coordinator.data.values()
            )
        elif self.fraction_key == "collection_tomorrow":
            return any(
                dates and dates[0] == datetime.now().date() + timedelta(days=1)
                for dates in self.coordinator.data.values()
            )
        elif self.fraction_key == "collection_upcoming":
            return any(
                dates and any(d > datetime.now().date() for d in dates)
                for dates in self.coordinator.data.values()
            )
        return False


class RecycleAppUpcomingSensor(RecycleAppDateSensor):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, list[date]]],
        unique_id: str,
        fractions: dict[str, tuple[str, str]],
        device_info: dict[str, Any] | None = None,
        date_format=DEFAULT_DATE_FORMAT,
        entity_id_prefix: str = "",
        language: str = None,
    ) -> None:
        """Initialize the Upcoming Sensor."""
        super().__init__(
            coordinator,
            unique_id,
            "collection_upcoming",
            fractions,
            device_info,
            date_format,
            entity_id_prefix,
            language,
        )
        self._attr_icon = "mdi:truck-fast"


class RecycleAppTodaySensor(RecycleAppDateSensor):
    """Sensor for fractions to be picked up today."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, list[date]]],
        unique_id: str,
        fractions: dict[str, tuple[str, str]],
        device_info: dict[str, Any] | None = None,
        date_format=DEFAULT_DATE_FORMAT,
        entity_id_prefix: str = "",
    ) -> None:
        """Initialize the Today Sensor."""
        super().__init__(
            coordinator,
            unique_id,
            "collection_today",
            fractions,
            device_info,
            date_format,
            entity_id_prefix,
        )
        self._attr_icon = "mdi:truck-check"


class RecycleAppTomorrowSensor(RecycleAppDateSensor):
    """Sensor for fractions to be picked up tomorrow."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, list[date]]],
        unique_id: str,
        fractions: dict[str, tuple[str, str]],
        device_info: dict[str, Any] | None = None,
        date_format=DEFAULT_DATE_FORMAT,
        entity_id_prefix: str = "",
    ) -> None:
        """Initialize the Tomorrow Sensor."""
        super().__init__(
            coordinator,
            unique_id,
            "collection_tomorrow",
            fractions,
            device_info,
            date_format,
            entity_id_prefix,
        )
        self._attr_icon = "mdi:truck-delivery"
