"""Audit models - Track changes for compliance."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import BaseModel


class AuditTrail(BaseModel):
    """Audit trail model - tracks all attendance modifications."""

    ACTION_TYPES = {
        "CREATE": "Created",
        "UPDATE": "Updated",
        "DELETE": "Deleted",
        "APPROVE": "Approved",
        "REJECT": "Rejected",
    }

    def __init__(
        self,
        id: int | None = None,
        attendance_id: int | None = None,
        old_status_id: int | None = None,
        new_status_id: int | None = None,
        action: str = "UPDATE",
        modified_by: int | None = None,
        reason: str = "",
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.attendance_id = attendance_id
        self.old_status_id = old_status_id
        self.new_status_id = new_status_id
        self.action = action
        self.modified_by = modified_by
        self.reason = reason

    def validate(self) -> bool:
        """Validate audit trail data."""
        return bool(
            self.attendance_id
            and self.modified_by
            and self.action in self.ACTION_TYPES
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert audit trail to dictionary."""
        return {
            "id": self.id,
            "attendance_id": self.attendance_id,
            "old_status_id": self.old_status_id,
            "new_status_id": self.new_status_id,
            "action": self.action,
            "action_display": self.ACTION_TYPES.get(self.action, "Unknown"),
            "modified_by": self.modified_by,
            "reason": self.reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<AuditTrail(attendance_id={self.attendance_id}, action={self.action}, modified_by={self.modified_by})>"


class Notification(BaseModel):
    """Notification model - System notifications for users."""

    NOTIFICATION_TYPES = {
        "WARNING": "Attendance Warning",
        "ALERT": "Critical Alert",
        "INFO": "Information",
        "SUCCESS": "Success",
    }

    def __init__(
        self,
        id: int | None = None,
        user_id: int | None = None,
        title: str = "",
        message: str = "",
        notification_type: str = "INFO",
        is_read: bool = False,
        created_at: datetime | str | None = None,
        **kwargs,
    ):
        super().__init__(id=id, created_at=created_at, **kwargs)
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.is_read = is_read

    def validate(self) -> bool:
        """Validate notification data."""
        return bool(
            self.user_id
            and self.title
            and self.message
            and self.notification_type in self.NOTIFICATION_TYPES
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert notification to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "type_display": self.NOTIFICATION_TYPES.get(
                self.notification_type, "Unknown"
            ),
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Notification(user_id={self.user_id}, type={self.notification_type}, read={self.is_read})>"
