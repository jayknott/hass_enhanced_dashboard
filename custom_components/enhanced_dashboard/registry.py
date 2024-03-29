"""Override registry settings in enhanced_templates."""
from .const import (
    ALL_ENTITY_TYPES,
    COVER_CLASS_MAP,
    DEFAULT_AREA_ICON,
    BINARY_SENSOR_CLASS_MAP,
    PLATFORM_MAP,
    SENSOR_CLASS_MAP,
)


async def setup_registry() -> None:
    import custom_components.enhanced_templates.const as et_const
    import custom_components.enhanced_templates.registry as et_registry

    et_const.DEFAULT_AREA_ICON = DEFAULT_AREA_ICON
    et_registry.BINARY_SENSOR_CLASS_MAP = BINARY_SENSOR_CLASS_MAP
    et_registry.COVER_CLASS_MAP = COVER_CLASS_MAP
    et_registry.ENTITY_TYPES = ALL_ENTITY_TYPES
    et_registry.PLATFORM_MAP = PLATFORM_MAP
    et_registry.SENSOR_CLASS_MAP = SENSOR_CLASS_MAP

    et_registry.update_registry()
