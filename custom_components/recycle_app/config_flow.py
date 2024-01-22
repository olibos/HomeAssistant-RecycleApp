"""RecycleApp ConfigFlow definitions."""
import logging
from typing import Any, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowError, FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import selector

from .api import FostPlusApi, FostPlusApiException
from .const import DEFAULT_DATE_FORMAT, DOMAIN

_LOGGER = logging.getLogger(__name__)


class RecycleAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    def __init__(self) -> None:
        self._data = {}
        self._options = {}
        self._parks = {}

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
                date_format: str = info.get("format", DEFAULT_DATE_FORMAT)
                fractions = await self.hass.async_add_executor_job(
                    api.get_fractions, zip_code_id, street_id, house_umber, language
                )
                await self.async_set_unique_id(
                    f"RecycleApp-{zip_code_id}-{street_id}-{house_umber}"
                )
                self._abort_if_unique_id_configured()
                name = f"{house_umber} {street_name}, {zip_code_name}"
                self._data = {
                    "zipCodeId": zip_code_id,
                    "streetId": street_id,
                    "houseNumber": house_umber,
                    "name": name,
                }
                recycling_park_zip_code = info.get("recyclingParkZipCode", None)
                if recycling_park_zip_code:
                    zip_code_id = (
                        await self.hass.async_add_executor_job(
                            api.get_zip_code, recycling_park_zip_code, language
                        )
                    )[0]
                self._options = {
                    "language": language,
                    "format": date_format,
                    "fractions": fractions,
                    "recyclingParkZipCode": zip_code_id,
                    "parks": [],
                }
                self._parks = await self.hass.async_add_executor_job(
                    api.get_recycling_parks, zip_code_id, language
                )

                if len(self._parks) > 0:
                    return await self.async_step_parks()
                else:
                    return self.async_create_entry(
                        title=name,
                        data=self._data,
                        options=self._options,
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
                    vol.Required("format", default=DEFAULT_DATE_FORMAT): str,
                    vol.Optional(
                        "recyclingParkZipCode",
                    ): OptionalInt(),
                }
            ),
            errors=errors,
        )

    async def async_step_parks(self, user_input: Optional[dict[str, Any]] = None):
        if user_input is not None:
            _LOGGER.info(f"user_input: {user_input}")
            self._options["parks"] = user_input["parks"]
            return self.async_create_entry(
                title=self._data["name"],
                data=self._data,
                options=self._options,
            )

        parks = list(self._parks.keys())

        return self.async_show_form(
            step_id="parks",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "parks",
                        default=parks,
                    ): cv.multi_select(
                        {key: value["name"] for key, value in self._parks.items()}
                    )
                }
            ),
            last_step=True,
        )


class OptionalInt(vol.Coerce):
    def __init__(self):
        super().__init__(int)

    def __call__(self, v: int) -> Optional[int]:
        """Validate input."""
        if v:
            try:
                return int(v)
            except ValueError as error:
                raise vol.Invalid("Not an integer!") from error

        return v


class RecycleAppOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self._parks = None
        self._data = None

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
            recycling_park_zip_code = user_input.get("recyclingParkZipCode", None)
            if recycling_park_zip_code:
                zip_code_id = (
                    await self.hass.async_add_executor_job(
                        api.get_zip_code, recycling_park_zip_code, language
                    )
                )[0]
            self._parks = await self.hass.async_add_executor_job(
                api.get_recycling_parks, zip_code_id, language
            )
            self._data = {
                "language": language,
                "format": date_format,
                "fractions": fractions,
                "recyclingParkZipCode": zip_code_id,
                "parks": [],
            }

            if len(self._parks) > 0:
                return await self.async_step_parks()
            else:
                return self.async_create_entry(
                    title="",
                    data=self._data,
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
                    vol.Optional(
                        "recyclingParkZipCode",
                        default=self.config_entry.options.get(
                            "recyclingParkZipCode", ""
                        ).split("-")[0],
                    ): OptionalInt(),
                }
            ),
            last_step=False,
        )

    async def async_step_parks(self, user_input: dict[str, Any] = None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            self._data["parks"] = user_input["parks"]
            return self.async_create_entry(
                title="",
                data=self._data,
            )

        parks = self.config_entry.options.get("parks", None)
        if parks:
            parks = list(set(parks) & set(self._parks.keys()))
        else:
            parks = list(self._parks.keys())

        return self.async_show_form(
            step_id="parks",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "parks",
                        default=parks,
                    ): cv.multi_select(
                        {key: value["name"] for key, value in self._parks.items()}
                    )
                }
            ),
            last_step=True,
        )
