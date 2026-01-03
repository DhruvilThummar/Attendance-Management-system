"""Student entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class Student(BaseModel):
    user_id: int | None = None
    enrollment_no: str | None = None
    division_id: int | None = None
