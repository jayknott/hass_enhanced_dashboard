"""Services available for this integration."""
from custom_components.enhanced_dashboard.counters import update_counters
from homeassistant.core import ServiceCall

from .const import DOMAIN, SERVICE_REBUILD_COUNTERS
from .share import get_hass


async def setup_services() -> None:
    """Setup services."""

    hass = get_hass()
    register = hass.services.async_register

    async def service_rebuild_counters(call: ServiceCall) -> None:
        await update_counters()
        hass.async_create_task(
            hass.services.async_call("browser_mod", "lovelace_reload")
        )

    register(DOMAIN, SERVICE_REBUILD_COUNTERS, service_rebuild_counters)
