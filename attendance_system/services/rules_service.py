"""Attendance threshold rules stub."""
from __future__ import annotations

from typing import Iterable


def compute_defaulters(records: Iterable[tuple[int, int]]) -> list[int]:
    """Return student IDs below threshold; records = (student_id, percent)."""
    threshold = 75
    return [sid for sid, pct in records if pct < threshold]
