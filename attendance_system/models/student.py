"""Student entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class Student(BaseModel):
    __table__: ClassVar[str] = 'students'
    user_id: int | None = None
    enrollment_no: str | None = None
    roll_no: str | None = None
    branch: str | None = None
    phone_number: str | None = None
    mentor_name: str | None = None
    division_id: int | None = None
