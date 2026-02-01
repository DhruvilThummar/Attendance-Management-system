"""Timetable model - Weekly class schedules for divisions."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import BaseModel


class Timetable(BaseModel):
    """Timetable model defining class schedule."""

    DAYS_OF_WEEK = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    }

    def __init__(
        self,
        id: int | None = None,
        division_id: int | None = None,
        subject_id: int | None = None,
        faculty_id: int | None = None,
        day_of_week: int | None = None,  # 1=Monday to 6=Saturday
        start_time: str = "",
        end_time: str = "",
        semester_id: int | None = None,
        is_active: bool = True,
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.division_id = division_id
        self.subject_id = subject_id
        self.faculty_id = faculty_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.semester_id = semester_id
        self.is_active = is_active

    def validate(self) -> bool:
        """Validate timetable data."""
        return bool(
            self.division_id
            and self.subject_id
            and self.faculty_id
            and 1 <= (self.day_of_week or 0) <= 6
            and self.start_time
            and self.end_time
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert timetable to dictionary."""
        return {
            "id": self.id,
            "division_id": self.division_id,
            "subject_id": self.subject_id,
            "faculty_id": self.faculty_id,
            "day_of_week": self.day_of_week,
            "day_name": self.DAYS_OF_WEEK.get(self.day_of_week, "Unknown"),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "semester_id": self.semester_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        day_name = self.DAYS_OF_WEEK.get(self.day_of_week, "Unknown")
        return f"<Timetable(division_id={self.division_id}, day={day_name}, time={self.start_time}-{self.end_time})>"

    @property
    def day_name(self) -> str:
        """Get day name from day_of_week."""
        return self.DAYS_OF_WEEK.get(self.day_of_week, "Unknown")
