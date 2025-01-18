"""RecycleApp Helpers."""

import re

from homeassistant.helpers.translation import async_get_translations


async def get_localized_date(
    hass, date_object, format_str, language="nl", domain="your_domain"
):
    """Helper function to format the date with localized values for the given format."""

    # Get translations for the current language (e.g., Dutch)
    translations = await async_get_translations(hass, language, "common", {domain})

    # Extract month and day translations (full and short forms)
    month_full = {
        key.replace(f"component.{domain}.common.month.full.", ""): value
        for key, value in translations.items()
        if key.startswith(f"component.{domain}.common.month.full.")
    }
    month_short = {
        key.replace(f"component.{domain}.common.month.short.", ""): value
        for key, value in translations.items()
        if key.startswith(f"component.{domain}.common.month.short.")
    }
    day_full = {
        key.replace(f"component.{domain}.common.day.full.", ""): value
        for key, value in translations.items()
        if key.startswith(f"component.{domain}.common.day.full.")
    }
    day_short = {
        key.replace(f"component.{domain}.common.day.short.", ""): value
        for key, value in translations.items()
        if key.startswith(f"component.{domain}.common.day.short.")
    }

    # Mapping of strftime placeholders to localized translations
    translation_map = {
        "%A": day_full.get(date_object.strftime("%A"), date_object.strftime("%A")),
        "%a": day_short.get(date_object.strftime("%A"), date_object.strftime("%a")),
        "%B": month_full.get(date_object.strftime("%B"), date_object.strftime("%B")),
        "%b": month_short.get(date_object.strftime("%B"), date_object.strftime("%b")),
        "%d": date_object.strftime("%d"),  # Numeric day
        "%m": date_object.strftime("%m"),  # Numeric month
        "%Y": date_object.strftime("%Y"),  # Full year
        "%y": date_object.strftime("%y"),  # Short year
    }

    # Replace strftime placeholders in the format string with localized values
    def replace_format(match):
        directive = match.group(0)
        return translation_map.get(directive, directive)

    # Apply regex replacement
    localized_date = re.sub(r"%[aAbBdmYy]", replace_format, format_str)

    return localized_date
