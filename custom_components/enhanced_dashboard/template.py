"""Override registry settings in enhanced_templates."""
from typing import Any
from homeassistant.helpers.template import (
    _ENVIRONMENT,
    TemplateEnvironment,
)

from .const import JINJA_GLOBALS
from .share import get_hass


async def setup_template() -> None:
    """Setup Jinja template for this integration."""

    jinja: TemplateEnvironment = get_hass().data[_ENVIRONMENT]

    # Add additional Jinja globals
    for jinja_global in JINJA_GLOBALS.items():
        jinja.globals[jinja_global[0]] = jinja_global[1]

    # TODO: Add translations


async def add_template_global(name: str, value: Any) -> None:
    """Add a global to the template."""

    jinja: TemplateEnvironment = get_hass().data[_ENVIRONMENT]

    jinja.globals[name] = value
