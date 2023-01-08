"""RecycleApp sensor."""
from homeassistant.components.sensor import SensorDeviceClass
from typing import Any, Dict, List
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from datetime import datetime, timedelta
import logging
from custom_components.recycle_app.api import FostPlusApi
from .const import COLLECTION_TYPES, DOMAIN
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.event import async_track_time_change

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry, async_add_entities):
    config: Dict = hass.data[DOMAIN][config_entry.entry_id]
    # Update our config to include new repos and remove those that have been removed.
    # if config_entry.options:
    #     config.update(config_entry.options)
    api = FostPlusApi()
    _LOGGER.debug(f'Adding fractions')

    zip_code_id: str = config["zipCodeId"]
    street_id: str = config["streetId"]
    house_number: int = config["houseNumber"]
    fractions: List[str] = config["fractions"]
    language: str = config.get("language", "fr")

    async def async_update_collections():
        _LOGGER.debug("Update collections")
        """Fetch data"""
        return await hass.async_add_executor_job(api.get_collections, zip_code_id, street_id, house_number)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name='RecycleAppGetCollections',
        update_method=async_update_collections
    )
    
    lastRefresh = datetime.utcnow()

    @callback
    async def async_refresh(now):
        nonlocal lastRefresh
        if (datetime.utcnow() - lastRefresh).total_seconds() > 120:
            lastRefresh=datetime.utcnow()
            _LOGGER.debug(f"async_refresh {unique_id}")
            await coordinator.async_refresh()

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    # Refresh every day at midnight
    async_track_time_change(hass, async_refresh, hour=0, minute=0, second=0);

    unique_id = f"RecycleApp-{zip_code_id}-{street_id}-{house_number}"
    device_info = DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, unique_id)},
        name=config.get("name", "Collecte des poubelles"),
        manufacturer='Fost Plus',
        model='Recycle!'
    )

    async_add_entities([RecycleAppEntity(
        coordinator, f"{unique_id}-{f}", f, language, device_info) for f in fractions])


class RecycleAppEntity(CoordinatorEntity, Entity):
    """Base class for all RecycleApp entities."""

    def __init__(
            self,
            coordinator: DataUpdateCoordinator,
            unique_id: str,
            fraction: str,
            language: str = None,
            device_info: Dict[str, Any] = None
    ):
        """Initialize the entity"""
        super().__init__(coordinator)
        self._unique_id = unique_id
        self._fraction = fraction
        self._language = language
        self._device_info = device_info
        self._attr_extra_state_attributes = {"days": None}

    @property
    def device_class(self):
        return SensorDeviceClass.DATE

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def name(self):
        return COLLECTION_TYPES[self._fraction][self._language]

    @property
    def icon(self) -> str:
        return "mdi:trash-can"

    @property
    def entity_picture(self):
        return COLLECTION_TYPES[self._fraction].get("image", None)

    @property
    def state(self):
        return self.coordinator.data[self._fraction] if self._fraction in self.coordinator.data else None

    @property
    def available(self) -> bool:
        return self._fraction in self.coordinator.data

    @property
    def device_info(self) -> dict:
        return self._device_info

    @callback
    def async_write_ha_state(self) -> None:
        if (self.state):
            delta: timedelta = self.state - datetime.now().date()
            self._attr_extra_state_attributes["days"] = delta.days
        else:
            self._attr_extra_state_attributes["days"] = None

        super().async_write_ha_state()
