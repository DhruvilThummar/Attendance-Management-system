"""Default configuration for the attendance system."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class DefaultConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/attendance_db"
    )
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "attendance_system/static/reports")
    BACKUP_DIR: str = os.getenv("BACKUP_DIR", "attendance_system/static/reports/backups")
