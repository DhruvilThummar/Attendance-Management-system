"""Custom exception classes for the attendance system."""

from __future__ import annotations


class AttendanceSystemException(Exception):
    """Base exception for attendance system."""

    pass


class InvalidAttendanceError(AttendanceSystemException):
    """Raised when attendance data is invalid."""

    pass


class StudentNotFoundError(AttendanceSystemException):
    """Raised when student is not found."""

    pass


class FacultyNotFoundError(AttendanceSystemException):
    """Raised when faculty is not found."""

    pass


class LectureNotFoundError(AttendanceSystemException):
    """Raised when lecture is not found."""

    pass


class TimetableError(AttendanceSystemException):
    """Raised when timetable operation fails."""

    pass


class CalendarGenerationError(AttendanceSystemException):
    """Raised when lecture auto-generation fails."""

    pass


class DefaulterError(AttendanceSystemException):
    """Raised when defaulter list generation fails."""

    pass


class ReportGenerationError(AttendanceSystemException):
    """Raised when report generation fails."""

    pass


class DatabaseError(AttendanceSystemException):
    """Raised when database operation fails."""

    pass


class AuthenticationError(AttendanceSystemException):
    """Raised when authentication fails."""

    pass


class AuthorizationError(AttendanceSystemException):
    """Raised when user is not authorized."""

    pass


class NotificationError(AttendanceSystemException):
    """Raised when notification operation fails."""

    pass


class AuditError(AttendanceSystemException):
    """Raised when audit logging fails."""

    pass
