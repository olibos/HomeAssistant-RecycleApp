"""Fraction display-name helpers shared by RecycleApp entities."""

import homeassistant.helpers.entity_registry as er


def get_fraction_name(
    entity_registry: er.EntityRegistry,
    entity_id: str | None,
    fractions: dict[str, tuple[str, str]],
    fraction_id: str,
) -> str:
    """Return a fraction sensor's own name, without the device name.

    Honors names the user set on the fraction sensor in the entity registry.

    HA >= 2026.11 prefixes the device name in friendly_name and exposes the
    entity-only name as RegistryEntry.entity_name (same as the entity_name()
    template function). Older versions never prefixed our names, so the
    registry name / original_name is already the bare fraction name.

    Falls back to the fraction name stored in the config entry options.
    """
    if entity_id and (entry := entity_registry.async_get(entity_id)):
        if name := (
            getattr(entry, "entity_name", None) or entry.name or entry.original_name
        ):
            return name
    return fractions.get(fraction_id, ("", fraction_id))[1]
