"""Subject entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class Subject(BaseModel):
    code: str | None = None
    name: str | None = None
