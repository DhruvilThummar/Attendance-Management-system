"""User entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class User(BaseModel):
    email: str | None = None
    password_hash: str | None = None
    role: str | None = None  # Admin, HOD, Faculty, Student
