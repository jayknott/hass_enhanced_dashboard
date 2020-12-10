"""Services available for this integration."""
from homeassistant.core import ServiceCall

from .const import DOMAIN, SERVICE_REBUILD_DASHBOARD
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

    register(DOMAIN, SERVICE_REBUILD_DASHBOARD, service_rebuild_dashboard)
