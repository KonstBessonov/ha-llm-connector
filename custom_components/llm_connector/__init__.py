"""Инициализация интеграции LLM Connector."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from .const import DOMAIN, STORAGE_VERSION, STORAGE_KEY
from .services import async_setup_services
from .chat_manager import ChatManager

async def async_setup(hass: HomeAssistant, config) -> bool:
    """Настройка интеграции."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Настройка интеграции через config flow."""
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    chat_manager = ChatManager(store)
    await chat_manager.async_load()

    hass.data[DOMAIN] = {
        "entry": entry,
        "chat_manager": chat_manager,
    }

    await async_setup_services(hass)

    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Выгрузка интеграции."""
    hass.data.pop(DOMAIN)
    return True