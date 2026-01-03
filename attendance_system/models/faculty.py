"""Faculty entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class Faculty(BaseModel):
    user_id: int | None = None
    department: str | None = None
