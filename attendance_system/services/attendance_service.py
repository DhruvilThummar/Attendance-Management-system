"""
Attendance Management Service
=============================

Handles all attendance-related operations:
- Mark attendance for lectures
- Edit existing attendance records
- Calculate attendance percentages
- Generate attendance reports
- Get attendance for specific students

Author: Development Team
Version: 1.0
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ..db_manager import get_cursor, fetch_all, fetch_one


class AttendanceService:
    """
    Service for managing attendance operations.
    
    Methods:
    - mark_attendance: Mark attendance for a student in a lecture
    - edit_attendance: Edit existing attendance record
    - get_student_attendance: Get attendance records for a student
    - get_class_attendance: Get attendance for entire class
    - calculate_percentage: Calculate attendance percentage
    - generate_report: Generate attendance report
    """
    
    def __init__(self, db_connection=None):
        """
        Initialize attendance service.
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
    
    def mark_attendance(
        self,
        lecture_id: int,
        student_id: int,
        status: str,
        faculty_id: int,
        remarks: str = ""
    ) -> Dict[str, Any]:
        """
        Mark attendance for a student in a lecture.
        
        Args:
            lecture_id: ID of the lecture/class
            student_id: ID of the student
            status: Attendance status (PRESENT/ABSENT)
            faculty_id: ID of faculty marking attendance
            remarks: Optional remarks about attendance
        
        Returns:
            dict: Success status and attendance record ID
            
        Example:
            result = attendance_service.mark_attendance(
                lecture_id=1,
                student_id=5,
                status='PRESENT',
                faculty_id=10
            )
        """
        try:
            # Validate inputs
            if not self._validate_status(status):
                return {
                    'success': False,
                    'error': f'Invalid status: {status}. Must be PRESENT or ABSENT.'
                }
            
            # Check if already marked
            existing = self._check_existing_attendance(lecture_id, student_id)
            if existing:
                return {
                    'success': False,
                    'error': 'Attendance already marked for this student in this lecture'
                }
            
            status_id = self._get_status_id(status)
            if not status_id:
                return {
                    'success': False,
                    'error': f'Unknown attendance status: {status}'
                }

            # Insert attendance record
            with get_cursor() as (conn, cur):
                cur.execute(
                    """
                    INSERT INTO attendance (student_id, status_id, marked_at, lecture_id)
                    VALUES (%s, %s, NOW(), %s)
                    """,
                    (student_id, status_id, lecture_id),
                )
                attendance_id = cur.lastrowid

            return {
                'success': True,
                'message': f'Attendance marked as {status}',
                'attendance_id': attendance_id
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error marking attendance: {str(e)}'
            }
    
    def edit_attendance(
        self,
        attendance_id: int,
        new_status: str,
        remarks: str = ""
    ) -> Dict[str, Any]:
        """
        Edit existing attendance record.
        
        Args:
            attendance_id: ID of the attendance record to edit
            new_status: New attendance status
            remarks: Updated remarks
        
        Returns:
            dict: Success status and updated record
            
        Example:
            result = attendance_service.edit_attendance(
                attendance_id=5,
                new_status='ABSENT',
                remarks='Approved leave'
            )
        """
        try:
            # Validate status
            if not self._validate_status(new_status):
                return {
                    'success': False,
                    'error': f'Invalid status: {new_status}'
                }
            
            # Check if record exists
            existing = self._get_attendance_by_id(attendance_id)
            if not existing:
                return {
                    'success': False,
                    'error': f'Attendance record {attendance_id} not found'
                }
            
            status_id = self._get_status_id(new_status)
            if not status_id:
                return {
                    'success': False,
                    'error': f'Unknown attendance status: {new_status}'
                }

            with get_cursor() as (conn, cur):
                cur.execute(
                    """
                    UPDATE attendance
                    SET status_id = %s, marked_at = NOW()
                    WHERE attendance_id = %s
                    """,
                    (status_id, attendance_id),
                )
            
            return {
                'success': True,
                'message': 'Attendance updated successfully',
                'new_status': new_status
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error updating attendance: {str(e)}'
            }
    
    def get_student_attendance(
        self,
        student_id: int,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get attendance records for a specific student.
        
        Args:
            student_id: ID of the student
            month: Optional month filter (1-12)
            year: Optional year filter
        
        Returns:
            list: List of attendance records
            
        Example:
            records = attendance_service.get_student_attendance(
                student_id=5,
                month=1,
                year=2024
            )
        """
        try:
            # Build query with filters
            query_filters = {'student_id': student_id}
            
            if month and year:
                query_filters['month'] = month
                query_filters['year'] = year
            
            where_clauses = ["a.student_id = %s"]
            params: List[Any] = [student_id]

            if month and year:
                where_clauses.append("MONTH(a.marked_at) = %s AND YEAR(a.marked_at) = %s")
                params.extend([month, year])

            query = f"""
                SELECT
                    a.attendance_id,
                    a.student_id,
                    a.lecture_id,
                    s.status_name,
                    a.marked_at,
                    l.lecture_date
                FROM attendance a
                JOIN attendance_status s ON s.status_id = a.status_id
                LEFT JOIN lecture l ON l.lecture_id = a.lecture_id
                WHERE {' AND '.join(where_clauses)}
                ORDER BY a.marked_at DESC
            """

            rows = fetch_all(query, params)
            return self._rows_to_dicts(rows, [
                "attendance_id",
                "student_id",
                "lecture_id",
                "status",
                "marked_at",
                "lecture_date",
            ])
        
        except Exception as e:
            return []
    
    def get_class_attendance(
        self,
        lecture_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get attendance for entire class/lecture.
        
        Args:
            lecture_id: ID of the lecture
        
        Returns:
            list: Attendance records for all students
        """
        try:
            query = """
                SELECT
                    a.attendance_id,
                    a.student_id,
                    a.lecture_id,
                    s.status_name,
                    a.marked_at
                FROM attendance a
                JOIN attendance_status s ON s.status_id = a.status_id
                WHERE a.lecture_id = %s
                ORDER BY a.student_id ASC
            """
            rows = fetch_all(query, [lecture_id])
            return self._rows_to_dicts(rows, [
                "attendance_id",
                "student_id",
                "lecture_id",
                "status",
                "marked_at",
            ])
        
        except Exception as e:
            return []
    
    def calculate_percentage(
        self,
        student_id: int,
        subject_id: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Calculate attendance percentage for a student.
        
        Args:
            student_id: ID of the student
            subject_id: Optional subject filter
        
        Returns:
            dict: Attendance percentage and details
            
        Example:
            stats = attendance_service.calculate_percentage(
                student_id=5,
                subject_id=10
            )
            # Returns: {'percentage': 85.5, 'present': 17, 'absent': 3, 'total': 20}
        """
        try:
            present_status_id = self._get_status_id("PRESENT")
            if not present_status_id:
                return {'percentage': 0.0, 'present': 0, 'absent': 0, 'total': 0}

            params: List[Any] = [student_id]
            where = ["a.student_id = %s"]

            if subject_id:
                where.append("t.subject_id = %s")
                params.append(subject_id)

            total_query = f"""
                SELECT COUNT(*)
                FROM attendance a
                LEFT JOIN lecture l ON l.lecture_id = a.lecture_id
                LEFT JOIN timetable t ON t.timetable_id = l.timetable_id
                WHERE {' AND '.join(where)}
            """

            present_query = f"""
                SELECT COUNT(*)
                FROM attendance a
                LEFT JOIN lecture l ON l.lecture_id = a.lecture_id
                LEFT JOIN timetable t ON t.timetable_id = l.timetable_id
                WHERE {' AND '.join(where)} AND a.status_id = %s
            """

            total = fetch_one(total_query, params)
            present = fetch_one(present_query, params + [present_status_id])

            total_count = int(total[0]) if total else 0
            present_count = int(present[0]) if present else 0
            absent_count = total_count - present_count
            percentage = (present_count / total_count * 100) if total_count > 0 else 0.0

            return {
                'percentage': round(percentage, 2),
                'present': present_count,
                'absent': absent_count,
                'total': total_count
            }
        
        except Exception as e:
            return {'percentage': 0.0, 'error': str(e)}
    
    def generate_report(
        self,
        filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate attendance report with various filters.
        
        Args:
            filters: Filter criteria (student_id, faculty_id, subject_id, etc.)
        
        Returns:
            dict: Report data with statistics
        """
        try:
            where_clauses: List[str] = []
            params: List[Any] = []

            if filters.get('student_id'):
                where_clauses.append("a.student_id = %s")
                params.append(filters['student_id'])

            if filters.get('lecture_id'):
                where_clauses.append("a.lecture_id = %s")
                params.append(filters['lecture_id'])

            if filters.get('subject_id'):
                where_clauses.append("t.subject_id = %s")
                params.append(filters['subject_id'])

            if filters.get('faculty_id'):
                where_clauses.append("t.faculty_id = %s")
                params.append(filters['faculty_id'])

            if filters.get('division_id'):
                where_clauses.append("t.division_id = %s")
                params.append(filters['division_id'])

            if filters.get('start_date') and filters.get('end_date'):
                where_clauses.append("a.marked_at BETWEEN %s AND %s")
                params.extend([filters['start_date'], filters['end_date']])

            where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            query = f"""
                SELECT
                    a.attendance_id,
                    a.student_id,
                    a.lecture_id,
                    s.status_name,
                    a.marked_at,
                    l.lecture_date,
                    t.subject_id,
                    t.faculty_id,
                    t.division_id
                FROM attendance a
                LEFT JOIN attendance_status s ON s.status_id = a.status_id
                LEFT JOIN lecture l ON l.lecture_id = a.lecture_id
                LEFT JOIN timetable t ON t.timetable_id = l.timetable_id
                {where_sql}
                ORDER BY a.marked_at DESC
            """

            rows = fetch_all(query, params)
            records = self._rows_to_dicts(rows, [
                "attendance_id",
                "student_id",
                "lecture_id",
                "status",
                "marked_at",
                "lecture_date",
                "subject_id",
                "faculty_id",
                "division_id",
            ])

            present_count = sum(1 for r in records if r["status"] == "PRESENT")
            absent_count = sum(1 for r in records if r["status"] == "ABSENT")
            total_records = len(records)
            average_percentage = (present_count / total_records * 100) if total_records else 0.0

            return {
                'total_records': total_records,
                'present_count': present_count,
                'absent_count': absent_count,
                'average_percentage': round(average_percentage, 2),
                'records': records
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    # ========== HELPER METHODS ==========
    
    def _validate_status(self, status: str) -> bool:
        """
        Validate attendance status.
        
        Args:
            status: Status string to validate
        
        Returns:
            bool: True if valid
        """
        valid_statuses = ['PRESENT', 'ABSENT']
        return status.upper() in valid_statuses
    
    def _check_existing_attendance(
        self,
        lecture_id: int,
        student_id: int
    ) -> bool:
        """Check if attendance already marked for student in lecture."""
        query = """
            SELECT 1 FROM attendance
            WHERE lecture_id = %s AND student_id = %s
            LIMIT 1
        """
        row = fetch_one(query, [lecture_id, student_id])
        return bool(row)
    
    def _get_attendance_by_id(self, attendance_id: int) -> Optional[Dict]:
        """Get attendance record by ID."""
        query = """
            SELECT
                a.attendance_id,
                a.student_id,
                a.lecture_id,
                s.status_name,
                a.marked_at
            FROM attendance a
            JOIN attendance_status s ON s.status_id = a.status_id
            WHERE a.attendance_id = %s
            LIMIT 1
        """
        row = fetch_one(query, [attendance_id])
        if not row:
            return None
        return {
            "attendance_id": row[0],
            "student_id": row[1],
            "lecture_id": row[2],
            "status": row[3],
            "marked_at": row[4],
        }

    def _get_status_id(self, status: str) -> Optional[int]:
        """Get status_id from attendance_status by status name."""
        row = fetch_one(
            "SELECT status_id FROM attendance_status WHERE status_name = %s",
            [status.upper()],
        )
        return int(row[0]) if row else None

    @staticmethod
    def _rows_to_dicts(rows: List[tuple], keys: List[str]) -> List[Dict[str, Any]]:
        return [dict(zip(keys, row)) for row in rows]
