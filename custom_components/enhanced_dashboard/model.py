"""Base Integration class."""
import logging
from typing import List, Optional, Union
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.components.lovelace.const import MODE_STORAGE, MODE_YAML

from .const import DOMAIN, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


class Configuration:
    """Configuration class."""

    config: dict = {}
    config_entry: ConfigEntry = None
    config_entry_unsub_listener: CALLBACK_TYPE = None
    config_type: Optional[str] = None
    hacs_installed: bool = False
    language: str = DEFAULT_LANGUAGE
    lovelace_mode: Union[MODE_YAML, MODE_STORAGE] = MODE_STORAGE
    missing_resources: List[str] = []
    new_templates: bool = False

    def set_language(self, language: Optional[str]) -> None:
        """Set the language."""

        if language is None:
            return

        if language in SUPPORTED_LANGUAGES:
            self.language = language
            return

        log = logging.getLogger(f"custom_components.{DOMAIN}")
        log.warning(
            f"The specified language, '{language}', is not supported. The default language, '{DEFAULT_LANGUAGE}', has been selected."
        )


class IntegrationBase:
    """Base Integration class."""

    hass: HomeAssistant = None
    log = logging.getLogger(f"custom_components.{DOMAIN}")
    configuration: Configuration = None
    counters: List[str] = []
    super_counters: List[str] = []
