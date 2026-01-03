"""Head of Department entity."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModel


@dataclass
class HOD(BaseModel):
    user_id: int | None = None
    department_id: int | None = None
