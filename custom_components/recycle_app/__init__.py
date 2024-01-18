"""Custom integration to integrate RecycleApp with Home Assistant."""
from datetime import datetime
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import Config, HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import FostPlusApi
from .const import DEFAULT_DATE_FORMAT, DOMAIN

PLATFORMS = [Platform.SENSOR, Platform.CALENDAR]
_LOGGER = logging.getLogger(__name__)


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup(hass: HomeAssistant, _: Config) -> bool:
    """Set up the RecycleApp component from yaml configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the RecycleApp component from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = entry.data

    config = entry.data
    options = entry.options
    api = FostPlusApi()

    zip_code_id: str = config["zipCodeId"]
    street_id: str = config["streetId"]
    house_number: int = config["houseNumber"]
    fractions: dict[str, tuple[str, str]] = options.get("fractions")
    language: str = options.get("language", "fr")
    date_format: str = options.get("format", DEFAULT_DATE_FORMAT)
    _LOGGER.debug(f"zip_code_id: {zip_code_id}")
    _LOGGER.debug(f"street_id: {street_id}")
    _LOGGER.debug(f"house_number: {house_number}")
    _LOGGER.debug(f"fractions: {fractions}")
    _LOGGER.debug(f"language: {language}")
    _LOGGER.debug(f"format: {date_format}")

    async def async_update_collections():
        """Fetch data."""
        _LOGGER.debug("Update collections")
        return await hass.async_add_executor_job(
            api.get_collections, zip_code_id, street_id, house_number
        )

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="RecycleAppGetCollections",
        update_method=async_update_collections,
    )

    last_refresh = datetime.now()
    unique_id = f"RecycleApp-{zip_code_id}-{street_id}-{house_number}"

    @callback
    async def async_refresh(now):
        nonlocal last_refresh
        if (datetime.now() - last_refresh).total_seconds() > 120:
            last_refresh = datetime.now()
            _LOGGER.debug(f"async_refresh {unique_id}")
            await coordinator.async_refresh()

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    # Refresh every day at midnight
    async_track_time_change(hass, async_refresh, hour=0, minute=0, second=0)

    device_info = DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, unique_id)},
        name=config.get("name", "Collecte des poubelles"),
        manufacturer="Fost Plus",
        model="Recycle!",
    )

    for platform in PLATFORMS:
        # Forward the setup to the target platform.
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
