#!/bin/bash

# Скрипт для создания структуры проекта LLM Connector

echo "🚀 Создание структуры проекта LLM Connector..."

# Создание основных директорий
mkdir -p custom_components/llm_connector
mkdir -p tests
mkdir -p hass_config

# Создание файлов структуры
touch custom_components/llm_connector/__init__.py
touch custom_components/llm_connector/config_flow.py
touch custom_components/llm_connector/const.py
touch custom_components/llm_connector/manifest.json
touch custom_components/llm_connector/services.yaml
touch custom_components/llm_connector/chat_manager.py
touch custom_components/llm_connector/llm_client.py
touch custom_components/llm_connector/services.py
touch custom_components/llm_connector/utils.py

# Создание тестовых файлов
touch tests/__init__.py
touch tests/test_chat_manager.py
touch tests/test_llm_client.py

# Создание .gitignore
cat > .gitignore << EOF
venv/
__pycache__/
*.pyc
.pytest_cache/
.hass*
.DS_Store
Thumbs.db
EOF

# Создание README.md
cat > README.md << EOF
# LLM Connector for Home Assistant

Интеграция для работы с OpenAI-совместимыми API (LM Studio, OpenAI, etc.)

## Функциональность

- Сервис \`llm_connector.ask\` - отправка запросов к LLM с сохранением контекста
- Сервис \`llm_connector.reset_history\` - сброс истории чата
- Поддержка различных провайдеров через настраиваемый URL

## Установка

1. Скопируйте папку \`custom_components/llm_connector\` в директорию конфигурации Home Assistant
2. Перезапустите Home Assistant
3. Добавьте интеграцию через Настройки → Устройства и службы → Добавить интеграцию → LLM Connector

## Настройка

- **Base URL**: URL эндпоинта (например, \`http://localhost:1234/v1\`)
- **API Key**: Ключ API (опционально)
- **Model**: Модель по умолчанию (например, \`gpt-3.5-turbo\`)
- **Max History**: Максимальное количество сообщений в истории (0 = без ограничений)
EOF

# Создание requirements.txt
cat > requirements.txt << EOF
homeassistant>=2023.0.0
aiohttp>=3.8.0
voluptuous>=0.13.0
pytest>=7.0.0
respx>=0.20.0
EOF

# Создание setup.py для удобства установки
cat > setup.py << EOF
from setuptools import setup, find_packages

setup(
    name="llm-connector",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "homeassistant>=2023.0.0",
        "aiohttp>=3.8.0",
        "voluptuous>=0.13.0",
    ],
)
EOF

echo "✅ Структура проекта создана!"
echo ""
echo "Следующие шаги:"
echo "1. source venv/bin/activate  # если используете виртуальное окружение"
echo "2. pip install -r requirements.txt"
echo "3. Начните разработку в custom_components/llm_connector/"
echo ""
echo "Структура проекта:"
echo "├── custom_components/"
echo "│   └── llm_connector/"
echo "├── tests/"
echo "├── hass_config/"
echo "├── README.md"
echo "├── requirements.txt"
echo "└── .gitignore"