"""Timetable entry entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class TimetableEntry(BaseModel):
    subject_id: int | None = None
    faculty_id: int | None = None
    division_id: int | None = None
    day: str | None = None  # e.g. Monday
    slot: str | None = None  # e.g. 09:00-10:00
