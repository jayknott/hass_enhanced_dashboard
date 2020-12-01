"""Setup the integration."""
from homeassistant.components.lovelace.const import MODE_STORAGE
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MODE, EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers.typing import ConfigType

# from .components.automation import setup_automations

# from .components.input_boolean import setup_input_booleans
# from .components.input_number import setup_input_numbers
# from .components.input_select import setup_input_selects
# from .components.input_text import setup_input_texts

# from .components.registry import setup_registries, update_registries
# from .components.template import (
#     setup_template,
#     update_template_areas_global,
#     update_template_entities_global,
# )
# from .components.yaml_parser import setup_yaml_parser
# from .events import setup_events

from .files import setup_files
from .model import Configuration
from .share import get_base, get_configuration, get_hass, get_log

# from .services import setup_services


from .const import DOMAIN, TITLE


async def setup_integration(hass: HomeAssistant, config: ConfigType) -> bool:
    """Main setup procedure for this integration."""

    get_base().hass = hass

    log = get_log()

    # Check for Enhanced Templates
    if "enhanced_templates" not in hass.config.components:
        log.error(
            f"Enhanced Templates is not installed. {TITLE} requires Enhanced Templates to operate."
        )
        return False

    # Check if legacy templates are enabled.
    if hass.config.legacy_templates:
        log.error(
            f"Legacy templates are enabled. {TITLE} requires legacy templates to be disabled."
        )
        return False

    # Check for HACS
    if "hacs" not in hass.config.components:
        log.warning(
            f"HACS is not installed, {TITLE} dependencies will have to be installed manually."
        )
    else:
        get_configuration().hacs_installed = True

    # Check for browser mod.
    if "browser_mod" not in hass.config.components:
        log.warning(
            "Key 'browser_mod' not found in configuration.yaml. Browser mod is required for popups and other UI elements."
        )
    else:
        get_configuration().browser_mod_installed = True

    from .counters import setup_counters
    from .lovelace import setup_lovelace
    from .registry import setup_registry

    # hass.data[DOMAIN] = {
    #     CONF_BUILT_IN_ENTITIES: {},
    #     CONF_MISSING_RESOURCES: [],
    #     CONF_AREAS: [],
    #     CONF_ENTITIES: [],
    # }

    async def handle_hass_started(_event: Event) -> None:
        """Event handler for when HA has started."""

        # await update_registries()
        # await update_template_areas_global()
        # await update_template_entities_global()
        create_task(setup_counters())
        # create_task(setup_input_booleans())
        # create_task(setup_input_numbers())
        # create_task(setup_input_selects())
        # create_task(setup_input_texts())
        # create_task(setup_automations())
        create_task(setup_lovelace())
        # create_task(setup_events())
        # create_task(setup_services())

    # await setup_registries()

    create_task = hass.async_create_task
    create_task(setup_files())
    # create_task(setup_template())
    # create_task(setup_yaml_parser())
    create_task(setup_registry())

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, handle_hass_started)

    return True


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up this integration using yaml."""

    base = get_base()
    base.configuration = (
        base.configuration if base.configuration is not None else Configuration()
    )
    base.configuration.lovelace_mode = config.get(CONF_MODE, MODE_STORAGE)

    if DOMAIN not in config:
        return True

    if base.configuration and base.configuration.config_type == "flow":
        return True

    base.configuration.config = config[DOMAIN]
    base.configuration.config_type = "yaml"

    return await setup_integration(hass, config)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using the UI."""

    base = get_base()

    if base.configuration and base.configuration.config_type == "yaml":
        base.log.warning(
            f"""
                {TITLE} is setup both in config.yaml and integrations.
                The YAML configuration has taken precedence.
            """
        )
        return False

    # Todo: Find out what this means and if it is needed.
    # if config_entry.source == config_entries.SOURCE_IMPORT:
    #     hass.async_create_task(hass.config_entries.async_remove(config_entry.entry_id))
    #     return False

    base.configuration = (
        base.configuration if base.configuration is not None else Configuration()
    )
    base.configuration.config_entry = config_entry
    base.configuration.config_type = "flow"

    return await setup_integration(hass, config_entry.data)
