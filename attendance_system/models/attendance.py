"""Attendance record entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class AttendanceRecord(BaseModel):
    __table__: ClassVar[str] = 'attendance'
    lecture_id: int | None = None
    student_id: int | None = None
    status: str | None = None  # P or A
