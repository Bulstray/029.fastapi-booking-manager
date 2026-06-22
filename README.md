[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TaskIQ](https://img.shields.io/badge/TaskIQ-0.14+-FF6B6B?style=for-the-badge&logo=task&logoColor=white)](https://taskiq-python.github.io/)
[![Redis](https://img.shields.io/badge/Redis-7+-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.14+-000000?style=for-the-badge&logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0+-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/Ruff-0.6+-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

# Booking Service - Backend для записи на встречи

Сервис для управления бронированиями с асинхронной фоновой обработкой через очередь задач.


## 🏗 Стек технологий

| Компонент     | Технология |
|---------------|---------|
| Backend       | Python  |
| Web Framework |    FastAPI|
| Task Queue   | TaskIQ|
| Queue Broker | Redis|
|Database| PostgreSQL|
|ORM| 	SQLAlchemy 2.0+|
|Migrations | Alembic|
| Validation | Pydantic|
| Testing | Pytest|
| Containerization| Docker Compose|
| Code Quality| Ruff, mypy|


#### В задании допускался Celery, но TaskIQ дает более чистую интеграцию с async-кодом и лучше ложится на архитектуру FastAPI.

### Почему FastAPI?

 - Встроенная поддержка асинхронности (async/await)
 - Автоматическая генерация OpenAPI документации 
 - Встроенная валидация через Pydantic

### Почему TaskIQ вместо Celery?
 - Нативная поддержка asyncio (не требуется asyncio.run())
 - Проще интеграция с FastAPI (оба используют async)
 - Лучше подходит для современного async-стека 
 - Меньше зависимостей и проще конфигурация


## 🚀 Быстрый старт

Если сначала запускали тесты, то убедитесь, что переменные окружения удалены


1. Клонирование
```bash
https://github.com/Bulstray/029.fastapi-booking-manager.git
```
2. Установка зависимостей (Если uv не установлен, то нужно установить сначала pipx, а потом через него uv)
```bash
uv sync
```

2. Переход в рабочую папку
```bash
cd booking-catalog
```

3. Создание .env файла по примеру .env.template
4. Поднять докер

```bash
docker-compose up
```
5. Запуск
```bash
uv run main.py 
```

## 🧪 Тестирование

1. Клонирование
```bash
https://github.com/Bulstray/029.fastapi-booking-manager.git
```
2. Установка зависимостей (Если uv не установлен, то нужно установить сначала pipx, а потом через него uv)
```bash
uv sync
```
3. Переход в рабочую папку
```bash
cd booking-catalog
```
4. Создание .env файла по примеру .env.template
5. Настройка переменной окружения
```bash
$env:APP_CONFIG__DB__URL="sqlite+aiosqlite:///:memory:"
```
6. Запуск тестов
```bash
pytest
```