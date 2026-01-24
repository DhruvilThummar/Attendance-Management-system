"""Notification entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class Notification(BaseModel):
    __table__: ClassVar[str] = 'notifications'
    user_id: int | None = None
    message: str | None = None
    seen: bool = False
    created_at: str | None = None  # ISO timestamp
