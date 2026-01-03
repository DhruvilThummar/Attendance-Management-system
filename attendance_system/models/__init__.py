"""Data-only models for the attendance system."""
from .base import BaseModel
from .user import User
from .student import Student
from .faculty import Faculty
from .hod import HOD
from .subject import Subject
from .division import Division
from .timetable import TimetableEntry
from .lecture import Lecture
from .attendance import AttendanceRecord
from .audit import AttendanceAudit
from .notification import Notification

__all__ = [
    "BaseModel",
    "User",
    "Student",
    "Faculty",
    "HOD",
    "Subject",
    "Division",
    "TimetableEntry",
    "Lecture",
    "AttendanceRecord",
    "AttendanceAudit",
    "Notification",
]
