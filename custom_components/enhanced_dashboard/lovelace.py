"""Extend Lovelace to support this integration."""
import os
from typing import Type

from homeassistant.components.frontend import (
    async_register_built_in_panel,
    async_remove_panel,
    DATA_PANELS,
)
from homeassistant.components.lovelace import CONF_DASHBOARDS
from homeassistant.components.lovelace.dashboard import LovelaceYAML
from homeassistant.components.lovelace.const import (
    CONF_ICON,
    CONF_MODE,
    CONF_REQUIRE_ADMIN,
    CONF_RESOURCE_TYPE_WS,
    CONF_RESOURCES,
    CONF_SHOW_IN_SIDEBAR,
    CONF_TITLE,
    DOMAIN as LOVELACE_DOMAIN,
    MODE_STORAGE,
    MODE_YAML,
)
from homeassistant.const import (
    CONF_FILENAME,
    CONF_URL,
)
from homeassistant.helpers.collection import StorageCollection

from .const import (
    HACS_PLUGINS,
    LOVELACE_CUSTOM_CARDS,
    LOVELACE_DASHBOARD_ICON,
    LOVELACE_DASHBOARD_URL_PATH,
    LOVELACE_DIR,
    LOVELACE_FILENAME_SOURCE,
    LOVELACE_RESOURCE_TYPE_MODULE,
    TITLE,
)
from .share import get_base, get_configuration, get_hass, get_log


async def setup_lovelace() -> None:
    """Setup Lovelace"""

    await update_resources()
    await update_dashboards()


async def add_resource_module(url: str) -> None:
    """Add a resource to the Lovelace resources list if it doesn't exist."""

    conf = get_configuration()
    hass = get_hass()
    log = get_log()

    resources: Type[StorageCollection] = hass.data[LOVELACE_DOMAIN][CONF_RESOURCES]

    for resource in resources.async_items():
        if resource[CONF_URL] == url:
            # Item is already in the list
            return

    if conf.lovelace_mode == MODE_STORAGE:
        await resources.async_create_item(
            {CONF_URL: url, CONF_RESOURCE_TYPE_WS: LOVELACE_RESOURCE_TYPE_MODULE}
        )
    else:
        log.error(
            f"{url} is not in the lovelace:resources list in the configuration.yaml"
        )
        conf.missing_resources.append(url)


async def update_resources() -> None:
    """Check Lovelace resources and and resources that are missing if in storage mode."""

    # base = get_base()
    conf = get_configuration()
    log = get_log()

    # Reset missing resources
    missing_resources = conf.missing_resources = []

    # Add custom cards to the list
    for card in LOVELACE_CUSTOM_CARDS:
        url = (
            f"/local/{LOVELACE_DASHBOARD_URL_PATH}/{card['dirname']}/{card['filename']}"
        )
        await add_resource_module(url)

    if not conf.hacs_installed:
        return

    from custom_components.hacs.share import get_hacs

    hacs = get_hacs()

    # Add the HACS plugins to the list
    for hacs_plugin in HACS_PLUGINS:
        try:
            repo = hacs.get_by_name(hacs_plugin)
            url = f"/hacsfiles/{hacs_plugin.split('/')[-1]}/{repo.data.file_name}"

            try:
                await add_resource_module(url)
            except:
                log.error(
                    f"Unable to add {hacs_plugin} the the Lovelace resource list.",
                    hacs_plugin,
                )
                missing_resources.append(url)
        except:
            log.warning(
                f"Could not connect to HACS to check repository for '{hacs_plugin}', will assume everything is okay."
            )


async def update_dashboards() -> None:
    """Add this integrations Lovelace dashboard."""

    hass = get_base().hass

    config = {
        CONF_MODE: MODE_YAML,
        CONF_TITLE: TITLE,
        CONF_ICON: LOVELACE_DASHBOARD_ICON,
        CONF_SHOW_IN_SIDEBAR: True,
        CONF_REQUIRE_ADMIN: False,
        CONF_FILENAME: os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                LOVELACE_DIR,
                LOVELACE_FILENAME_SOURCE,
            )
        ),
    }

    yaml_config = LovelaceYAML(hass, LOVELACE_DASHBOARD_URL_PATH, config)
    hass.data[LOVELACE_DOMAIN][CONF_DASHBOARDS][
        LOVELACE_DASHBOARD_URL_PATH
    ] = yaml_config

    kwargs = {
        "frontend_url_path": LOVELACE_DASHBOARD_URL_PATH,
        "require_admin": config[CONF_REQUIRE_ADMIN],
        "config": {CONF_MODE: config[CONF_MODE]},
        "update": False,
        "sidebar_title": config[CONF_TITLE],
        "sidebar_icon": config[CONF_ICON],
    }

    if LOVELACE_DASHBOARD_URL_PATH in hass.data.get(DATA_PANELS, {}):
        async_remove_panel(hass, LOVELACE_DASHBOARD_URL_PATH)

    async_register_built_in_panel(hass, LOVELACE_DOMAIN, **kwargs)

    # Refresh lovelace using browser_mod
    hass.async_create_task(hass.services.async_call("browser_mod", "lovelace_reload"))
