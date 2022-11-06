"""RecycleApp sensor."""
from homeassistant.const import DEVICE_CLASS_DATE
from typing import Any, Dict, List
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from datetime import timedelta
import logging
from custom_components.recycle_app.api import FostPlusApi
from .const import COLLECTION_TYPES, DOMAIN
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry, async_add_entities):
    config: Dict = hass.data[DOMAIN][config_entry.entry_id]
    # Update our config to include new repos and remove those that have been removed.
    # if config_entry.options:
    #     config.update(config_entry.options)
    api = FostPlusApi()
    _LOGGER.debug(f'Adding fractions')

    zipCodeId: str = config["zipCodeId"]
    streetId: str = config["streetId"]
    houseNumber: int = config["houseNumber"]
    fractions: List[str] = config["fractions"]
    refresh: int = config.get("refresh", 24)
    language: str = config.get("language", "fr")

    async def async_update_collections():
        """Fetch data"""
        return await hass.async_add_executor_job(api.getCollections, zipCodeId, streetId, houseNumber)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name='RecycleAppGetCollections',
        update_method=async_update_collections,
        update_interval=timedelta(hours=refresh)
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    uniqueId = f"RecycleApp-{zipCodeId}-{streetId}-{houseNumber}"
    device_info = {
        'identifiers': {
            (DOMAIN, uniqueId)
        },
        'name': config.get("name", "Collecte des poubelles"),
        'manufacturer': 'Fost Plus',
        'model': 'Recycle!'
    }

    async_add_entities([RecycleAppEntity(
        coordinator, f"{uniqueId}-{f}", f, language, device_info) for f in fractions])


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

    @property
    def device_class(self):
        return DEVICE_CLASS_DATE

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
