"""Notification service implementation."""
from __future__ import annotations
import logging
from typing import List
from ..models.notification import Notification

logger = logging.getLogger(__name__)

def create_notification(user_id: int, message: str) -> None:
    """Create a new notification for a user."""
    logger.info(f"Creating notification for user {user_id}: {message}")
    notif = Notification(user_id=user_id, message=message, seen=False)
    notif.save()

def get_user_notifications(user_id: int, unread_only: bool = False) -> List[Notification]:
    """Fetch notifications for a user."""
    query = f"SELECT * FROM {Notification.__table__} WHERE user_id = %s"
    if unread_only:
        query += " AND seen = FALSE"
    query += " ORDER BY created_at DESC"
    
    from ..db_manager import execute
    rows = execute(query, (user_id,))
    return [Notification(*row) for row in rows]

def mark_as_read(notification_id: int) -> None:
    """Mark a notification as seen."""
    notif = Notification.get_by_id(notification_id)
    if notif:
        notif.seen = True
        notif.save()
