"""Custom integration to integrate RecycleApp with Home Assistant."""

import asyncio
from datetime import date, datetime, timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import FostPlusApi
from .const import DEFAULT_DATE_FORMAT, DOMAIN, MANUFACTURER, WEBSITE
from .info import AppInfo

PLATFORMS = [Platform.CALENDAR, Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)


def _get_next_retry(interval: timedelta | None) -> timedelta:
    new_interval = interval * 2 if interval else timedelta(minutes=5)
    max_interval = timedelta(hours=1)
    return min(new_interval, max_interval)


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup(hass: HomeAssistant, _: ConfigType) -> bool:
    """Set up the RecycleApp component from yaml configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle migration of a config entry to the latest version."""
    version = config_entry.version
    options = config_entry.options
    data = dict(config_entry.data)  # Create a mutable copy of data
    _LOGGER.debug("Migrating from version %s", version)
    if version < 2:
        recycling_park_zip_code = options.get("recyclingParkZipCode")

        # Fix invalid recyclingParkZipCode if needed
        if isinstance(recycling_park_zip_code, list):
            _LOGGER.debug("Converting recyclingParkZipCode from list to single value")
            options = {**options, "recyclingParkZipCode": recycling_park_zip_code[0]}

        hass.config_entries.async_update_entry(
            config_entry, data=data, options=options, version=2
        )
        _LOGGER.info("Migration to version 2 completed")
    
    if version < 3:
        data["entity_id_prefix"] = ""
        hass.config_entries.async_update_entry(
            config_entry, data=data, version=3
        )
        _LOGGER.info("Migration to version 3 completed")

    _LOGGER.info("Migration to version %s successful", config_entry.version)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the RecycleApp component from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})

    config = entry.data
    options = entry.options
    api = FostPlusApi()

    zip_code_id: str = config["zipCodeId"]
    street_id: str = config["streetId"]
    house_number: int = config["houseNumber"]
    fractions: dict[str, tuple[str, str]] = options.get("fractions")
    language: str = options.get("language", "fr")
    date_format: str = options.get("format", DEFAULT_DATE_FORMAT)
    recycling_park_zip_code: str = options.get("recyclingParkZipCode", zip_code_id)
    parks: list[str] = options.get("parks", [])
    entity_id_prefix: str = options.get("entity_id_prefix", "")
    _LOGGER.debug("zip_code_id: %s", zip_code_id)
    _LOGGER.debug("street_id: %s", street_id)
    _LOGGER.debug("house_number: %d", house_number)
    _LOGGER.debug("fractions: %r", fractions)
    _LOGGER.debug("language: %s", language)
    _LOGGER.debug("format: %s", date_format)
    _LOGGER.debug("entity_id_prefix: %s", entity_id_prefix)
    _LOGGER.debug("parks: %r [%s]", parks, recycling_park_zip_code)

    async def async_update_collections() -> dict[str, list[date]]:
        """Fetch data."""
        _LOGGER.debug("Update collections")
        retry = _get_next_retry(coordinator.update_interval)
        try:
            coordinator.update_interval = None
            return await hass.async_add_executor_job(
                api.get_collections, zip_code_id, street_id, house_number
            )
        except Exception as exception:
            coordinator.update_interval = retry
            raise UpdateFailed from exception

    async def async_update_parks() -> dict[str, dict]:
        """Fetch data."""
        _LOGGER.debug("Update recycling parks")
        retry = _get_next_retry(parks_coordinator.update_interval)
        try:
            parks_coordinator.update_interval = None
            return await hass.async_add_executor_job(
                api.get_recycling_parks, recycling_park_zip_code, language
            )
        except Exception as exception:
            parks_coordinator.update_interval = retry
            raise UpdateFailed from exception

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        config_entry=entry,
        name="RecycleAppGetCollections",
        update_method=async_update_collections,
    )

    parks_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        config_entry=entry,
        name="RecycleAppGetRecyclingParks",
        update_method=async_update_parks,
    )

    last_refresh = datetime.min
    unique_id = f"RecycleApp-{entity_id_prefix}-{zip_code_id}-{street_id}-{house_number}"

    @callback
    async def async_refresh(_now: datetime | None = None):
        nonlocal last_refresh
        if (datetime.now() - last_refresh).total_seconds() > 120:
            last_refresh = datetime.now()
            _LOGGER.debug("async_refresh %s", unique_id)
            await asyncio.gather(
                coordinator.async_refresh(), parks_coordinator.async_refresh()
            )

    await hass.async_add_executor_job(api.initialize)
    # Fetch initial data so we have data when entities subscribe
    await async_refresh()

    # Refresh every day at midnight
    async_track_time_change(hass, async_refresh, hour=0, minute=0, second=0)

    device_info = DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, unique_id)},
        name=config.get("name", "Collecte des poubelles"),
        manufacturer=MANUFACTURER,
        model="Waste collection",
        configuration_url=WEBSITE,
    )
    device_registry = dr.async_get(hass)
    for device_entry in dr.async_entries_for_config_entry(
        device_registry, entry.entry_id
    ):
        _domain, identifier = list(device_entry.identifiers)[0]
        if identifier == unique_id:
            continue

        park_id = identifier.split("-")[-1]
        if park_id in parks and unique_id in identifier:
            continue
        _LOGGER.debug(f"Removing device_entry {device_entry}")
        device_registry.async_remove_device(device_entry.id)

    hass.data[DOMAIN][entry.entry_id] = AppInfo(
        collect_device=device_info,
        collect_coordinator=coordinator,
        unique_id=unique_id,
        recycling_park_coordinator=parks_coordinator,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
