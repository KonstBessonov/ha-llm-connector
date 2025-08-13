import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_BASE_URL, CONF_API_KEY, CONF_MODEL, CONF_MAX_HISTORY

class LLMConnectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="LLM Connector", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_BASE_URL): str,
                vol.Optional(CONF_API_KEY): str,
                vol.Optional(CONF_MODEL, default="gpt-3.5-turbo"): str,
                vol.Optional(CONF_MAX_HISTORY, default=0): int,
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return LLMConnectorOptionsFlowHandler(config_entry)

class LLMConnectorOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_BASE_URL, default=self.config_entry.data.get(CONF_BASE_URL)): str,
                vol.Optional(CONF_API_KEY, default=self.config_entry.data.get(CONF_API_KEY, "")): str,
                vol.Optional(CONF_MODEL, default=self.config_entry.data.get(CONF_MODEL, "")): str,
                vol.Optional(CONF_MAX_HISTORY, default=self.config_entry.data.get(CONF_MAX_HISTORY, 0)): int,
            }),
        )