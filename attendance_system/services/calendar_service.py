"""Lecture auto-generation stub."""
from __future__ import annotations

from datetime import date
from typing import Iterable

from ..db_manager import execute


def generate_lectures(timetable_ids: Iterable[int], start: date, end: date) -> None:
    # TODO: create lecture rows for working days
    _ = (timetable_ids, start, end, execute)
    raise NotImplementedError
