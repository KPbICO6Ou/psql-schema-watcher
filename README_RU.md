# PostgreSQL Tools

Коллекция инструментов для управления базой данных PostgreSQL с мониторингом DDL событий и интеграцией Peewee ORM.

**Переводы:** [English](README.md) | [Русский](README_RU.md)

## Возможности

- **Мониторинг DDL событий** с уведомлениями в реальном времени

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
Инструмент мониторинга DDL событий в реальном времени.

**Использование:**
```bash
python3 psql-watcher.py --db default
```

**Возможности:**
- Мониторинг DDL событий (CREATE, ALTER, DROP)
- Уведомления в реальном времени через PostgreSQL NOTIFY
- Автоматическая установка и очистка триггеров
- Настраиваемый мониторинг схем

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
