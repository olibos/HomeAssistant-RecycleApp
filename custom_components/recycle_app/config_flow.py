import logging
from typing import Any, Dict, Optional
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowError

from custom_components.recycle_app.api import FostPlusApi, FostPlusApiException

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class RecycleAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, *_):
        return await self.async_step_setup()

    async def async_step_setup(self, info: Optional[Dict[str, Any]] = None):
        errors: Dict[str, str] = {}
        if info is not None:
            try:
                api = FostPlusApi()
                language: str = info["language"]
                zipCodeId, zipCodeName = await self.hass.async_add_executor_job(api.getZipCode, info["zipCode"], language)
                streetId, streetName = await self.hass.async_add_executor_job(api.getStreet, info["street"], zipCodeId, language)
                houseNumber: int = info["streetNumber"]
                fractions = await self.hass.async_add_executor_job(api.getFractions, zipCodeId, streetId, houseNumber)
                await self.async_set_unique_id(f"RecycleApp-{zipCodeId}-{streetId}-{houseNumber}")
                self._abort_if_unique_id_configured()
                name = f"{houseNumber} {streetName}, {zipCodeName}"
                return self.async_create_entry(
                    title=name,
                    data={
                        "zipCodeId": zipCodeId,
                        "streetId": streetId,
                        "houseNumber": houseNumber,
                        "fractions": fractions,
                        "name": name,
                        "refresh": 24,
                        "language": language
                    }
                )

            except FostPlusApiException as error:
                errors['base'] = error.code

            except FlowError as flowError:
                raise flowError

            except Exception as error:
                _LOGGER.error(f"Failed to register {error}", error)
                errors['base'] = "register_failed"

        return self.async_show_form(
            step_id="setup",
            data_schema=vol.Schema(
                {
                    vol.Required("zipCode"): int,
                    vol.Required("street"): str,
                    vol.Required("streetNumber"): int,
                    vol.Required("language", default="fr"): vol.In({"fr": "FR", "nl": "NL", "en": "EN", "de": "DE"})
                }),
            errors=errors
        )
