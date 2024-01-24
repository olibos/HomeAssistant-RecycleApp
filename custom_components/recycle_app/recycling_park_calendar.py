"""RecycleApp Calendar."""
from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util


class RecyclingParkCalendarEntity(CoordinatorEntity, CalendarEntity):
    """Representation of a Collect Calendar element."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        unique_id: str,
        park_id: str,
        device_info: DeviceInfo,
    ) -> None:
        super().__init__(coordinator)
        self._park_id = park_id
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info

    def __get_events(self, start_date: datetime, end_date: datetime):
        if not self.coordinator.last_update_success or self.coordinator.data is None:
            return

        exceptions = {
            dt_util.as_local(dt_util.parse_datetime(entry["date"])).date()
            for entry in self.coordinator.data[self._park_id].get("exceptions", [])
        }

        current_date = start_date
        one_day = timedelta(days=1)
        name = (
            self.device_entry.name_by_user or self.device_entry.name
            if self.device_entry
            else self.device_info["name"]
        )

        while current_date <= end_date:
            if dt_util.as_local(current_date).date() in exceptions:
                current_date += one_day
                continue

            day_of_week = (current_date.weekday() + 1) % 7
            yield from (
                CalendarEvent(
                    start=dt_util.as_local(
                        datetime.combine(
                            current_date,
                            dt_util.parse_time(opening_hour["from"]),
                        )
                    ),
                    end=dt_util.as_local(
                        datetime.combine(
                            current_date,
                            dt_util.parse_time(opening_hour["until"]),
                        )
                    ),
                    summary=name,
                )
                for period in self.coordinator.data[self._park_id]["periods"]
                if current_date >= dt_util.parse_datetime(period["from"])
                and current_date <= dt_util.parse_datetime(period["until"])
                for opening_day in period["openingDays"]
                if opening_day["day"] == day_of_week
                for opening_hour in opening_day["openingHours"]
            )

            current_date += one_day

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        now = dt_util.now()
        return next(
            (
                event
                for event in self.__get_events(now, now + timedelta(days=10))
                if now < event.end
            ),
            None,
        )

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        return list(self.__get_events(start_date, end_date))
