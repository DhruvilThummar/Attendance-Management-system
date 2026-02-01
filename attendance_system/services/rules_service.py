"""Attendance rules service - Enforce attendance policies."""

from __future__ import annotations

from typing import List, Tuple, Dict, Any

from ..models.user import Student
from ..models.attendance import Attendance
from ..exceptions import DefaulterError, InvalidAttendanceError


class AttendanceRulesService:
    """Service to enforce attendance rules and generate defaulter lists."""

    MIN_ATTENDANCE_PERCENTAGE = 75  # 75% minimum attendance required

    def __init__(self):
        self.attendance_records: Dict[int, List[Attendance]] = {}

    def add_attendance_record(self, student_id: int, attendance: Attendance) -> None:
        """Add attendance record for a student."""
        if student_id not in self.attendance_records:
            self.attendance_records[student_id] = []
        self.attendance_records[student_id].append(attendance)

    def get_attendance_percentage(self, student_id: int) -> float:
        """Calculate attendance percentage for a student."""
        if student_id not in self.attendance_records:
            return 0.0

        records = self.attendance_records[student_id]
        if not records:
            return 0.0

        present_count = sum(1 for r in records if r.is_present)
        total_count = len(records)

        return (present_count / total_count * 100) if total_count > 0 else 0.0

    def is_defaulter(self, student_id: int) -> bool:
        """Check if student is a defaulter (attendance < 75%)."""
        percentage = self.get_attendance_percentage(student_id)
        return percentage < self.MIN_ATTENDANCE_PERCENTAGE

    def get_defaulters(self, students: List[Student]) -> List[Tuple[Student, float]]:
        """Get list of defaulter students with their attendance percentages."""
        defaulters = []
        for student in students:
            if self.is_defaulter(student.id):
                percentage = self.get_attendance_percentage(student.id)
                defaulters.append((student, percentage))
        return defaulters

    def get_students_needing_warning(self, students: List[Student], warning_threshold: int = 80) -> List[Tuple[Student, float]]:
        """Get students whose attendance is below warning threshold but > 75%."""
        warning_list = []
        for student in students:
            percentage = self.get_attendance_percentage(student.id)
            if self.MIN_ATTENDANCE_PERCENTAGE <= percentage < warning_threshold:
                warning_list.append((student, percentage))
        return warning_list

    def validate_attendance(self, student_id: int, attendance: Attendance) -> bool:
        """Validate attendance record."""
        if not attendance.validate():
            raise InvalidAttendanceError("Invalid attendance record")

        if student_id != attendance.student_id:
            raise InvalidAttendanceError("Student ID mismatch")

        return True

    def get_attendance_summary(self, student_id: int) -> Dict[str, Any]:
        """Get comprehensive attendance summary for a student."""
        records = self.attendance_records.get(student_id, [])

        if not records:
            return {
                "student_id": student_id,
                "total_lectures": 0,
                "present": 0,
                "absent": 0,
                "percentage": 0.0,
                "is_defaulter": False,
                "status": "No records",
            }

        present = sum(1 for r in records if r.is_present)
        absent = sum(1 for r in records if not r.is_present)
        total = len(records)
        percentage = (present / total * 100) if total > 0 else 0.0

        return {
            "student_id": student_id,
            "total_lectures": total,
            "present": present,
            "absent": absent,
            "percentage": round(percentage, 2),
            "is_defaulter": percentage < self.MIN_ATTENDANCE_PERCENTAGE,
            "status": "Defaulter" if percentage < self.MIN_ATTENDANCE_PERCENTAGE else "Regular",
        }

    def bulk_get_attendance_summaries(
        self, student_ids: List[int]
    ) -> Dict[int, Dict[str, Any]]:
        """Get attendance summaries for multiple students."""
        return {
            student_id: self.get_attendance_summary(student_id)
            for student_id in student_ids
        }

    def reset_records(self, student_id: int | None = None) -> None:
        """Reset attendance records for a student or all students."""
        if student_id:
            self.attendance_records.pop(student_id, None)
        else:
            self.attendance_records.clear()
