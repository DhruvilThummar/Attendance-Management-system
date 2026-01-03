"""Seed database with sample data (placeholder)."""
from __future__ import annotations

from attendance_system.db_manager import execute, init_db_pool


def main():
    init_db_pool("postgresql://user:password@localhost:5432/attendance_db")
    _ = execute  # TODO: insert seed rows


if __name__ == "__main__":
    main()
