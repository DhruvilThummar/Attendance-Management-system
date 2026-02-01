"""Models package - Data models with OOP (Unit 9: Inheritance, Polymorphism)."""

from .base import BaseModel, User, Role, AttendanceStatus
from .user import Student, Faculty, HOD, Parent
from .lecture import Lecture
from .attendance import Attendance
from .timetable import Timetable
from .audit import AuditTrail, Notification
from .subject import Subject, Division, Department, Semester

__all__ = [
    "BaseModel",
    "User",
    "Role",
    "AttendanceStatus",
    "Student",
    "Faculty",
    "HOD",
    "Parent",
    "Lecture",
    "Attendance",
    "Timetable",
    "AuditTrail",
    "Notification",
    "Subject",
    "Division",
    "Department",
    "Semester",
]
