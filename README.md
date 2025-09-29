# PostgreSQL Tools

A collection of PostgreSQL database management tools with DDL event monitoring and Peewee ORM integration.

## Features

- **PostgreSQL Database Setup** with Docker Compose
- **DDL Event Monitoring** with real-time notifications
- **Database Management** with Peewee ORM
- **Migration System** with force apply capabilities
- **Test Data Management** with sample records

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

### 2. Database Setup

```bash
# Start PostgreSQL with Docker Compose
docker-compose up -d

# Check if database is running
docker-compose ps
```

### 3. Basic Usage

```bash
# Create test table
python3 psql-test.py --create-table

# Apply migrations
python3 psql-test.py --migrate

# Add test data
python3 psql-test.py --add-test-data

# Show data
python3 psql-test.py --show-data
```

## Tools Overview

### psql-test.py
Database management tool with Peewee ORM integration.

**Available Commands:**
- `--create-table` - Create test table
- `--drop-table` - Drop test table
- `--migrate` - Apply migrations
- `--force-migrate` - Force apply migrations (ignore already applied)
- `--reset-migrations` - Reset all migrations and reapply
- `--full-reset` - Full reset: drop table, migrations and recreate
- `--add-test-data` - Add test data
- `--show-data` - Show data from table

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

### Docker Compose

The `docker-compose.yml` file sets up a PostgreSQL database with:
- Exposed on `0.0.0.0:5432`
- Environment variable configuration
- Health checks

## Migration System

The migration system supports:
- **Drop Column**: Removes existing columns
- **Add Column**: Creates new columns
- **Force Apply**: Ignores migration history
- **Reset**: Clears migration history and reapplies

### Example Migration Workflow

```bash
# 1. Create table
python3 psql-test.py --create-table

# 2. Apply migrations (drop and add status column)
python3 psql-test.py --migrate

# 3. Add test data
python3 psql-test.py --add-test-data

# 4. View results
python3 psql-test.py --show-data
```

## DDL Event Monitoring

The watcher tool provides real-time monitoring of database schema changes:

```bash
# Start monitoring (in one terminal)
python3 psql-watcher.py --db default

# Perform DDL operations (in another terminal)
python3 psql-test.py --migrate
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
- Docker and Docker Compose
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
├── docker-compose.yml     # PostgreSQL setup
├── requirements.txt       # Python dependencies
├── psql-test.py          # Database management tool
├── psql-watcher.py       # DDL event monitoring
└── .env                  # Environment configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Translations

- [English](README.md) (current)
- [Русский](README_RU.md)

## GitHub Repository

For the latest version and to contribute, visit: [GitHub Repository](https://github.com/your-username/psql-tools)

Russian documentation: [README_RU.md](https://github.com/your-username/psql-tools/blob/main/README_RU.md)
