"""Division entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class Division(BaseModel):
    __table__: ClassVar[str] = 'divisions'
    name: str | None = None
    semester: int | None = None
