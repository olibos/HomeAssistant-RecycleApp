from datetime import date, datetime, timedelta
import logging

from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import translation
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

_LOGGER = logging.getLogger(__name__)


# file1 = hass.config.path(
#         "custom_components", "test", "translations", "switch.en.json"
#     )
#     file2 = hass.config.path(
#         "custom_components", "test", "translations", "invalid.json"
#     )
#     assert translation.load_translations_files(
class OpeningHoursEntity(CoordinatorEntity, SensorEntity):
    """Opening hours entity for Recycling Parks."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        unique_id: str,
        park_id: str,
        day_of_week: str,
        device_info: DeviceInfo,
    ):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = SensorEntityDescription(
            key="OpeningHoursEntity",
            has_entity_name=True,
            translation_key=f"opening_hours_{day_of_week.lower()}",
            icon="mdi:clock-outline",
        )
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info
        self._day_of_week = day_of_week
        self._park_id = park_id

    @property
    def native_value(self) -> str | None:
        _LOGGER.info(f"_name_translation_key={self._name_translation_key}")
        return "TODO: Opening hours"
