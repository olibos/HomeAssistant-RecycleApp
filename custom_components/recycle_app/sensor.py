"""RecycleApp sensor."""
from homeassistant.components.sensor import SensorDeviceClass
from typing import Any, Dict, Tuple
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from datetime import datetime, timedelta
import logging
from custom_components.recycle_app.api import FostPlusApi
from .const import DOMAIN, get_icon
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.event import async_track_time_change

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry, async_add_entities):
    config: Dict = hass.data[DOMAIN][config_entry.entry_id]
    options = config_entry.options
    api = FostPlusApi()

    zip_code_id: str = config["zipCodeId"]
    street_id: str = config["streetId"]
    house_number: int = config["houseNumber"]
    fractions: Dict[str, Tuple[str, str]] = options.get("fractions")
    language: str = options.get("language", "fr")
    _LOGGER.debug(f'zip_code_id: {zip_code_id}')
    _LOGGER.debug(f'street_id: {street_id}')
    _LOGGER.debug(f'house_number: {house_number}')
    _LOGGER.debug(f'fractions: {fractions}')
    _LOGGER.debug(f'language: {language}')

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
    
    last_refresh = datetime.utcnow()

    @callback
    async def async_refresh(now):
        nonlocal last_refresh
        if (datetime.utcnow() - last_refresh).total_seconds() > 120:
            last_refresh=datetime.utcnow()
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

    if isinstance(fractions, dict):
        async_add_entities([RecycleAppEntity(
            coordinator, f"{unique_id}-{fraction}", fraction, color, name, device_info) for (fraction, (color, name)) in fractions.items()])
    else:
        _LOGGER.error(f'Your fractions are in the v1 format... Please delete this address and restart.')

class RecycleAppEntity(CoordinatorEntity, Entity):
    """Base class for all RecycleApp entities."""

    def __init__(
            self,
            coordinator: DataUpdateCoordinator,
            unique_id: str,
            fraction: str,
            color: str,
            name: str,
            device_info: Dict[str, Any] = None
    ):
        """Initialize the entity"""
        super().__init__(coordinator)
        self._unique_id = unique_id
        self._fraction = fraction
        self._image = get_icon(fraction, color)
        self._name = name
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
        return self._name

    @property
    def icon(self) -> str:
        return "mdi:trash-can"

    @property
    def entity_picture(self):
        return self._image

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
