"""User entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class User(BaseModel):
    __table__: ClassVar[str] = 'users'
    college_id: int | None = None
    email: str | None = None
    name: str | None = None
    password: str | None = None
    role: str | None = None  # Admin, HOD, Faculty, Student
    is_approved: bool | None = False
