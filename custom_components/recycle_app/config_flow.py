"""RecycleApp ConfigFlow definitions."""

import logging
from typing import Any

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
    """Handle a config flow for RecycleApp."""

    VERSION = 2

    def __init__(self) -> None:
        """Initialize the config flow handler."""
        self._data = {}
        self._options = {}
        self._parks = {}
        self._zip_codes = []
        self._saved_steps = []

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return RecycleAppOptionsFlowHandler(config_entry)

    async def async_step_user(self, *_) -> FlowResult:
        """Handle the initial step initiated by the user."""
        return await self.async_step_setup()

    async def async_step_zip_codes(
        self, info: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the step for selecting a zip code.

        This step presents a form to the user with a list of zip codes to choose from.
        When the user has provided a zip code, it proceeds to the setup step.

        Args:
            info (dict[str, Any] | None): The information provided by the user,
                                          containing the selected zip code index.

        Returns:
            FlowResult: The result of the flow, either showing the form again or
                        proceeding to the setup step with the selected zip code.

        """

        errors: dict[str, str] = {}

        if info is not None:
            index = int(info["zip_code"])
            zip_code = self._zip_codes[index]
            return await self.async_step_setup(self._saved_steps.pop(), zip_code)

        return self.async_show_form(
            step_id="zip_codes",
            data_schema=vol.Schema(
                {
                    vol.Required("zip_code"): selector(
                        {
                            "select": {
                                "options": [
                                    {"label": label, "value": str(idx)}
                                    for idx, (_, label) in enumerate(self._zip_codes)
                                ],
                                "mode": "list",
                            }
                        }
                    )
                }
            ),
            last_step=False,
            errors=errors,
        )

    async def async_step_setup(
        self,
        info: dict[str, Any] | None = None,
        selected_zip_code: tuple[str, str] | None = None,
    ) -> FlowResult:
        """Handle the setup step."""
        errors: dict[str, str] = {}
        if info is not None:
            try:
                api = FostPlusApi()
                language: str = info["language"]
                zip_codes = (
                    await self.hass.async_add_executor_job(
                        api.get_zip_code, info["zipCode"], language
                    )
                    if selected_zip_code is None
                    else [selected_zip_code]
                )
                if len(zip_codes) > 1:
                    self._saved_steps.append(info)
                    self._zip_codes = zip_codes
                    return await self.async_step_zip_codes()

                zip_code_id, zip_code_name = zip_codes[0]
                street_id, street_name = await self.hass.async_add_executor_job(
                    api.get_street, info["street"], zip_code_id, language
                )
                house_number: int = info["streetNumber"]
                date_format: str = info.get("format", DEFAULT_DATE_FORMAT)
                fractions = await self.hass.async_add_executor_job(
                    api.get_fractions, zip_code_id, street_id, house_number, language
                )
                await self.async_set_unique_id(
                    f"RecycleApp-{zip_code_id}-{street_id}-{house_number}"
                )
                self._abort_if_unique_id_configured()
                name = f"{house_number} {street_name}, {zip_code_name}"
                self._data = {
                    "zipCodeId": zip_code_id,
                    "streetId": street_id,
                    "houseNumber": house_number,
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
                    "entity_id_prefix": info.get("entity_id_prefix", ""),
                }
                self._parks = await self.hass.async_add_executor_job(
                    api.get_recycling_parks, zip_code_id, language
                )

                if len(self._parks) > 0:
                    return await self.async_step_parks()

                return self.async_create_entry(
                    title=name,
                    data=self._data,
                    options=self._options,
                )

            except FostPlusApiException as error:
                errors["base"] = error.code

            except FlowError:
                raise

            except Exception as error:
                _LOGGER.error("Failed to register %r", error)
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
                    vol.Optional("entity_id_prefix", default=""): str,
                }
            ),
            errors=errors,
        )

    async def async_step_parks(self, user_input: dict[str, Any] | None = None):
        """Handle the parks step."""
        if user_input is not None:
            _LOGGER.debug("user_input: %r", user_input)
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
    """Optional integer validator."""

    def __init__(self) -> None:
        """Initialize the options flow handler."""
        super().__init__(int)

    def __call__(self, v: int) -> int | None:
        """Validate input."""
        if v:
            try:
                return int(v)
            except ValueError as error:
                raise vol.Invalid("Not an integer!") from error

        return v


class RecycleAppOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for RecycleApp."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._parks = None
        self._data = None

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
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
            _LOGGER.critical(f"user input: {user_input}")
            recycling_park_zip_code = user_input.get("recyclingParkZipCode", None)
            _LOGGER.critical(f"ZIP INPUT: {recycling_park_zip_code}\nzip_code_id: {zip_code_id}")
            if recycling_park_zip_code:
                zip_code_id = (
                    await self.hass.async_add_executor_job(
                        api.get_zip_code, recycling_park_zip_code, language
                    )
                )[0]
            self._parks = await self.hass.async_add_executor_job(
                api.get_recycling_parks, zip_code_id, language
            )
            _LOGGER.critical(f"zip_code_id! {zip_code_id}\nparks: {self._parks}")

            entity_id_prefix = user_input.get("entity_id_prefix", "")
            self._data = {
                "language": language,
                "format": date_format,
                "fractions": fractions,
                "recyclingParkZipCode": zip_code_id,
                "parks": [],
                "entity_id_prefix": entity_id_prefix,
            }

            if len(self._parks) > 0:
                return await self.async_step_parks()

            return self.async_create_entry(
                title="",
                data=self._data,
            )

        self.initial_data = {
            "language": self.config_entry.options.get("language", "fr"),
            "format": self.config_entry.options.get("format", DEFAULT_DATE_FORMAT),
            "recyclingParkZipCode": str(
                next(iter(self.config_entry.options.get("recyclingParkZipCode", [])), "")
            ).partition("-")[0],
            "entity_id_prefix": self.config_entry.options.get("entity_id_prefix", ""),
        }
        
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(
                    {
                        vol.Required("language"): selector(
                            {
                                "select": {
                                    "options": ["fr", "nl", "en", "de"],
                                    "mode": "dropdown",
                                }
                            }
                        ),
                        vol.Required("format"): str,
                        vol.Optional("recyclingParkZipCode"): OptionalInt(),
                        vol.Optional("entity_id_prefix"): str,
                    }
                ),
                self.initial_data,
            ),
            last_step=False,
        )

    async def async_step_parks(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
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
