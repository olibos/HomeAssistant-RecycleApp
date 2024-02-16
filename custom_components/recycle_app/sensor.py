"""RecycleApp sensor."""
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

from .api import FostPlusApi
from .const import DEFAULT_DATE_FORMAT, DOMAIN, get_icon
from .info import AppInfo
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
    entities = [
        RecycleAppEntity(
            app_info["collect_coordinator"],
            f"{unique_id}-{fraction}",
            fraction,
            color,
            name,
            app_info["collect_device"],
            date_format,
        )
        for (fraction, (color, name)) in fractions.items()
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
                name=park_info["name"],
                manufacturer="Fost Plus",
                model="Recycle!",
            )

            entities += [
                OpeningHoursEntity(
                    app_info["recycling_park_coordinator"],
                    f"{unique_id}-{park_id}-{day_of_week}",
                    park_id,
                    day_of_week,
                    device_info,
                )
                for day_of_week in DAYS_OF_WEEK
            ]

    async_add_entities(entities)


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
        device_info: dict[str, Any] = None,
        date_format=DEFAULT_DATE_FORMAT,
    ):
        """Initialize the entity."""
        super().__init__(coordinator)
        is_timestamp = date_format == "TIMESTAMP"
        self.entity_description = SensorEntityDescription(
            key="RecycleAppEntity",
            name=name,
            icon="mdi:trash-can",
            device_class=SensorDeviceClass.TIMESTAMP
            if is_timestamp
            else SensorDeviceClass.DATE,
        )
        self._attr_unique_id = unique_id
        self._fraction = fraction
        self._attr_entity_picture = get_icon(fraction, color)
        self._attr_device_info = device_info
        self._attr_extra_state_attributes = {"days": None}
        self._date_format = date_format if not is_timestamp else DEFAULT_DATE_FORMAT

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
