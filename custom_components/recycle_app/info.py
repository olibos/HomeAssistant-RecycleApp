"""Integration information."""
from datetime import date
from typing import TypedDict

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class AppInfo(TypedDict, total=True):
    """Integration information for RecycleApp entities."""

    collect_device: DeviceInfo
    collect_coordinator: DataUpdateCoordinator[dict[str, list[date]]]
    recycling_park_coordinator: DataUpdateCoordinator[dict[str, dict]]
    unique_id: str
