"""Subject entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class Subject(BaseModel):
    __table__: ClassVar[str] = 'subjects'
    code: str | None = None
    name: str | None = None
