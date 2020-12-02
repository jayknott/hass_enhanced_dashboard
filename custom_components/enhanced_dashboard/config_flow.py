"""Adds config flow for this integration."""
from custom_components.enhanced_dashboard.share import get_configuration, get_log
from typing import Any, Dict, Optional
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType

from .const import DEFAULT_LANGUAGE, DOMAIN, SUPPORTED_LANGUAGES, TITLE

OPTIONS_SCHEMA = vol.Schema(
    {vol.Required("language", default=DEFAULT_LANGUAGE): vol.In(SUPPORTED_LANGUAGES)}
)


class EnhancedDashboardFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for this integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    OPTIONS_SCHEMA = vol.Schema(
        {
            vol.Required("language", default=DEFAULT_LANGUAGE): vol.In(
                SUPPORTED_LANGUAGES
            )
        }
    )

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if self.hass.data.get(DOMAIN):
            return self.async_abort(reason="single_instance_allowed")

        if not user_input or user_input.get("language") is None:
            return self.async_show_form(step_id="user", data_schema=OPTIONS_SCHEMA)

        user_input_update = user_input if user_input is not None else {}
        return self.async_create_entry(title=TITLE, data=user_input_update)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        return EnhancedDashboardOptionsFlowHandler(config_entry)


class EnhancedDashboardOptionsFlowHandler(config_entries.OptionsFlow):
    """Integration config flow options handler."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialize integration options flow."""

        self.config_entry = config_entry

    async def async_step_init(self, user_input: ConfigType = None):
        """Manage the options."""

        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input: ConfigType = None):
        """User initiated options."""

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            "language",
                            default=(get_configuration().language),
                        ): vol.In(SUPPORTED_LANGUAGES)
                    }
                ),
            )

        return self.async_create_entry(title=TITLE, data=user_input)