"""Base model classes using OOP principles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class BaseModel(ABC):
    """Abstract base model with common functionality."""

    def __init__(self, id: int | None = None, created_at: datetime | None = None):
        self.id = id
        self.created_at = created_at or datetime.now()

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate model data."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class User(BaseModel):
    """User model - Base class for all users."""

    def __init__(
        self,
        id: int | None = None,
        college_id: int | None = None,
        name: str = "",
        email: str = "",
        password_hash: str = "",
        mobile: str | None = None,
        role_id: int | None = None,
        is_approved: bool = False,
        created_at: datetime | None = None,
    ):
        super().__init__(id, created_at)
        self.college_id = college_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.mobile = mobile
        self.role_id = role_id
        self.is_approved = is_approved

    def validate(self) -> bool:
        """Validate user data."""
        return bool(self.name and self.email and self.password_hash)

    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "college_id": self.college_id,
            "name": self.name,
            "email": self.email,
            "mobile": self.mobile,
            "role_id": self.role_id,
            "is_approved": self.is_approved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Role(BaseModel):
    """Role model for RBAC."""

    ROLES = {
        1: "ADMIN",
        2: "HOD",
        3: "FACULTY",
        4: "STUDENT",
        5: "PARENT",
    }

    def __init__(self, id: int | None = None, role_name: str = ""):
        super().__init__(id)
        self.role_name = role_name

    def validate(self) -> bool:
        """Validate role."""
        return self.role_name in self.ROLES.values()

    def to_dict(self) -> dict[str, Any]:
        """Convert role to dictionary."""
        return {
            "id": self.id,
            "role_name": self.role_name,
        }


class AttendanceStatus(BaseModel):
    """Attendance status model."""

    STATUSES = {
        1: "PRESENT",
        2: "ABSENT",
    }

    def __init__(self, id: int | None = None, status_name: str = ""):
        super().__init__(id)
        self.status_name = status_name

    def validate(self) -> bool:
        """Validate status."""
        return self.status_name in self.STATUSES.values()

    def to_dict(self) -> dict[str, Any]:
        """Convert status to dictionary."""
        return {
            "id": self.id,
            "status_name": self.status_name,
        }

    @property
    def is_present(self) -> bool:
        """Check if present."""
        return self.status_name == "PRESENT"
