import logging
from typing import Any, Dict, Optional
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowError
from homeassistant.helpers.selector import selector
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
                zip_code_id, zip_code_name = await self.hass.async_add_executor_job(api.get_zip_code, info["zipCode"], language)
                street_id, street_name = await self.hass.async_add_executor_job(api.get_street, info["street"], zip_code_id, language)
                house_umber: int = info["streetNumber"]
                fractions = await self.hass.async_add_executor_job(api.get_fractions, zip_code_id, street_id, house_umber)
                await self.async_set_unique_id(f"RecycleApp-{zip_code_id}-{street_id}-{house_umber}")
                self._abort_if_unique_id_configured()
                name = f"{house_umber} {street_name}, {zip_code_name}"
                return self.async_create_entry(
                    title=name,
                    data={
                        "zipCodeId": zip_code_id,
                        "streetId": street_id,
                        "houseNumber": house_umber,
                        "fractions": fractions,
                        "name": name,
                        "refresh": 24,
                        "language": language
                    }
                )

            except FostPlusApiException as error:
                errors['base'] = error.code

            except FlowError as flow_error:
                raise flow_error

            except Exception as error:
                _LOGGER.error(f"Failed to register {error}")
                errors['base'] = "register_failed"

        return self.async_show_form(
            step_id="setup",
            data_schema=vol.Schema(
                {
                    vol.Required("zipCode"): int,
                    vol.Required("street"): str,
                    vol.Required("streetNumber"): int,
                    vol.Required("language", default="fr"): selector({
                        "select": {
                            "options": ["fr", "nl", "en", "de"],
                            "mode": "dropdown"
                        }
                    })
                }),
            errors=errors
        )
