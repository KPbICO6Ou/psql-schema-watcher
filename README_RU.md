# PostgreSQL Tools

Коллекция инструментов для управления базой данных PostgreSQL с мониторингом DDL событий и интеграцией Peewee ORM.

## Возможности

- **Настройка PostgreSQL** с Docker Compose
- **Мониторинг DDL событий** с уведомлениями в реальном времени
- **Управление базой данных** с Peewee ORM
- **Система миграций** с возможностью принудительного применения
- **Управление тестовыми данными** с примерами записей

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

### 2. Настройка базы данных

```bash
# Запустите PostgreSQL с Docker Compose
docker-compose up -d

# Проверьте, что база данных запущена
docker-compose ps
```

### 3. Базовое использование

```bash
# Создать тестовую таблицу
python3 psql-test.py --create-table

# Применить миграции
python3 psql-test.py --migrate

# Добавить тестовые данные
python3 psql-test.py --add-test-data

# Показать данные
python3 psql-test.py --show-data
```

## Обзор инструментов

### psql-test.py
Инструмент управления базой данных с интеграцией Peewee ORM.

**Доступные команды:**
- `--create-table` - Создать тестовую таблицу
- `--drop-table` - Удалить тестовую таблицу
- `--migrate` - Применить миграции
- `--force-migrate` - Принудительно применить миграции (игнорировать уже примененные)
- `--reset-migrations` - Сбросить все миграции и применить заново
- `--full-reset` - Полный сброс: удалить таблицу, миграции и создать заново
- `--add-test-data` - Добавить тестовые данные
- `--show-data` - Показать данные из таблицы

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

### Docker Compose

Файл `docker-compose.yml` настраивает базу данных PostgreSQL с:
- Доступом на `0.0.0.0:5432`
- Конфигурацией через переменные окружения
- Проверками здоровья

## Система миграций

Система миграций поддерживает:
- **Удаление колонок**: Удаляет существующие колонки
- **Добавление колонок**: Создает новые колонки
- **Принудительное применение**: Игнорирует историю миграций
- **Сброс**: Очищает историю миграций и применяет заново

### Пример рабочего процесса миграций

```bash
# 1. Создать таблицу
python3 psql-test.py --create-table

# 2. Применить миграции (удалить и добавить колонку status)
python3 psql-test.py --migrate

# 3. Добавить тестовые данные
python3 psql-test.py --add-test-data

# 4. Посмотреть результаты
python3 psql-test.py --show-data
```

## Мониторинг DDL событий

Инструмент watcher обеспечивает мониторинг изменений схемы базы данных в реальном времени:

```bash
# Начать мониторинг (в одном терминале)
python3 psql-watcher.py --db default

# Выполнить DDL операции (в другом терминале)
python3 psql-test.py --migrate
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
- Docker и Docker Compose
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
├── docker-compose.yml     # Настройка PostgreSQL
├── requirements.txt       # Python зависимости
├── psql-test.py          # Инструмент управления БД
├── psql-watcher.py       # Мониторинг DDL событий
└── .env                  # Конфигурация окружения
```

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для функции
3. Внесите изменения
4. Тщательно протестируйте
5. Отправьте pull request

## Лицензия

Этот проект с открытым исходным кодом и доступен под [лицензией MIT](LICENSE).

## Переводы

- [English](README.md)
- [Русский](README_RU.md) (текущий)

## GitHub Repository

Для получения последней версии и участия в разработке, посетите: [GitHub Repository](https://github.com/your-username/psql-tools)

Английская документация: [README.md](https://github.com/your-username/psql-tools/blob/main/README.md)
