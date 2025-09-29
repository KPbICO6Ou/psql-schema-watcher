# PostgreSQL Tools

A collection of PostgreSQL database management tools with DDL event monitoring and Peewee ORM integration.

**Translations:** [English](README.md) | [Русский](README_RU.md)

## Features

- **DDL Event Monitoring** with real-time notifications

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd psql-tools

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```bash
# Start DDL event monitoring
python3 psql-watcher.py --db default
```

## Tool Overview

### psql-watcher.py
Real-time DDL event monitoring tool.

**Usage:**
```bash
python3 psql-watcher.py --db default
```

**Features:**
- Monitors DDL events (CREATE, ALTER, DROP)
- Real-time notifications via PostgreSQL NOTIFY
- Automatic trigger installation and cleanup
- Configurable schema monitoring

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=default
```

## DDL Event Monitoring

The watcher tool provides real-time monitoring of database schema changes:

```bash
# Start monitoring
python3 psql-watcher.py --db default
```

**Monitored Events:**
- CREATE TABLE
- ALTER TABLE
- DROP TABLE
- CREATE INDEX
- DROP INDEX
- And more...

## Requirements

- Python 3.7+
- PostgreSQL 12+
- Virtual environment (recommended)

## Dependencies

- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variable management
- `peewee` - ORM framework
- `playhouse` - Peewee extensions

## Project Structure

```
psql-tools/
├── README.md              # English documentation
├── README_RU.md          # Russian documentation
├── requirements.txt       # Python dependencies
├── psql-watcher.py       # DDL event monitoring
└── .env                  # Environment configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

