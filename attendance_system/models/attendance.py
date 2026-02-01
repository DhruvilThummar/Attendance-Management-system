"""Attendance model - Student attendance records."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import BaseModel


class Attendance(BaseModel):
    """Attendance model tracking student attendance for lectures."""

    def __init__(
        self,
        id: int | None = None,
        student_id: int | None = None,
        lecture_id: int | None = None,
        attendance_status_id: int | None = None,
        marked_by: int | None = None,
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.student_id = student_id
        self.lecture_id = lecture_id
        self.attendance_status_id = attendance_status_id  # 1=Present, 2=Absent
        self.marked_by = marked_by

    def validate(self) -> bool:
        """Validate attendance data."""
        return bool(
            self.student_id
            and self.lecture_id
            and self.attendance_status_id
            and self.marked_by
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert attendance to dictionary."""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "lecture_id": self.lecture_id,
            "attendance_status_id": self.attendance_status_id,
            "marked_by": self.marked_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        status_str = "Present" if self.attendance_status_id == 1 else "Absent"
        return f"<Attendance(student_id={self.student_id}, lecture_id={self.lecture_id}, status={status_str})>"

    @property
    def is_present(self) -> bool:
        """Check if student was present."""
        return self.attendance_status_id == 1
