#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noinspection SyntaxError
"""
ONE-FILE PostgreSQL schema watcher:
- Loads .env (PG_HOST, PG_PORT, PG_USER, PG_PASSWORD, optional PG_SSLMODE)
- Args: --db (required), --schemas (default: public), --channel (default: ddl_changes), --no-ping
- Installs event triggers & functions scoped to given schemas
- LISTEN for NOTIFYs and calls run_user_hook(payload)
- On Ctrl+C/SIGTERM removes ONLY the objects it created and exits

Requires superuser to create event triggers.

Example env (.env):
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASS=password

Requirements:
pip3 install psycopg2-binary python-dotenv

Usage:
python3 psql-watcher.py --db mydb

"""
import os
import sys
import json
import uuid
import signal
import select
import argparse
import logging
from typing import List
# pip install python-dotenv psycopg2-binary
from dotenv import load_dotenv
import psycopg2
import psycopg2.extensions
from psycopg2 import sql

LOGGING = {
    'format': '%(asctime)s.%(msecs)03d [%(levelname)s]: (%(name)s.%(funcName)s) %(message)s',
    'level': logging.INFO,
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'handlers': [
        logging.StreamHandler(),
        # logging.handlers.RotatingFileHandler(filename=f'{SCRIPT_NAME}.log', maxBytes=1024 * 1024 * 10, backupCount=3),
    ],
}
logging.basicConfig(**LOGGING)
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        pass

load_dotenv('.env')

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD", "password")

STOP_FLAG = False

# language=TEXT
# noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
INSTALL_SQL = """
CREATE OR REPLACE FUNCTION {fn_changes}()
RETURNS event_trigger AS $$
DECLARE
  rec record;
  payload text;
BEGIN
  -- Log ALL events without filtering
  FOR rec IN SELECT * FROM pg_event_trigger_ddl_commands() LOOP
    payload := json_build_object(
      'event',       TG_TAG,
      'schema',      COALESCE(rec.schema_name, 'unknown'),
      'object',      COALESCE(rec.object_identity, 'unknown'),
      'object_type', COALESCE(rec.object_type, 'unknown'),
      'command_tag', TG_TAG,
      'username',    session_user,
      'txid',        txid_current(),
      'ts',          to_char(clock_timestamp(), 'YYYY-MM-DD\"T\"HH24:MI:SS.MS TZ'),
      'query',       current_query(),
      'classid',     COALESCE(rec.classid::text, 'unknown'),
      'objid',       COALESCE(rec.objid::text, 'unknown')
    )::text;
    
    -- Send notification for ALL events
    PERFORM pg_notify({channel}, payload);
  END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION {fn_drops}()
RETURNS event_trigger AS $$
DECLARE
  rec record;
  payload text;
BEGIN
  -- Log ALL DROP events without filtering
  FOR rec IN SELECT * FROM pg_event_trigger_dropped_objects() LOOP
    payload := json_build_object(
      'event',       TG_TAG,
      'schema',      COALESCE(rec.schema_name, 'unknown'),
      'object',      COALESCE(rec.object_identity, 'unknown'),
      'object_type', COALESCE(rec.object_type, 'unknown'),
      'command_tag', TG_TAG,
      'username',    session_user,
      'txid',        txid_current(),
      'ts',          to_char(clock_timestamp(), 'YYYY-MM-DD\"T\"HH24:MI:SS.MS TZ'),
      'query',       current_query()
    )::text;
    
    -- Send notification for ALL DROP events
    PERFORM pg_notify({channel}, payload);
  END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE EVENT TRIGGER {trg_ddl}
  ON ddl_command_end
  EXECUTE FUNCTION {fn_changes}();

CREATE EVENT TRIGGER {trg_drop}
  ON sql_drop
  EXECUTE FUNCTION {fn_drops}();
"""

UNINSTALL_SQL = """
DROP EVENT TRIGGER IF EXISTS {trg_ddl};
DROP EVENT TRIGGER IF EXISTS {trg_drop};
DROP FUNCTION IF EXISTS {fn_changes}();
DROP FUNCTION IF EXISTS {fn_drops}();
"""

def run_hook(payload: str) -> None:
    """
    Called for every DDL event. 'payload' is a JSON string.
    Edit this to run your custom logic.
    """
    print(f"[HOOK TRIGGERED] DDL Event detected!")
    print(f"[PAYLOAD] {payload}")
    print("-" * 50)
    # Run bash script
    # import subprocess
    # subprocess.run(["/path/to/your/script.sh", payload])

