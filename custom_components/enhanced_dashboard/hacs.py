"""Extend Lovelace to support this integration."""
# try:
from custom_components.hacs.helpers.functions.register_repository import (
    register_repository,
)
from custom_components.hacs.share import get_hacs

# except:
#     hacs_repository = None
#     hacs_repository_data = None
#     get_hacs = None

from .const import (
    HACS_CUSTOM_REPOSITORIES,
    HACS_INTEGRATIONS,
    HACS_PLUGINS,
)
from .share import get_configuration, get_log


async def setup_hacs() -> None:
    """Setup HACS modules"""

    await update_hacs()


async def update_hacs() -> None:
    """Install or update hacs integrations and frontend plugins."""

    if not get_configuration().hacs_installed:
        return

    log = get_log()
    hacs = get_hacs()

    # Add custom repositories to HACS
    for repo in HACS_CUSTOM_REPOSITORIES:
        await register_repository(repo["full_name"], repo["type"])

    # Install needed HACS integrations and plugins
    for hacs_plugin in list(HACS_INTEGRATIONS.values()) + HACS_PLUGINS:
        try:
            repo = hacs.get_by_name(hacs_plugin)
            if repo.data.installed:
                log.warning(f"{hacs_plugin} already installed.")
            else:
                log.warning(f"{hacs_plugin} installing.")
            try:
                pass
                await repo.async_install()
            except:
                log.error("Unable to install HACS repository: %s", hacs_plugin)
        except:
            log.warning(
                f"Could not connect to HACS to install '{hacs_plugin}', will assume everything is okay."
            )


def pending_restart():
    """HACS has a dependency that requires a restart."""

    if not get_configuration().hacs_installed:
        return False

    log = get_log()

    for hacs_plugin in list(HACS_INTEGRATIONS.values()) + HACS_PLUGINS:
        try:
            repo = get_hacs().get_by_name(hacs_plugin)
            if repo.pending_restart:
                return True

        except:
            log.warning(
                f"Could not connect to HACS install '{hacs_plugin}', will assume everything is okay."
            )

    return False
