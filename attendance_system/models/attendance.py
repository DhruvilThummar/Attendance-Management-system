"""Attendance record entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class AttendanceRecord(BaseModel):
    lecture_id: int | None = None
    student_id: int | None = None
    status: str | None = None  # P or A
