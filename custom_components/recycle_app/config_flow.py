"""RecycleApp ConfigFlow definitions."""
import logging
from typing import Any, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowError, FlowResult
from homeassistant.helpers.selector import selector

from .api import FostPlusApi, FostPlusApiException
from .const import DEFAULT_DATE_FORMAT, DOMAIN

_LOGGER = logging.getLogger(__name__)


class RecycleAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return RecycleAppOptionsFlowHandler(config_entry)

    async def async_step_user(self, *_):
        return await self.async_step_setup()

    async def async_step_setup(self, info: Optional[dict[str, Any]] = None):
        errors: dict[str, str] = {}
        if info is not None:
            try:
                api = FostPlusApi()
                language: str = info["language"]
                zip_code_id, zip_code_name = await self.hass.async_add_executor_job(
                    api.get_zip_code, info["zipCode"], language
                )
                street_id, street_name = await self.hass.async_add_executor_job(
                    api.get_street, info["street"], zip_code_id, language
                )
                house_umber: int = info["streetNumber"]
                fractions = await self.hass.async_add_executor_job(
                    api.get_fractions, zip_code_id, street_id, house_umber, language
                )
                await self.async_set_unique_id(
                    f"RecycleApp-{zip_code_id}-{street_id}-{house_umber}"
                )
                self._abort_if_unique_id_configured()
                name = f"{house_umber} {street_name}, {zip_code_name}"
                return self.async_create_entry(
                    title=name,
                    data={
                        "zipCodeId": zip_code_id,
                        "streetId": street_id,
                        "houseNumber": house_umber,
                        "name": name,
                    },
                    options={"fractions": fractions, "language": language},
                )

            except FostPlusApiException as error:
                errors["base"] = error.code

            except FlowError as flow_error:
                raise flow_error

            except Exception as error:
                _LOGGER.error(f"Failed to register {error}")
                errors["base"] = "register_failed"

        return self.async_show_form(
            step_id="setup",
            data_schema=vol.Schema(
                {
                    vol.Required("zipCode"): int,
                    vol.Required("street"): str,
                    vol.Required("streetNumber"): int,
                    vol.Required("language", default="fr"): selector(
                        {
                            "select": {
                                "options": ["fr", "nl", "en", "de"],
                                "mode": "dropdown",
                            }
                        }
                    ),
                }
            ),
            errors=errors,
        )


class RecycleAppOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] = None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            api = FostPlusApi()
            zip_code_id = self.config_entry.data.get("zipCodeId")
            street_id = self.config_entry.data.get("streetId")
            house_umber = self.config_entry.data.get("houseNumber")
            language = user_input.get("language", "fr")
            date_format = user_input.get("format", DEFAULT_DATE_FORMAT)
            fractions = await self.hass.async_add_executor_job(
                api.get_fractions, zip_code_id, street_id, house_umber, language
            )
            return self.async_create_entry(
                title="",
                data={
                    "language": language,
                    "format": date_format,
                    "fractions": fractions,
                },
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "language",
                        default=self.config_entry.options.get("language", "fr"),
                    ): selector(
                        {
                            "select": {
                                "options": ["fr", "nl", "en", "de"],
                                "mode": "dropdown",
                            }
                        }
                    ),
                    vol.Required(
                        "format",
                        default=self.config_entry.options.get(
                            "format", DEFAULT_DATE_FORMAT
                        ),
                    ): str,
                }
            ),
        )
