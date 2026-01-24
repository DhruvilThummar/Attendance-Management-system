"""Faculty entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class Faculty(BaseModel):
    __table__: ClassVar[str] = 'faculties'
    user_id: int | None = None
    department: str | None = None
    short_name: str | None = None
    phone_number: str | None = None
