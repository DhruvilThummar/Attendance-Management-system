"""Division entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class Division(BaseModel):
    name: str | None = None
    semester: int | None = None
