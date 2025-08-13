# LLM Connector for Home Assistant

Интеграция для работы с OpenAI-совместимыми API (LM Studio, OpenAI, etc.)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

## Функциональность

- Сервис `llm_connector.ask` - отправка запросов к LLM с сохранением контекста
- Сервис `llm_connector.reset_history` - сброс истории чата
- Поддержка различных провайдеров через настраиваемый URL

## Установка через HACS

1. Откройте HACS в Home Assistant
2. Перейдите в "Интеграции"
3. Нажмите три точки в правом верхнем углу → "Пользовательские репозитории"
4. Добавьте URL: `https://github.com/KonstBessonov/ha-llm-connector`
5. Выберите тип: "Integration"
6. Нажмите "Добавить"
7. Найдите "LLM Connector" и нажмите "Установить"
8. Перезапустите Home Assistant

## Установка вручную

1. Скопируйте папку `custom_components/llm_connector` в директорию конфигурации Home Assistant
2. Перезапустите Home Assistant
3. Добавьте интеграцию через Настройки → Устройства и службы → Добавить интеграцию → LLM Connector

## Настройка

- **Base URL**: URL эндпоинта (например, `http://localhost:1234/v1`)
- **API Key**: Ключ API (опционально)
- **Model**: Модель по умолчанию (например, `gpt-3.5-turbo`)
- **Max History**: Максимальное количество сообщений в истории (0 = без ограничений)

## Использование

### Сервис ask

```yaml
service: llm_connector.ask
data:
  user_id: "123456789"
  prompt: "Какая сегодня погода?"

service: llm_connector.reset_history
data:
  user_id: "123456789"

