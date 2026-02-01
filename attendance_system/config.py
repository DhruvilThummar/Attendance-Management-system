"""Configuration for the Attendance Management System."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """App configuration loaded from environment variables."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")

    # Expected format: mysql://user:password@host:port/dbname
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql://root:password@localhost:3306/attendance_db"
    )

    # Optional: schema file path used by seed script
    SCHEMA_PATH: str = os.getenv("SCHEMA_PATH", "attendance_system/schema.sql")
