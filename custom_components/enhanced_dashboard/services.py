"""Services available for this integration."""
from homeassistant.core import ServiceCall

from .const import (
    DOMAIN,
    SERVICE_REBUILD_DASHBOARD,
    SERVICE_SECURE,
    SERVICE_TURN_OFF_DEVICES,
    SERVICE_TURN_OFF_LIGHTS,
)
from .counters import update_counters
from .share import get_hass
from .template import update_translations


async def setup_services() -> None:
    """Setup services."""

    hass = get_hass()
    register = hass.services.async_register

    async def service_rebuild_dashboard(call: ServiceCall) -> None:
        await update_counters()
        update_translations()
        hass.async_create_task(
            hass.services.async_call("browser_mod", "lovelace_reload")
        )

    async def service_secure(call: ServiceCall) -> None:
        pass

    async def service_turn_off_devices(call: ServiceCall) -> None:
        pass

    async def service_turn_off_lights(call: ServiceCall) -> None:
        pass

    register(DOMAIN, SERVICE_REBUILD_DASHBOARD, service_rebuild_dashboard)
    register(DOMAIN, SERVICE_SECURE, service_secure)
    register(DOMAIN, SERVICE_TURN_OFF_DEVICES, service_turn_off_devices)
    register(DOMAIN, SERVICE_TURN_OFF_LIGHTS, service_turn_off_lights)
