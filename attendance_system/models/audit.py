"""Audit trail for attendance edits."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class AttendanceAudit(BaseModel):
    attendance_id: int | None = None
    old_status: str | None = None
    new_status: str | None = None
    edited_by: int | None = None
    edited_at: str | None = None  # ISO timestamp
