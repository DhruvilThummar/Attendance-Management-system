"""Academic structure models - Subject, Division, Department, Semester."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import BaseModel


class Subject(BaseModel):
    """Subject model - Academic subject/course."""

    def __init__(
        self,
        id: int | None = None,
        code: str = "",
        name: str = "",
        credits: int = 0,
        semester_id: int | None = None,
        dept_id: int | None = None,
        is_active: bool = True,
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.code = code
        self.name = name
        self.credits = credits
        self.semester_id = semester_id
        self.dept_id = dept_id
        self.is_active = is_active

    def validate(self) -> bool:
        """Validate subject data."""
        return bool(self.code and self.name and self.dept_id and self.credits > 0)

    def to_dict(self) -> dict[str, Any]:
        """Convert subject to dictionary."""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "credits": self.credits,
            "semester_id": self.semester_id,
            "dept_id": self.dept_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Subject(code={self.code}, name={self.name}, credits={self.credits})>"


class Division(BaseModel):
    """Division model - Class division/section."""

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


class Department(BaseModel):
    """Department model - Academic department."""

    def __init__(
        self,
        id: int | None = None,
        name: str = "",
        code: str = "",
        hod_id: int | None = None,
        is_active: bool = True,
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.name = name
        self.code = code
        self.hod_id = hod_id
        self.is_active = is_active

    def validate(self) -> bool:
        """Validate department data."""
        return bool(self.name and self.code)

    def to_dict(self) -> dict[str, Any]:
        """Convert department to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "hod_id": self.hod_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Department(name={self.name}, code={self.code})>"


class Semester(BaseModel):
    """Semester model - Academic semester."""

    def __init__(
        self,
        id: int | None = None,
        number: int = 0,
        dept_id: int | None = None,
        start_date: datetime | str | None = None,
        end_date: datetime | str | None = None,
        is_active: bool = True,
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.number = number
        self.dept_id = dept_id
        self.start_date = (
            datetime.fromisoformat(start_date)
            if isinstance(start_date, str)
            else start_date
        )
        self.end_date = (
            datetime.fromisoformat(end_date) if isinstance(end_date, str) else end_date
        )
        self.is_active = is_active

    def validate(self) -> bool:
        """Validate semester data."""
        return bool(self.number > 0 and self.dept_id and self.start_date and self.end_date)

    def to_dict(self) -> dict[str, Any]:
        """Convert semester to dictionary."""
        return {
            "id": self.id,
            "number": self.number,
            "dept_id": self.dept_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Semester(number={self.number}, dept_id={self.dept_id})>"
