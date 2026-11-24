"""RecycleApp sensor."""

from datetime import date, datetime, timedelta
from typing import Any, final

from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
import homeassistant.helpers.entity_registry as er
from homeassistant.const import Platform
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util, slugify

from .api import client as api
from .const import DEFAULT_DATE_FORMAT, DOMAIN, get_icon, MANUFACTURER, WEBSITE
from .info import AppInfo
from .naming import get_fraction_name
from .opening_hours_entity import DAYS_OF_WEEK, OpeningHoursEntity


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
        )
        for (fraction, (color, name)) in fractions.items()
    ]

    recycling_park_zip_code: str = config_entry.options.get(
        "recyclingParkZipCode", None
    )
    parks: list[str] = config_entry.options.get("parks", [])

    if len(parks) > 0 and recycling_park_zip_code:
        parks_found = await hass.async_add_executor_job(
            api.get_recycling_parks, recycling_park_zip_code, language
        )
        for park_id, park_info in parks_found.items():
            if park_id not in parks:
                continue
            device_info = DeviceInfo(
                entry_type=DeviceEntryType.SERVICE,
                identifiers={(DOMAIN, f"{unique_id}-{park_id}")},
                name=park_info["name"],
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

    entities += [
        RecycleAppCollectionDaySensor(
            app_info["collect_coordinator"],
            unique_id,
            day_offset,
            fractions,
            app_info["collect_device"],
            entity_id_prefix,
        )
        for day_offset in (0, 1)
    ]

    async_add_entities(entities)


class RecycleAppCollectionDaySensor(
    CoordinatorEntity[DataUpdateCoordinator[dict[str, list[date]]]], SensorEntity
):
    """Sensor that lists all fractions collected on a given day offset."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, list[date]]],
        base_unique_id: str,
        day_offset: int,
        fractions: dict[str, tuple[str, str]],
        device_info: dict[str, Any] | None = None,
        entity_id_prefix: str = "",
    ) -> None:
        super().__init__(coordinator)
        label = "today" if day_offset == 0 else "tomorrow"
        self._day_offset = day_offset
        self._fractions = fractions
        # Fraction sensors are registered as f"{base_unique_id}-{fraction}".
        self._fraction_unique_ids = {
            f"{base_unique_id}-{fraction}": fraction for fraction in fractions
        }
        self._attr_unique_id = f"{base_unique_id}-{label}"
        self._attr_device_info = device_info
        self.entity_description = SensorEntityDescription(
            key=f"collection_{label}",
            translation_key=f"collection_{label}",
            has_entity_name=True,
            icon="mdi:trash-can",
        )
        prefix = slugify(entity_id_prefix) if entity_id_prefix else ""
        self.entity_id = (
            f"sensor.{prefix}_collection_{label}" if prefix else f"sensor.collection_{label}"
        )

    async def async_added_to_hass(self) -> None:
        """Re-evaluate the state at local midnight, from cached data only."""
        await super().async_added_to_hass()

        @callback
        def _async_midnight(_now: datetime) -> None:
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_time_change(
                self.hass, _async_midnight, hour=0, minute=0, second=0
            )
        )

        # Renaming or disabling a fraction sensor changes no state, so nothing
        # else would refresh the list here until the next coordinator update.
        entity_registry = er.async_get(self.hass)

        @callback
        def _is_fraction_registry_change(event_data: er.EventEntityRegistryUpdatedData) -> bool:
            if event_data["action"] != "update" or not (
                event_data.get("changes", {}).keys() & {"name", "disabled_by"}
            ):
                return False
            entry = entity_registry.async_get(event_data["entity_id"])
            return (
                entry is not None
                and entry.platform == DOMAIN
                and entry.unique_id in self._fraction_unique_ids
            )

        @callback
        def _async_fraction_changed(_event: Event) -> None:
            self.async_write_ha_state()

        self.async_on_remove(
            self.hass.bus.async_listen(
                er.EVENT_ENTITY_REGISTRY_UPDATED,
                _async_fraction_changed,
                event_filter=_is_fraction_registry_change,
            )
        )

    @property
    def available(self) -> bool:
        """Stay available on cached data even if the last refresh failed."""
        return self.coordinator.data is not None

    @property
    def native_value(self) -> str:
        if self.coordinator.data is None:
            return ""
        target = dt_util.now().date() + timedelta(days=self._day_offset)
        entity_registry = er.async_get(self.hass)
        names: list[str] = []
        for fraction_unique_id, fraction in self._fraction_unique_ids.items():
            if target not in self.coordinator.data.get(fraction, ()):
                continue
            entity_id = entity_registry.async_get_entity_id(
                Platform.SENSOR, DOMAIN, fraction_unique_id
            )
            # Skip fractions whose sensor the user disabled. A missing registry
            # entry (not registered yet at startup) falls back to the config name.
            if entity_id and (entry := entity_registry.async_get(entity_id)):
                if entry.disabled:
                    continue
            names.append(
                get_fraction_name(entity_registry, entity_id, self._fractions, fraction)
            )
        return ", ".join(names)

    @property
    def icon(self) -> str:
        return "mdi:trash-can" if self.native_value else "mdi:delete-empty"


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
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        is_timestamp = date_format == "TIMESTAMP"
        self.entity_description = SensorEntityDescription(
            key="RecycleAppEntity",
            name=name,
            icon="mdi:trash-can",
            device_class=(
                SensorDeviceClass.TIMESTAMP if is_timestamp else SensorDeviceClass.DATE
            ),
        )
        self._attr_unique_id = unique_id
        self._fraction = fraction
        self._attr_entity_picture = get_icon(fraction, color)
        self._attr_device_info = device_info
        self._attr_extra_state_attributes = {"days": None}
        self._date_format = date_format if not is_timestamp else DEFAULT_DATE_FORMAT

        # Handle entity_id prefix using slugify
        prefix = (
            slugify(entity_id_prefix) if entity_id_prefix else ""
        )  # Slugify the prefix
        base_name = slugify(name)  # Slugify the base name
        self.entity_id = (
            f"sensor.{prefix}_{base_name}" if prefix else f"sensor.{base_name}"
        )

    @property
    @final
    def state(self) -> str | None:
        value = self.native_value
        if value is None:
            return None

        return value.strftime(self._date_format)

    @property
    def native_value(self) -> date | None:
        return (
            self.coordinator.data[self._fraction][0]
            if self.coordinator.data is not None
            and self._fraction in self.coordinator.data
            else None
        )

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
