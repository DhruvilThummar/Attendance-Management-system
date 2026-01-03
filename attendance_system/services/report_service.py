"""Report generation stub."""
from __future__ import annotations

from pathlib import Path

from ..config import DefaultConfig


def generate_daily_report(output: Path | None = None) -> Path:
    cfg = DefaultConfig()
    out = output or Path(cfg.REPORTS_DIR) / "daily_report.pdf"
    # TODO: build PDF via ReportLab/WeasyPrint
    return out
