# PostgreSQL DDL Event Monitor

Инструмент мониторинга DDL событий PostgreSQL в реальном времени, который отслеживает изменения схемы базы данных и запускает пользовательские действия.

**Переводы:** [English](README.md) | [Русский](README_RU.md)

## Возможности

- **Мониторинг DDL событий в реальном времени** - Отслеживает операции CREATE, ALTER, DROP
- **Система пользовательских хуков** - Выполнение Python скриптов или shell команд при событиях
- **PostgreSQL Event Triggers** - Использует нативную систему event triggers PostgreSQL
- **Автоматическая очистка** - Удаляет триггеры и функции при выходе
- **Настраиваемый мониторинг** - Мониторинг конкретных схем и типов событий
- **JSON Payload** - Богатая информация о событиях в формате JSON

## Быстрый старт

### 1. Настройка окружения

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd psql-tools

# Создайте виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Базовое использование

```bash
# Запустить мониторинг DDL событий
python3 psql-watcher.py --db default
```

## Обзор инструмента

### psql-watcher.py
Инструмент мониторинга DDL событий в реальном времени с системой пользовательских хуков.

**Использование:**
```bash
python3 psql-watcher.py --db default
```

**Возможности:**
- Мониторинг DDL событий (CREATE, ALTER, DROP, CREATE INDEX и др.)
- Уведомления в реальном времени через PostgreSQL NOTIFY
- Автоматическая установка и очистка триггеров
- Настраиваемый мониторинг схем
- Система пользовательских хуков для выполнения скриптов
- JSON payload с богатой информацией о событиях

## Конфигурация

### Переменные окружения

Создайте файл `.env` со следующими переменными:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=default
```

## Мониторинг DDL событий

Инструмент watcher обеспечивает мониторинг изменений схемы базы данных в реальном времени:

```bash
# Начать мониторинг
python3 psql-watcher.py --db default
```

**Отслеживаемые события:**
- CREATE TABLE
- ALTER TABLE
- DROP TABLE
- CREATE INDEX
- DROP INDEX
- И другие...

## Система пользовательских хуков

Инструмент поддерживает пользовательские действия при возникновении DDL событий:

### Python Script Hook
Создайте файл `script.py` с функцией `main(payload)`:
```python
def main(payload):
    # payload - это JSON строка с деталями события
    import json
    data = json.loads(payload)
    print(f"Событие: {data['event']}")
    print(f"Схема: {data['schema']}")
    print(f"Объект: {data['object']}")
```

### Shell Script Hook
Создайте файл `script.sh`, который получает payload как аргумент:
```bash
#!/bin/bash
echo "DDL Событие: $1"
# Обработать JSON payload
```

Инструмент автоматически:
- Попытается импортировать и запустить `script.py` если он существует
- Попытается выполнить `script.sh` если он существует
- Запишет результаты выполнения всех хуков в лог

## Требования

- Python 3.7+
- PostgreSQL 12+
- Виртуальное окружение (рекомендуется)

## Зависимости

- `psycopg2-binary` - Адаптер PostgreSQL
- `python-dotenv` - Управление переменными окружения
- `peewee` - ORM фреймворк
- `playhouse` - Расширения Peewee

## Структура проекта

```
psql-tools/
├── README.md              # Документация на английском
├── README_RU.md          # Документация на русском
├── requirements.txt       # Python зависимости
├── psql-watcher.py       # Мониторинг DDL событий
└── .env                  # Конфигурация окружения
```

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для функции
3. Внесите изменения
4. Тщательно протестируйте
5. Отправьте pull request
