"""Notification stub."""
from __future__ import annotations

from ..db_manager import execute


def create_notification(user_id: int, message: str) -> None:
    _ = (user_id, message, execute)
    raise NotImplementedError
