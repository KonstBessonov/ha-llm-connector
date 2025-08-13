# LLM Connector for Home Assistant

Интеграция для работы с OpenAI-совместимыми API (LM Studio, OpenAI, etc.)

## Функциональность

- Сервис `llm_connector.ask` - отправка запросов к LLM с сохранением контекста
- Сервис `llm_connector.reset_history` - сброс истории чата
- Поддержка различных провайдеров через настраиваемый URL

## Установка

1. Скопируйте папку `custom_components/llm_connector` в директорию конфигурации Home Assistant
2. Перезапустите Home Assistant
3. Добавьте интеграцию через Настройки → Устройства и службы → Добавить интеграцию → LLM Connector

## Настройка

- **Base URL**: URL эндпоинта (например, `http://localhost:1234/v1`)
- **API Key**: Ключ API (опционально)
- **Model**: Модель по умолчанию (например, `gpt-3.5-turbo`)
- **Max History**: Максимальное количество сообщений в истории (0 = без ограничений)
