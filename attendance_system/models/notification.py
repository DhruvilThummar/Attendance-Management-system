"""Notification entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class Notification(BaseModel):
    user_id: int | None = None
    message: str | None = None
    seen: bool = False
    created_at: str | None = None  # ISO timestamp
