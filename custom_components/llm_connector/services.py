"""Регистрация и обработка сервисов интеграции."""
import logging
from typing import Any, Dict
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportResponse
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .llm_client import LLMClient
from .utils import sanitize_user_id, extract_error_message, is_valid_user_id

_LOGGER = logging.getLogger(__name__)

# Схемы валидации для сервисов
SERVICE_ASK_SCHEMA = vol.Schema({
    vol.Required("user_id"): cv.string,
    vol.Required("prompt"): cv.string,
})

SERVICE_RESET_HISTORY_SCHEMA = vol.Schema({
    vol.Required("user_id"): cv.string,
})

async def async_setup_services(hass: HomeAssistant) -> None:
    """Регистрация сервисов интеграции."""
    
    async def handle_ask(call: ServiceCall) -> Dict[str, Any]:
        """Обработка сервиса ask."""
        try:
            _LOGGER.info("Получен вызов сервиса ask: %s", call.data)
            
            raw_user_id = call.data["user_id"]
            prompt = call.data["prompt"]
            
            # Валидация user_id
            if not is_valid_user_id(raw_user_id):
                raise Exception("Неверный формат user_id")
            
            user_id = sanitize_user_id(raw_user_id)
            
            _LOGGER.info("Запрос от пользователя %s: %s", user_id, prompt)
            
            # Получение данных интеграции
            domain_data = hass.data.get(DOMAIN)
            if not domain_data:
                raise Exception("Интеграция не загружена")
            
            _LOGGER.info("Данные интеграции: %s", domain_data.keys())
            
            # Проверка наличия entry
            if "entry" not in domain_data:
                raise Exception("Интеграция не настроена через config flow")
            
            entry = domain_data["entry"]
            _LOGGER.info("Данные entry: %s", entry.data)
            
            # Получение конфигурации
            base_url = entry.data.get("base_url")
            api_key = entry.data.get("api_key")
            model = entry.data.get("model")
            max_history = entry.data.get("max_history", 0)
            
            _LOGGER.info("Конфигурация: base_url=%s, model=%s", base_url, model)
            
            # Валидация базового URL
            if not base_url:
                raise Exception("Не указан базовый URL")
            
            # Получение менеджера чата
            chat_manager = domain_data["chat_manager"]
            if not chat_manager:
                raise Exception("Менеджер чата не инициализирован")
            
            # Создание клиента LLM
            async with LLMClient(base_url, api_key, model) as client:
                # Получение истории
                history = chat_manager.get_history(user_id)
                _LOGGER.info("История пользователя %s: %s сообщений", user_id, len(history))
                
                # Ограничение истории, если задано
                if max_history > 0 and len(history) > max_history:
                    history = history[-max_history:]
                    _LOGGER.info("История ограничена до %s сообщений", max_history)
                
                # Отправка запроса к LLM
                _LOGGER.info("Отправка запроса к LLM...")
                response = await client.ask(prompt, history, model)
                
                # Сохранение в истории
                chat_manager.add_message(user_id, "user", prompt)
                chat_manager.add_message(user_id, "assistant", response)
                await chat_manager.async_save()
                
                _LOGGER.info("Ответ пользователю %s: %s", user_id, response)
                
                return {"response": response}
                
        except Exception as e:
            error_msg = extract_error_message(e)
            _LOGGER.error("Ошибка при обработке запроса для пользователя %s: %s", call.data.get("user_id", "unknown"), error_msg)
            raise Exception(error_msg)

    async def handle_reset_history(call: ServiceCall) -> None:
        """Обработка сервиса reset_history."""
        try:
            _LOGGER.info("Получен вызов сервиса reset_history: %s", call.data)
            
            raw_user_id = call.data["user_id"]
            
            # Валидация user_id
            if not is_valid_user_id(raw_user_id):
                raise Exception("Неверный формат user_id")
            
            user_id = sanitize_user_id(raw_user_id)
            
            _LOGGER.info("Сброс истории для пользователя %s", user_id)
            
            # Получение менеджера чата
            domain_data = hass.data.get(DOMAIN)
            if not domain_data:
                raise Exception("Интеграция не загружена")
            
            chat_manager = domain_data["chat_manager"]
            if not chat_manager:
                raise Exception("Менеджер чата не инициализирован")
            
            # Сброс истории
            await chat_manager.reset_history(user_id)
            
            _LOGGER.info("История для пользователя %s успешно сброшена", user_id)
            
        except Exception as e:
            error_msg = extract_error_message(e)
            _LOGGER.error("Ошибка при сбросе истории для пользователя %s: %s", call.data.get("user_id", "unknown"), error_msg)
            raise Exception(error_msg)

    # Регистрация сервисов
    hass.services.async_register(
        DOMAIN,
        "ask",
        handle_ask,
        schema=SERVICE_ASK_SCHEMA,
        supports_response=SupportsResponse.ONLY
    )
    
    hass.services.async_register(
        DOMAIN,
        "reset_history",
        handle_reset_history,
        schema=SERVICE_RESET_HISTORY_SCHEMA
    )
    
    _LOGGER.info("Сервисы интеграции %s зарегистрированы", DOMAIN)