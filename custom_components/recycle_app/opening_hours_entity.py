from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


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
        self.__update_native_value()

    def __update_native_value(self) -> None:
        if (
            not self.coordinator.last_update_success
            or self.coordinator.data is None
            or self._park_id not in self.coordinator.data
        ):
            return

        now = dt_util.utcnow()
        day_of_week = (DAYS_OF_WEEK.index(self._day_of_week) + 1) % 7
        periods = []
        for period in self.coordinator.data[self._park_id].get("periods", []):
            if now < dt_util.parse_datetime(
                period["from"]
            ) or now > dt_util.parse_datetime(period["until"]):
                continue

            for opening_day in period["openingDays"]:
                if opening_day["day"] != day_of_week:
                    continue
                periods = [
                    f"{openingHour['from']} - {openingHour['until']}"
                    for openingHour in opening_day["openingHours"]
                ]
                break

        self._attr_native_value = "\n".join(periods) if len(periods) > 0 else None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.native_value is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.__update_native_value()
        super()._handle_coordinator_update()
