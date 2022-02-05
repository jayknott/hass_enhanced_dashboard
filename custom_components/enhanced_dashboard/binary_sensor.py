"""Binary sensors helper."""
from homeassistant.components.template.const import (
    CONF_AVAILABILITY,
    CONF_OBJECT_ID,
    CONF_PICTURE,
)
from homeassistant.components.template.binary_sensor import (
    BinarySensorTemplate,
    CONF_DELAY_OFF,
    CONF_DELAY_ON,
)
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_NAME,
    CONF_STATE,
    CONF_UNIQUE_ID,
)
from homeassistant.helpers.entity_platform import EntityPlatform

from .const import CONF_ATTRIBUTES, CONF_ENTITY_PLATFORM, PLATFORM_BINARY_SENSOR
from .share import get_hass, get_log

PLATFORM = PLATFORM_BINARY_SENSOR


async def create_binary_sensor_entity(
    device_id: str, conf: dict = {}
) -> BinarySensorTemplate:
    config = {
        CONF_OBJECT_ID: device_id,
        CONF_NAME: device_id,
        CONF_STATE: None,
        CONF_ATTRIBUTES: {},
    }
    config.update(conf)

    platform: EntityPlatform = get_hass().data[CONF_ENTITY_PLATFORM][
        PLATFORM_BINARY_SENSOR
    ][0]

    entity: BinarySensorTemplate = BinarySensorTemplate(
        get_hass(),
        config,
        config.get(CONF_UNIQUE_ID),
    )

    await platform.async_add_entities([entity])

    entity.entity_id = f"{PLATFORM}.{device_id}"

    return entity
