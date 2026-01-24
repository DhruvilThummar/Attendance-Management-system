"""Head of Department entity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from .base import BaseModel

@dataclass
class HOD(BaseModel):
    __table__: ClassVar[str] = 'hods'
    user_id: int | None = None
    department_id: int | None = None