def get_conn(dbname: str):
    conn = psycopg2.connect(
        dbname=dbname,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASS,
        sslmode=os.getenv("POSTGRES_SSLMODE", "disable"),
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def install_ddl(conn, schemas: List[str], channel: str, names: dict):
    with conn.cursor() as cur:
        schema_literals = [sql.Literal(schema) for schema in schemas]
        schema_array = sql.SQL("ARRAY[{}]").format(sql.SQL(",").join(schema_literals))
        q = sql.SQL(INSTALL_SQL).format(
            fn_changes=sql.Identifier(names["fn_changes"]),
            fn_drops=sql.Identifier(names["fn_drops"]),
            trg_ddl=sql.Identifier(names["trg_ddl"]),
            trg_drop=sql.Identifier(names["trg_drop"]),
            schema_array=schema_array,
            channel=sql.Literal(channel),
        )
        cur.execute(q)

def uninstall_ddl(conn, names: dict):
    with conn.cursor() as cur:
        q = sql.SQL(UNINSTALL_SQL).format(
            fn_changes=sql.Identifier(names["fn_changes"]),
            fn_drops=sql.Identifier(names["fn_drops"]),
            trg_ddl=sql.Identifier(names["trg_ddl"]),
            trg_drop=sql.Identifier(names["trg_drop"]),
        )
        cur.execute(q)

def listen_connection(dbname: str, channel: str):
    conn = get_conn(dbname)
    with conn.cursor() as cur:
        # channels don't need pre-creation; LISTEN is enough
        cur.execute(sql.SQL("LISTEN {}").format(sql.Identifier(channel)))
    return conn

def send_ping(dbname: str, channel: str):
    payload = json.dumps({"event": "PING", "msg": "startup ping"})
    with get_conn(dbname) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pg_notify(%s, %s)", (channel, payload))

def handle_stop(signum, frame):
    global STOP_FLAG
    STOP_FLAG = True

def parse_args():
    p = argparse.ArgumentParser(description="One-file PostgreSQL schema DDL watcher (auto-install & cleanup)")
    p.add_argument("--db", required=True, help="Target database name (required)")
    p.add_argument("--schemas", default="public", help="Comma-separated schemas (default: public)")
    p.add_argument("--channel", default="ddl_changes", help="NOTIFY channel name (default: ddl_changes)")
    p.add_argument("--no-ping", action="store_true", help="Do not send startup test NOTIFY")
    return p.parse_args()

def main():
    args = parse_args()

    schemas = [s.strip() for s in args.schemas.split(",") if s.strip()]
    if not schemas:
        logging.error("[FATAL] schemas list is empty")
        sys.exit(1)

    # unique suffix to ensure precise cleanup
    suffix = uuid.uuid4().hex[:12]
    names = {
        "fn_changes": f"notify_schema_changes_{suffix}",
        "fn_drops":   f"notify_schema_drops_{suffix}",
        "trg_ddl":    f"on_schema_ddl_{suffix}",
        "trg_drop":   f"on_schema_drop_{suffix}",
    }

    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    logging.info(f"[INIT] DB={args.db} CHANNEL={args.channel} SCHEMAS={schemas}")
    logging.info(f"[INIT] Objects: {names}")

    admin_conn = None
    listen_conn = None

    try:
        print("[DEBUG] Connecting to database...")
        admin_conn = get_conn(args.db)
        print("[DEBUG] Connection successful!")

        # Best-effort pre-clean (in case of same names)
        print("[DEBUG] Removing old triggers...")
        uninstall_ddl(admin_conn, names)
        print("[DEBUG] Old triggers removed!")

        # Install objects
        print("[DEBUG] Creating new triggers...")
        install_ddl(admin_conn, schemas, args.channel, names)
        print("[DEBUG] Triggers created!")
        logging.info("[OK] Installed event triggers & functions")

        # Start listening
        listen_conn = listen_connection(args.db, args.channel)
        logging.info(f"[OK] LISTEN {args.channel}")

        if not args.no_ping:
            send_ping(args.db, args.channel)
            logging.info("[OK] Sent startup ping")

        # Event loop
        print("[WATCHER] Listening for DDL events...")
        while not STOP_FLAG:
            r, _, _ = select.select([listen_conn], [], [], 30)
            if not r:
                continue
            listen_conn.poll()
            while listen_conn.notifies:
                n = listen_conn.notifies.pop(0)
                print(f"[WATCHER] Event received on channel: {n.channel}")
                try:
                    run_hook(n.payload)
                except Exception as e:
                    print(f"[WATCHER ERROR] Hook failed: {e}")

    except psycopg2.Error as e:
        logging.error(f"[DB ERROR] {e}")
        sys.exit(2)

    finally:
        # Cleanup ONLY objects we created
        try:
            if admin_conn is None:
                admin_conn = get_conn(args.db)
            uninstall_ddl(admin_conn, names)
            logging.info("[CLEANUP] Dropped created triggers & functions")
        except Exception as e:
            logging.warning(f"[CLEANUP WARN] {e}")
        finally:
            try:
                if listen_conn is not None:
                    listen_conn.close()
            except Exception as e:
                pass
            try:
                if admin_conn is not None:
                    admin_conn.close()
            except Exception as e:
                pass
        logging.info("[BYE] stopped")

if __name__ == "__main__":
    main()
