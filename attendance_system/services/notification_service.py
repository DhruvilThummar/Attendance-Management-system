"""Notification service - Send warnings and alerts."""

from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any

from ..models.audit import Notification
from ..models.user import Student, User
from ..exceptions import NotificationError


class NotificationService:
    """Service to create and manage notifications."""

    def __init__(self):
        self.notifications: Dict[int, List[Notification]] = {}
        self.notification_queue = []

    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "INFO",
    ) -> Notification:
        """Create a new notification."""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
        )

        if not notification.validate():
            raise NotificationError("Invalid notification data")

        if user_id not in self.notifications:
            self.notifications[user_id] = []

        self.notifications[user_id].append(notification)
        return notification

    def create_attendance_warning(self, student: Student, percentage: float) -> Notification:
        """Create attendance warning notification."""
        title = "Attendance Warning"
        message = (
            f"Your attendance is {percentage:.1f}%. "
            f"Minimum required is 75%. Please improve your attendance."
        )
        return self.create_notification(
            student.id or 0,
            title,
            message,
            notification_type="WARNING",
        )

    def create_defaulter_alert(self, student: Student, percentage: float) -> Notification:
        """Create defaulter alert notification."""
        title = "Attendance Critical Alert"
        message = (
            f"Your attendance has dropped to {percentage:.1f}%. "
            f"You are below the required 75% threshold. "
            f"Contact your HOD/Faculty immediately."
        )
        return self.create_notification(
            student.id or 0,
            title,
            message,
            notification_type="ALERT",
        )

    def create_approval_notification(self, user: User, approved: bool) -> Notification:
        """Create account approval/rejection notification."""
        title = "Account Status"
        if approved:
            message = "Your account has been approved. You can now log in."
            notif_type = "SUCCESS"
        else:
            message = "Your account has been rejected. Please contact the administrator."
            notif_type = "ALERT"

        return self.create_notification(
            user.id or 0,
            title,
            message,
            notification_type=notif_type,
        )

    def get_user_notifications(
        self, user_id: int, unread_only: bool = False
    ) -> List[Notification]:
        """Get notifications for a user."""
        user_notifs = self.notifications.get(user_id, [])

        if unread_only:
            return [n for n in user_notifs if not n.is_read]

        return user_notifs

    def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read."""
        user_notifs = self.notifications.get(user_id, [])

        for notif in user_notifs:
            if notif.id == notification_id:
                notif.is_read = True
                return True

        return False

    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications for a user as read."""
        user_notifs = self.notifications.get(user_id, [])
        count = 0

        for notif in user_notifs:
            if not notif.is_read:
                notif.is_read = True
                count += 1

        return count

    def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """Delete a notification."""
        user_notifs = self.notifications.get(user_id, [])

        for i, notif in enumerate(user_notifs):
            if notif.id == notification_id:
                user_notifs.pop(i)
                return True

        return False

    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        user_notifs = self.notifications.get(user_id, [])
        return sum(1 for n in user_notifs if not n.is_read)

    def get_notification_summary(self, user_id: int) -> Dict[str, Any]:
        """Get notification summary for a user."""
        user_notifs = self.notifications.get(user_id, [])
        unread = [n for n in user_notifs if not n.is_read]

        return {
            "total": len(user_notifs),
            "unread": len(unread),
            "by_type": self._count_by_type(user_notifs),
        }

    def _count_by_type(self, notifications: List[Notification]) -> Dict[str, int]:
        """Count notifications by type."""
        counts = {}
        for notif in notifications:
            notif_type = notif.notification_type
            counts[notif_type] = counts.get(notif_type, 0) + 1
        return counts

    def broadcast_attendance_warnings(
        self, defaulters: List[tuple[Student, float]]
    ) -> int:
        """Broadcast warnings to defaulter students."""
        count = 0
        for student, percentage in defaulters:
            if percentage < 75:
                self.create_defaulter_alert(student, percentage)
            else:
                self.create_attendance_warning(student, percentage)
            count += 1
        return count
