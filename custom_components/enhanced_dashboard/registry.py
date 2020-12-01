"""Override registry settings in enhanced_templates."""
import custom_components.enhanced_templates.const as et_const
import custom_components.enhanced_templates.registry as et_registry

from .const import (
    COVER_CLASS_MAP,
    DEFAULT_AREA_ICON,
    ENTITY_TYPES,
    BINARY_SENSOR_CLASS_MAP,
    PLATFORM_MAP,
    SENSOR_CLASS_MAP,
)


async def setup_registry() -> None:
    et_const.DEFAULT_AREA_ICON = DEFAULT_AREA_ICON
    et_registry.BINARY_SENSOR_CLASS_MAP = BINARY_SENSOR_CLASS_MAP
    et_registry.COVER_CLASS_MAP = COVER_CLASS_MAP
    et_registry.ENTITY_TYPES = ENTITY_TYPES
    et_registry.PLATFORM_MAP = PLATFORM_MAP
    et_registry.SENSOR_CLASS_MAP = SENSOR_CLASS_MAP

    await et_registry.update_registry()
