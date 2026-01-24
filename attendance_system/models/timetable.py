"""Timetable entry entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class TimetableEntry(BaseModel):
    __table__: ClassVar[str] = 'timetable'
    subject_id: int | None = None
    faculty_id: int | None = None
    division_id: int | None = None
    day: str | None = None  # e.g. Monday
    slot: str | None = None  # e.g. 09:00-10:00
