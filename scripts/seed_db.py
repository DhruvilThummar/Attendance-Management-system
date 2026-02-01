"""Seed database with sample data (legacy entrypoint).

This project uses MySQL. Prefer running the root-level `seed_db.py`, which
creates tables from `attendance_system/schema.sql` and seeds initial data.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

from attendance_system.db_manager import init_db_pool


def main():
    load_dotenv()
    init_db_pool(os.getenv("DATABASE_URL", ""))
    print("Database connection OK. Run the root-level seed_db.py to seed data.")


if __name__ == "__main__":
    main()
