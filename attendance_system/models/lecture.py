"""Lecture model - Auto-generated lectures from timetable."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import BaseModel


class Lecture(BaseModel):
    """Lecture model representing a single class session."""

    def __init__(
        self,
        id: int | None = None,
        timetable_id: int | None = None,
        lecture_date: datetime | str | None = None,
        start_time: str = "",
        end_time: str = "",
        faculty_id: int | None = None,
        subject_id: int | None = None,
        division_id: int | None = None,
        canceled: bool = False,
        created_at: datetime | str | None = None,
        created_by: int | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.timetable_id = timetable_id
        self.lecture_date = (
            datetime.fromisoformat(lecture_date)
            if isinstance(lecture_date, str)
            else lecture_date
        )
        self.start_time = start_time
        self.end_time = end_time
        self.faculty_id = faculty_id
        self.subject_id = subject_id
        self.division_id = division_id
        self.canceled = canceled
        self.created_by = created_by

    def validate(self) -> bool:
        """Validate lecture data."""
        return bool(
            self.timetable_id
            and self.lecture_date
            and self.start_time
            and self.end_time
            and self.faculty_id
            and self.subject_id
            and self.division_id
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert lecture to dictionary."""
        return {
            "id": self.id,
            "timetable_id": self.timetable_id,
            "lecture_date": (
                self.lecture_date.isoformat() if self.lecture_date else None
            ),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "faculty_id": self.faculty_id,
            "subject_id": self.subject_id,
            "division_id": self.division_id,
            "canceled": self.canceled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }

    def __repr__(self) -> str:
        return f"<Lecture(id={self.id}, date={self.lecture_date}, canceled={self.canceled})>"
