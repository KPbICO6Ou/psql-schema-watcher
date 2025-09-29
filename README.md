# PostgreSQL DDL Event Monitor

A real-time PostgreSQL DDL event monitoring tool that captures database schema changes and triggers custom actions.

**Translations:** [English](README.md) | [Русский](README_RU.md)

## Features

- **Real-time DDL Event Monitoring** - Captures CREATE, ALTER, DROP operations
- **Custom Hook System** - Execute Python scripts or shell commands on events
- **PostgreSQL Event Triggers** - Uses native PostgreSQL event trigger system
- **Automatic Cleanup** - Removes triggers and functions on exit
- **Configurable Monitoring** - Monitor specific schemas and event types
- **JSON Payload** - Rich event information in JSON format

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
Real-time DDL event monitoring tool with custom hook system.

**Usage:**
```bash
python3 psql-watcher.py --db default
```

**Features:**
- Monitors DDL events (CREATE, ALTER, DROP, CREATE INDEX, etc.)
- Real-time notifications via PostgreSQL NOTIFY
- Automatic trigger installation and cleanup
- Configurable schema monitoring
- Custom hook system for script execution
- JSON payload with rich event information

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

## Custom Hook System

The tool supports custom actions when DDL events occur:

### Python Script Hook
Create a `script.py` file with a `main(payload)` function:
```python
def main(payload):
    # payload is a JSON string with event details
    import json
    data = json.loads(payload)
    print(f"Event: {data['event']}")
    print(f"Schema: {data['schema']}")
    print(f"Object: {data['object']}")
```

### Shell Script Hook
Create a `script.sh` file that receives payload as argument:
```bash
#!/bin/bash
echo "DDL Event: $1"
# Process the JSON payload
```

The tool will automatically:
- Try to import and run `script.py` if it exists
- Try to execute `script.sh` if it exists
- Log all hook execution results

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

