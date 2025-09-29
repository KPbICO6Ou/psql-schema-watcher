#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peewee ORM Database Manager - Separate Functions
- Create single table
- Drop table
- Migrations
- Add test data

Requirements:
pip install peewee psycopg2-binary python-dotenv

Usage:
python3 psql-test.py --create-table
python3 psql-test.py --drop-table
python3 psql-test.py --migrate
python3 psql-test.py --add-test-data
python3 psql-test.py --show-data
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import List, Optional

# pip install peewee psycopg2-binary python-dotenv
from dotenv import load_dotenv
from peewee import *
from playhouse.migrate import *

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        pass

load_dotenv('.env')


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', '5432')),
    'database': os.getenv('POSTGRES_DB', 'default'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
}
# Create database connection
DATABASE = PostgresqlDatabase(
    DATABASE_CONFIG['database'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password'],
    host=DATABASE_CONFIG['host'],
    port=DATABASE_CONFIG['port'],
    autocommit=True
)

# Models
class BaseModel(Model):
    """Base model"""
    class Meta:
        database = DATABASE

class TestTable(BaseModel):
    """Test table"""
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False)
    email = CharField(max_length=255, null=True)
    age = IntegerField(null=True)
    is_active = BooleanField(default=True)
    status = CharField(max_length=50, null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'test_table'

class Migration(BaseModel):
    """Table for tracking migrations"""
    id = AutoField(primary_key=True)
    name = CharField(max_length=255, unique=True)
    applied_at = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'migrations'

# Function 1: Create table
def create_table():
    """Creates test table"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        DATABASE.create_tables([TestTable], safe=True)
        logger.info("Table test_table created successfully")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Function 2: Drop table
def drop_table():
    """Drops test table"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        DATABASE.drop_tables([TestTable], safe=True)
        logger.info("Table test_table dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping table: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Function 3: Create migrations table
def create_migration_table():
    """Creates migrations table"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        DATABASE.create_tables([Migration], safe=True)
        logger.info("Migrations table created/verified")
    except Exception as e:
        logger.error(f"Error creating migrations table: {e}")
        raise

# Function 4: Apply migrations
def apply_migrations():
    """Applies all migrations"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        
        # Create migrations table if it doesn't exist
        create_migration_table()

        # Migration 1: FORCE drop status column (if exists)
        try:
            # Check if column exists
            with DATABASE.cursor() as cursor:
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'test_table' AND column_name = 'status'
                """)
                if cursor.fetchone():
                    migrator = PostgresqlMigrator(DATABASE)
                    migrate(
                        migrator.drop_column('test_table', 'status')
                    )
                    logger.info("Migration: dropped column status")
                else:
                    logger.info("Column status does not exist, skipping drop")
        except Exception as e:
            logger.warning(f"Error checking/dropping column status: {e}")
        
        # Migration 2: FORCE create status column
        try:
            migrator = PostgresqlMigrator(DATABASE)
            migrate(
                migrator.add_column('test_table', 'status', CharField(max_length=50, default='active'))
            )
            logger.info("Migration: added column status")
        except Exception as e:
            logger.warning(f"Error creating column status: {e}")
            
    except Exception as e:
        logger.error(f"Error applying migrations: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Function 5: Add test data
def add_test_data():
    """Adds test data to table"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        
        # Check if table exists
        if not DATABASE.table_exists('test_table'):
            logger.error("Table test_table does not exist. Create table first.")
            return
        
        # Test data
        test_data = [
            {
                'name': 'John Smith',
                'email': 'ivan@example.com',
                'age': 25,
                'phone': '+7-123-456-7890',
                'status': 'active'
            },
            {
                'name': 'Maria Johnson',
                'email': 'maria@example.com',
                'age': 30,
                'phone': '+7-987-654-3210',
                'status': 'pending'
            },
            {
                'name': 'Alex Brown',
                'email': 'alex@example.com',
                'age': 28,
                'phone': '+7-555-123-4567',
                'status': 'inactive'
            },
            {
                'name': 'Elena Davis',
                'email': 'elena@example.com',
                'age': 35,
                'phone': '+7-111-222-3333',
                'status': 'active'
            },
            {
                'name': 'Dmitry Wilson',
                'email': 'dmitry@example.com',
                'age': 42,
                'phone': '+7-444-555-6666',
                'status': 'pending'
            }
        ]
        
        # Add data
        for data in test_data:
            TestTable.create(**data)
        
        logger.info(f"Added {len(test_data)} test records")
        
    except Exception as e:
        logger.error(f"Error adding test data: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Function 6: Show data
def show_data():
    """Shows data from table"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        
        if not DATABASE.table_exists('test_table'):
            logger.error("Table test_table does not exist")
            return
        
        records = TestTable.select()
        count = records.count()
        
        if count == 0:
            logger.info("Table is empty")
            return
        
        logger.info(f"Found {count} records:")
        logger.info("-" * 80)
        
        for record in records:
            logger.info(f"ID: {record.id:3d} | Name: {record.name:20s} | Email: {record.email:20s} | "
                       f"Age: {record.age:2d} | Phone: {getattr(record, 'phone', 'N/A'):15s} | "
                       f"Status: {getattr(record, 'status', 'N/A'):10s}")
        
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Function 7: Force apply migrations
def force_apply_migrations():
    """Force applies all migrations, ignoring already applied ones"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        
        # Create migrations table if it doesn't exist
        create_migration_table()
        
        # Remove old migration records
        Migration.delete().where(Migration.name.in_([
            'drop_status_column', 'add_status_column'
        ])).execute()
        logger.info("Removed old migration records")
        
        # Force apply migrations
        logger.info("Force applying migrations...")
        
        # Migration 1: FORCE drop status column (if exists)
        try:
            # Check if column exists
            with DATABASE.cursor() as cursor:
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'test_table' AND column_name = 'status'
                """)
                if cursor.fetchone():
                    migrator = PostgresqlMigrator(DATABASE)
                    migrate(
                        migrator.drop_column('test_table', 'status')
                    )
                    logger.info("Migration: dropped column status")
                else:
                    logger.info("Column status does not exist, skipping drop")
        except Exception as e:
            logger.warning(f"Error checking/dropping column status: {e}")
        
        # Migration 2: FORCE create status column
        try:
            migrator = PostgresqlMigrator(DATABASE)
            migrate(
                migrator.add_column('test_table', 'status', CharField(max_length=50, default='active'))
            )
            logger.info("Migration: added column status")
        except Exception as e:
            logger.warning(f"Error creating column status: {e}")
            
    except Exception as e:
        logger.error(f"Error force applying migrations: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Function 8: Reset migrations
def reset_migrations():
    """Resets all migrations and reapplies them"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        
        # Create migrations table if it doesn't exist
        create_migration_table()
        
        # Remove ALL migration records
        Migration.delete().execute()
        logger.info("Removed ALL migration records")
        
        # Reapply migrations
        logger.info("Reapplying migrations...")
        apply_migrations()
            
    except Exception as e:
        logger.error(f"Error resetting migrations: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Function 9: Full reset
def full_reset():
    """Full reset: drops table, migrations and recreates everything"""
    try:
        if DATABASE.is_closed():
            DATABASE.connect()
        
        logger.info("Starting full reset...")
        
        # 1. Drop test_table
        try:
            DATABASE.drop_tables([TestTable], safe=True)
            logger.info("Table test_table dropped")
        except Exception as e:
            logger.warning(f"Error dropping table: {e}")
        
        # 2. Remove all migrations
        try:
            Migration.delete().execute()
            logger.info("All migrations removed")
        except Exception as e:
            logger.warning(f"Error removing migrations: {e}")
        
        # 3. Recreate table
        DATABASE.create_tables([TestTable], safe=True)
        logger.info("Table test_table recreated")
        
        # 4. Apply migrations
        logger.info("Applying migrations...")
        apply_migrations()
        
        logger.info("Full reset completed successfully!")
            
    except Exception as e:
        logger.error(f"Error during full reset: {e}")
        raise
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Peewee ORM Database Manager - Separate Functions')
    
    # Main operations (mutually exclusive)
    main_group = parser.add_mutually_exclusive_group(required=True)
    main_group.add_argument('--create-table', action='store_true',
                          help='Create test table')
    main_group.add_argument('--drop-table', action='store_true',
                          help='Drop test table')
    main_group.add_argument('--migrate', action='store_true',
                          help='Apply migrations')
    main_group.add_argument('--force-migrate', action='store_true',
                          help='Force apply migrations (ignore already applied)')
    main_group.add_argument('--reset-migrations', action='store_true',
                          help='Reset all migrations and reapply')
    main_group.add_argument('--full-reset', action='store_true',
                          help='Full reset: drop table, migrations and recreate')
    main_group.add_argument('--add-test-data', action='store_true',
                          help='Add test data')
    main_group.add_argument('--show-data', action='store_true',
                          help='Show data from table')
    
    args = parser.parse_args()
    
    try:
        logger.info(f"Connecting to database: {DATABASE_CONFIG['database']}")
        
        # Execute selected operation
        if args.create_table:
            create_table()
        elif args.drop_table:
            drop_table()
        elif args.migrate:
            apply_migrations()
        elif args.force_migrate:
            force_apply_migrations()
        elif args.reset_migrations:
            reset_migrations()
        elif args.full_reset:
            full_reset()
        elif args.add_test_data:
            add_test_data()
        elif args.show_data:
            show_data()
        
    except Exception as e:
        logger.error(f"Error executing operation: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()