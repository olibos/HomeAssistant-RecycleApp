"""RecycleApp sensor."""
from datetime import date, datetime, timedelta
import logging
from typing import Any, final

from homeassistant import config_entries
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DEFAULT_DATE_FORMAT, DOMAIN, get_icon
from .info import AppInfo

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: config_entries.ConfigEntry, async_add_entities
):
    app_info: AppInfo = hass.data[DOMAIN][config_entry.entry_id]
    fractions: dict[str, tuple[str, str]] = config_entry.options.get("fractions")
    unique_id = app_info["unique_id"]
    date_format: str = config_entry.options.get("format", DEFAULT_DATE_FORMAT)

    if isinstance(fractions, dict):
        async_add_entities(
            [
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
        )
    else:
        _LOGGER.error(
            "Your fractions are in the v1 format... Please delete this address and restart"
        )


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
        self._unique_id = unique_id
        self._fraction = fraction
        self._image = get_icon(fraction, color)
        self._name = name
        self._device_info = device_info
        self._attr_extra_state_attributes = {"days": None}
        self._date_format = date_format

    @property
    def device_class(self):
        return SensorDeviceClass.DATE

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def name(self):
        return self._name

    @property
    def icon(self) -> str:
        return "mdi:trash-can"

    @property
    def entity_picture(self):
        return self._image

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
            if self._fraction in self.coordinator.data
            else None
        )

    @property
    def available(self) -> bool:
        return self._fraction in self.coordinator.data

    @property
    def device_info(self) -> dict:
        return self._device_info

    @callback
    def async_write_ha_state(self) -> None:
        value = self.native_value
        if value:
            delta: timedelta = value - datetime.now().date()
            self._attr_extra_state_attributes["days"] = delta.days
        else:
            self._attr_extra_state_attributes["days"] = None

        super().async_write_ha_state()
