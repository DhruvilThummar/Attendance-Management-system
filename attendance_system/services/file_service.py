"""File handling and backups stub."""
from __future__ import annotations

from pathlib import Path
import shutil

from ..config import DefaultConfig


def backup_reports() -> Path:
    cfg = DefaultConfig()
    src = Path(cfg.REPORTS_DIR)
    dst = Path(cfg.BACKUP_DIR)
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.glob("*.pdf"):
        shutil.copy(item, dst / item.name)
    return dst
