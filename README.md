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