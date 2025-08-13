"""Вспомогательные функции для интеграции LLM Connector."""
import re
from typing import List, Dict, Optional
import logging

_LOGGER = logging.getLogger(__name__)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Обрезка текста до заданной длины."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def sanitize_user_id(user_id: str) -> str:
    """Очистка и валидация user_id."""
    if not isinstance(user_id, str):
        user_id = str(user_id)
    
    # Удаление недопустимых символов (оставляем только буквы, цифры, подчеркивание, дефис, точку)
    sanitized = re.sub(r'[^\w\-\.]', '_', user_id)
    
    # Ограничение длины
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
    
    return sanitized

def format_history_for_logging(history: List[Dict[str, str]], max_messages: int = 3) -> str:
    """Форматирование истории для логирования."""
    if not history:
        return "[]"
    
    # Берем только последние сообщения
    recent_history = history[-max_messages:] if len(history) > max_messages else history
    
    formatted = []
    for msg in recent_history:
        role = msg.get("role", "unknown")
        content = truncate_text(msg.get("content", ""), 50)
        formatted.append(f"{role}: {content}")
    
    result = " | ".join(formatted)
    if len(history) > max_messages:
        result = f"[...{len(history) - max_messages} more] " + result
    
    return result

def count_tokens_approx(text: str) -> int:
    """Приблизительный подсчет токенов (1 токен ≈ 4 символа для английского, 1.5 для русского)."""
    if not text:
        return 0
    
    # Простая эвристика: для русского языка ~1.5 символа на токен, для остальных ~4
    russian_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))
    other_chars = len(text) - russian_chars
    
    # Приблизительный расчет
    russian_tokens = russian_chars / 1.5
    other_tokens = other_chars / 4
    
    return int(russian_tokens + other_tokens)

def validate_base_url(url: str) -> bool:
    """Базовая валидация URL."""
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    return url.startswith(("http://", "https://")) and len(url) > 10

def extract_error_message(exception: Exception) -> str:
    """Извлечение понятного сообщения об ошибке."""
    error_str = str(exception)
    
    # Обработка типичных ошибок
    if "timeout" in error_str.lower() or "timed out" in error_str.lower():
        return "Превышено время ожидания ответа"
    elif "unauthorized" in error_str.lower() or "401" in error_str:
        return "Ошибка авторизации. Проверьте API ключ"
    elif "forbidden" in error_str.lower() or "403" in error_str:
        return "Доступ запрещен"
    elif "not found" in error_str.lower() or "404" in error_str:
        return "Эндпоинт не найден. Проверьте URL"
    elif "connection" in error_str.lower():
        return "Ошибка подключения. Проверьте доступность сервера"
    else:
        # Ограничиваем длину сообщения
        return error_str[:200] if len(error_str) > 200 else error_str

def is_valid_user_id(user_id: str) -> bool:
    """Проверка валидности user_id."""
    if not user_id or not isinstance(user_id, str):
        return False
    
    # Должен быть непустой строкой
    return len(user_id.strip()) > 0 and len(user_id) <= 255