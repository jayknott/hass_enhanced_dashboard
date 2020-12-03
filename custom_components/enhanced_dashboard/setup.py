"""Setup the integration."""
from homeassistant.components.lovelace.const import MODE_STORAGE
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MODE, EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .model import Configuration
from .share import get_base, get_configuration, get_log
from .template import add_template_global

# from .services import setup_services


from .const import DOMAIN, HACS_INTEGRATIONS, LOVELACE_DIR, TITLE


async def setup_integration(hass: HomeAssistant, config: ConfigType) -> bool:
    """Main setup procedure for this integration."""

    get_base().hass = hass
    conf = get_configuration()
    log = get_log()

    # Check if legacy templates are enabled.
    if hass.config.legacy_templates:
        log.error(
            f"Legacy templates are enabled. {TITLE} requires legacy templates to be disabled."
        )
    else:
        conf.new_templates = True

    # Check for HACS
    if "hacs" not in hass.config.components:
        log.warning(
            f"HACS is not installed, {TITLE} dependencies will have to be installed manually."
        )
    else:
        conf.hacs_installed = True

    # hass.data[DOMAIN] = {
    #     CONF_BUILT_IN_ENTITIES: {},
    #     CONF_MISSING_RESOURCES: [],
    #     CONF_AREAS: [],
    #     CONF_ENTITIES: [],
    # }

    if conf.hacs_installed:
        from .hacs import setup_hacs, pending_restart

        await setup_hacs()
        if pending_restart():
            log.error(
                f"A required HACS integration requires a restart. Please restart Home Assistant for {TITLE} to be available."
            )
            return False

    # Check for required integrations
    missing_integration = False
    for integration in HACS_INTEGRATIONS.keys():
        if integration not in hass.config.components:
            log.error(
                f"The required HACS integration, '{integration}', is not installed. It may need to be installed manually."
            )
            missing_integration = True

    if missing_integration:
        return False

    from .files import setup_files
    from .registry import setup_registry
    from .template import setup_template

    create_task = hass.async_create_task
    create_task(setup_files())
    create_task(setup_template())
    create_task(setup_registry())

    add_template_global(
        "config",
        {
            "language": conf.language,
            "lovelace_dir": LOVELACE_DIR,
            "missing_resources": conf.missing_resources,
        },
    )

    async def handle_hass_started(_event: Event) -> None:
        """Event handler for when HA has started."""

        from .lovelace import setup_lovelace
        from .counters import setup_counters

        create_task(setup_counters())
        create_task(setup_lovelace())
        # create_task(setup_events())
        # create_task(setup_services())

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, handle_hass_started)

    return True


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up this integration using yaml."""

    conf = get_configuration()

    if conf is None:
        conf = Configuration()

    conf.lovelace_mode = config.get(CONF_MODE, MODE_STORAGE)

    if DOMAIN not in config:
        return True

    if conf and conf.config_type == "flow":
        return True

    conf.config = config[DOMAIN]
    conf.config_type = "yaml"

    conf.set_language(config.get(DOMAIN, {}).get("language"))

    if config.get(DOMAIN, {}).get("language") is not None:
        conf.language = config[DOMAIN]["language"]

    return await setup_integration(hass, config)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using the UI."""

    # base = get_base()
    conf = get_configuration()

    if conf and conf.config_type == "yaml":
        get_log().warning(
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

    if conf is None:
        conf = Configuration()

    conf.config_entry = config_entry
    conf.config_type = "flow"

    conf.set_language(config_entry.data.get("language"))

    async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
        """Listen for options updates."""

        get_log().warn("Listening for option updates")

    conf.config_entry_unsub_listener = config_entry.add_update_listener(update_listener)

    return await setup_integration(hass, config_entry)
