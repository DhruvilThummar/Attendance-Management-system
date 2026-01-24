"""Lecture entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class Lecture(BaseModel):
    __table__: ClassVar[str] = 'lectures'
    timetable_id: int | None = None
    date: str | None = None  # ISO date string
