"""Initialize the database using attendance_system/schema.sql.

Usage:
  python seed_db.py

It reads DATABASE_URL from the environment (.env supported):
  mysql://user:password@host:port/dbname

Note: The database itself must already exist.
"""

from __future__ import annotations

from dotenv import load_dotenv

from attendance_system.config import Config
from attendance_system.db_manager import run_sql_file


def main() -> None:
    load_dotenv()
    cfg = Config()
    run_sql_file(cfg.SCHEMA_PATH, dsn=cfg.DATABASE_URL)
    print("OK: schema applied")


if __name__ == "__main__":
    main()
