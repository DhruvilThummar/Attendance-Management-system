"""Division model - Class section."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import BaseModel


class Division(BaseModel):
    """Division model - Class section/division."""

    def __init__(
        self,
        id: int | None = None,
        name: str = "",
        dept_id: int | None = None,
        semester_id: int | None = None,
        strength: int = 0,
        is_active: bool = True,
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.name = name
        self.dept_id = dept_id
        self.semester_id = semester_id
        self.strength = strength
        self.is_active = is_active

    def validate(self) -> bool:
        """Validate division data."""
        return bool(self.name and self.dept_id and self.strength > 0)

    def to_dict(self) -> dict[str, Any]:
        """Convert division to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "dept_id": self.dept_id,
            "semester_id": self.semester_id,
            "strength": self.strength,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Division(name={self.name}, dept_id={self.dept_id}, strength={self.strength})>"
