"""Attendance marking and audit stub."""
from __future__ import annotations

from typing import Iterable

from ..db_manager import execute


def mark_attendance(lecture_id: int, student_statuses: Iterable[tuple[int, str]]) -> None:
    # TODO: insert/update attendance rows and write audits
    _ = (lecture_id, student_statuses, execute)
    raise NotImplementedError
