"""
Models package for Attendance Management System
"""

from .user import User, Role
from .college import College
from .department import Department
from .division import Division
from .faculty import Faculty
from .student import Student
from .parent import Parent
from .subject import Subject, Semester
from .timetable import Timetable
from .lecture import Lecture
from .attendance import Attendance, AttendanceStatus
from .academic_calendar import AcademicCalendar
from .proxy_lecture import ProxyLecture

__all__ = [
    'User',
    'Role',
    'College',
    'Department',
    'Division',
    'Faculty',
    'Student',
    'Parent',
    'Subject',
    'Semester',
    'Timetable',
    'Lecture',
    'Attendance',
    'AttendanceStatus',
    'AcademicCalendar',
    'ProxyLecture',
]
