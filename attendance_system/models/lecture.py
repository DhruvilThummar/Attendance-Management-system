"""Lecture entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class Lecture(BaseModel):
    timetable_id: int | None = None
    date: str | None = None  # ISO date string
