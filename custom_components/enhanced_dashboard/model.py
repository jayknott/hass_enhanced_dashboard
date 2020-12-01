"""Base Integration class."""
import logging
from typing import List, Optional, Union

from homeassistant.core import HomeAssistant
from homeassistant.components.lovelace.const import MODE_STORAGE, MODE_YAML

from .const import DOMAIN


class Configuration:
    """Configuration class."""

    config: dict = {}
    config_entry: dict = {}
    config_type: Optional[str] = None
    lovelace_mode: Union[MODE_YAML, MODE_STORAGE] = MODE_STORAGE
    hacs_installed: bool = False
    browser_mod_installed: bool = False
    missing_resources: List[str] = []


class IntegrationBase:
    """Base Integration class."""

    hass: HomeAssistant = None
    log = logging.getLogger(f"custom_components.{DOMAIN}")
    configuration: Configuration = None
    counters: List[str] = []
