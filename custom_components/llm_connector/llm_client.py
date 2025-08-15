"""Клиент для работы с OpenAI-совместимыми API."""
import aiohttp
import asyncio
from typing import List, Dict, Optional
import json
import logging

_LOGGER = logging.getLogger(__name__)

class LLMClient:
    """Клиент для работы с LLM через OpenAI-совместимое API."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 90
    ):
        """Инициализация клиента."""
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self._session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Получение или создание HTTP сессии."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def ask(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        model: Optional[str] = None
    ) -> str:
        """Отправка запроса к LLM и получение ответа."""
        try:
            # Подготовка сообщений
            messages = history.copy()
            messages.append({"role": "user", "content": prompt})

            # Подготовка данных запроса
            request_data = {
                "messages": messages
            }
            
            # Добавляем модель, если указана
            selected_model = model or self.model
            if selected_model:
                request_data["model"] = selected_model

            # Подготовка заголовков
            headers = {
                "Content-Type": "application/json",
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Отправка запроса
            session = await self._get_session()
            url = f"{self.base_url}/chat/completions"
            
            _LOGGER.debug("Отправка запроса к %s", url)
            _LOGGER.debug("Данные запроса: %s", json.dumps(request_data, ensure_ascii=False))

            async with session.post(url, json=request_data, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    _LOGGER.error("Ошибка API: %s - %s", response.status, error_text)
                    raise Exception(f"API ошибка: {response.status} - {error_text}")

                result = await response.json()
                _LOGGER.debug("Ответ от API: %s", json.dumps(result, ensure_ascii=False))

                # Извлечение ответа
                if "choices" in result and len(result["choices"]) > 0:
                    choice = result["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        return choice["message"]["content"].strip()
                    else:
                        raise Exception("Неверный формат ответа от API")
                else:
                    raise Exception("Пустой ответ от API")

        except asyncio.TimeoutError:
            _LOGGER.error("Таймаут при запросе к LLM")
            raise Exception("Превышено время ожидания ответа от LLM")
        except aiohttp.ClientError as e:
            _LOGGER.error("Ошибка соединения: %s", str(e))
            raise Exception(f"Ошибка соединения: {str(e)}")
        except Exception as e:
            _LOGGER.error("Неожиданная ошибка: %s", str(e))
            raise Exception(f"Ошибка при работе с LLM: {str(e)}")

    async def close(self):
        """Закрытие HTTP сессии."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        """Контекстный менеджер."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие сессии при выходе из контекста."""
        await self.close()