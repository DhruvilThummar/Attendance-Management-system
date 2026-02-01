"""
Timetable Management Service
============================

Handles timetable/schedule operations:
- Create and manage class schedules
- Assign faculty to lectures
- View schedules by division/faculty
- Generate lecture instances
- Manage time slots

Author: Development Team
Version: 1.0
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from ..db_manager import get_cursor, fetch_all, fetch_one


class TimetableService:
    """
    Service for managing timetables and schedules.
    
    Methods:
    - create_schedule: Create a schedule entry
    - assign_faculty: Assign faculty to a schedule
    - get_division_schedule: Get schedule for a division
    - get_faculty_schedule: Get schedule for a faculty
    - create_lectures: Generate lecture instances
    - update_schedule: Update schedule details
    """
    
    def __init__(self, db_connection=None):
        """
        Initialize timetable service.
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
    
    def create_schedule(
        self,
        division_id: int,
        subject_id: int,
        faculty_id: int,
        day_of_week: str,
        start_time: str,
        end_time: str,
        room_no: str = ""
    ) -> Dict[str, Any]:
        """
        Create a new schedule entry.
        
        Args:
            division_id: ID of the division/section
            subject_id: ID of the subject
            faculty_id: ID of the faculty
            day_of_week: Day name (Monday, Tuesday, etc.)
            start_time: Start time (HH:MM format)
            end_time: End time (HH:MM format)
            room_no: Room/classroom number
        
        Returns:
            dict: Success status and schedule ID
            
        Example:
            result = timetable_service.create_schedule(
                division_id=1,
                subject_id=5,
                faculty_id=10,
                day_of_week='Monday',
                start_time='09:00',
                end_time='10:00',
                room_no='A101'
            )
        """
        try:
            # Validate inputs
            if not self._validate_day(day_of_week):
                return {'success': False, 'error': 'Invalid day of week'}
            
            if not self._validate_time(start_time, end_time):
                return {'success': False, 'error': 'Invalid time format'}
            
            # Normalize day for DB enum
            day_enum = self._normalize_day(day_of_week)

            # Check for scheduling conflicts
            conflict = self._check_conflict(
                faculty_id, division_id, day_enum, start_time, end_time
            )
            if conflict:
                return {'success': False, 'error': 'Faculty has conflict with another class'}
            
            # Create schedule record
            # Determine next lecture number for the day/division
            lecture_no_row = fetch_one(
                """
                SELECT COALESCE(MAX(lecture_no), 0) + 1
                FROM timetable
                WHERE division_id = %s AND day_of_week = %s
                """,
                [division_id, day_enum],
            )
            lecture_no = int(lecture_no_row[0]) if lecture_no_row else 1

            with get_cursor() as (conn, cur):
                cur.execute(
                    """
                    INSERT INTO timetable (
                        subject_id, faculty_id, division_id, day_of_week,
                        lecture_no, room_no, start_time, end_time
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        subject_id,
                        faculty_id,
                        division_id,
                        day_enum,
                        lecture_no,
                        room_no or None,
                        start_time,
                        end_time,
                    ),
                )
                schedule_id = cur.lastrowid

            return {
                'success': True,
                'message': 'Schedule created successfully',
                'schedule_id': schedule_id
            }
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_division_schedule(
        self,
        division_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get complete schedule for a division.
        
        Args:
            division_id: ID of the division
        
        Returns:
            list: Schedule entries for the division
            
        Example:
            schedule = timetable_service.get_division_schedule(division_id=1)
            # Returns schedule grouped by day
        """
        try:
            query = """
                SELECT
                    timetable_id,
                    subject_id,
                    faculty_id,
                    division_id,
                    day_of_week,
                    lecture_no,
                    room_no,
                    start_time,
                    end_time
                FROM timetable
                WHERE division_id = %s
                ORDER BY day_of_week, start_time
            """
            rows = fetch_all(query, [division_id])

            organized_schedule = {
                'Monday': [],
                'Tuesday': [],
                'Wednesday': [],
                'Thursday': [],
                'Friday': [],
                'Saturday': [],
                'Sunday': []
            }

            for row in rows:
                entry = {
                    'timetable_id': row[0],
                    'subject_id': row[1],
                    'faculty_id': row[2],
                    'division_id': row[3],
                    'day_of_week': self._denormalize_day(row[4]),
                    'lecture_no': row[5],
                    'room_no': row[6],
                    'start_time': str(row[7]),
                    'end_time': str(row[8])
                }
                organized_schedule[entry['day_of_week']].append(entry)

            return organized_schedule
        
        except Exception as e:
            return {}
    
    def get_faculty_schedule(
        self,
        faculty_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get schedule for a specific faculty.
        
        Args:
            faculty_id: ID of the faculty
        
        Returns:
            list: Faculty's schedule entries
        """
        try:
            query = """
                SELECT
                    timetable_id,
                    subject_id,
                    faculty_id,
                    division_id,
                    day_of_week,
                    lecture_no,
                    room_no,
                    start_time,
                    end_time
                FROM timetable
                WHERE faculty_id = %s
                ORDER BY day_of_week, start_time
            """
            rows = fetch_all(query, [faculty_id])
            return [
                {
                    'timetable_id': r[0],
                    'subject_id': r[1],
                    'faculty_id': r[2],
                    'division_id': r[3],
                    'day_of_week': self._denormalize_day(r[4]),
                    'lecture_no': r[5],
                    'room_no': r[6],
                    'start_time': str(r[7]),
                    'end_time': str(r[8])
                }
                for r in rows
            ]
        
        except Exception as e:
            return []
    
    def create_lectures(
        self,
        schedule_id: int,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """
        Generate lecture instances from a schedule entry.
        
        This creates actual lecture records that can have attendance marked.
        
        Args:
            schedule_id: ID of the schedule template
            start_date: Start date for lecture generation (YYYY-MM-DD)
            end_date: End date for lecture generation (YYYY-MM-DD)
        
        Returns:
            dict: Number of lectures created and success status
            
        Example:
            result = timetable_service.create_lectures(
                schedule_id=1,
                start_date='2024-01-01',
                end_date='2024-01-31'
            )
            # Returns: {'success': True, 'lectures_created': 4}
        """
        try:
            # Get schedule details
            schedule = self._get_schedule(schedule_id)
            if not schedule:
                return {'success': False, 'error': 'Schedule not found'}
            
            # Parse dates
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Generate lecture dates matching day of week
            lectures_created = 0
            current_date = start
            
            while current_date <= end:
                # Check if this day matches the schedule day
                if self._get_day_name(current_date) == schedule['day_of_week']:
                    with get_cursor() as (conn, cur):
                        cur.execute(
                            """
                            INSERT INTO lecture (timetable_id, lecture_date)
                            VALUES (%s, %s)
                            """,
                            (schedule_id, current_date.date()),
                        )
                    lectures_created += 1
                
                current_date += timedelta(days=1)
            
            return {
                'success': True,
                'message': f'{lectures_created} lectures created',
                'lectures_created': lectures_created
            }
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_schedule(
        self,
        schedule_id: int,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update schedule details.
        
        Args:
            schedule_id: ID of the schedule to update
            updates: Dictionary of fields to update
        
        Returns:
            dict: Success status
        """
        try:
            allowed_fields = {
                'subject_id', 'faculty_id', 'division_id', 'day_of_week',
                'lecture_no', 'room_no', 'start_time', 'end_time', 'building_block'
            }
            set_clauses = []
            params: List[Any] = []

            for key, value in updates.items():
                if key not in allowed_fields:
                    continue
                if key == 'day_of_week':
                    value = self._normalize_day(str(value))
                set_clauses.append(f"{key} = %s")
                params.append(value)

            if not set_clauses:
                return {'success': False, 'error': 'No valid fields to update'}

            params.append(schedule_id)
            query = f"""
                UPDATE timetable
                SET {', '.join(set_clauses)}
                WHERE timetable_id = %s
            """

            with get_cursor() as (conn, cur):
                cur.execute(query, params)

            return {'success': True, 'message': 'Schedule updated'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ========== HELPER METHODS ==========
    
    def _validate_day(self, day: str) -> bool:
        """Validate day of week."""
        valid_days = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday'
        ]
        valid_enum = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        return day in valid_days or day in valid_enum
    
    def _validate_time(self, start_time: str, end_time: str) -> bool:
        """Validate time format and logic."""
        try:
            start = datetime.strptime(start_time, '%H:%M')
            end = datetime.strptime(end_time, '%H:%M')
            return start < end
        except ValueError:
            return False
    
    def _check_conflict(
        self,
        faculty_id: int,
        division_id: int,
        day: str,
        start_time: str,
        end_time: str
    ) -> bool:
        """Check for scheduling conflicts."""
        query = """
            SELECT 1
            FROM timetable
            WHERE day_of_week = %s
              AND (faculty_id = %s OR division_id = %s)
              AND NOT (end_time <= %s OR start_time >= %s)
            LIMIT 1
        """
        row = fetch_one(query, [day, faculty_id, division_id, start_time, end_time])
        return bool(row)
    
    def _get_schedule(self, schedule_id: int) -> Optional[Dict]:
        """Get schedule record by ID."""
        query = """
            SELECT
                timetable_id,
                subject_id,
                faculty_id,
                division_id,
                day_of_week,
                lecture_no,
                room_no,
                start_time,
                end_time
            FROM timetable
            WHERE timetable_id = %s
            LIMIT 1
        """
        row = fetch_one(query, [schedule_id])
        if not row:
            return None
        return {
            'timetable_id': row[0],
            'subject_id': row[1],
            'faculty_id': row[2],
            'division_id': row[3],
            'day_of_week': self._denormalize_day(row[4]),
            'lecture_no': row[5],
            'room_no': row[6],
            'start_time': str(row[7]),
            'end_time': str(row[8])
        }
    
    def _get_day_name(self, date: datetime) -> str:
        """Get day name from date."""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[date.weekday()]

    def _normalize_day(self, day: str) -> str:
        mapping = {
            'Monday': 'MON',
            'Tuesday': 'TUE',
            'Wednesday': 'WED',
            'Thursday': 'THU',
            'Friday': 'FRI',
            'Saturday': 'SAT',
            'Sunday': 'SUN'
        }
        if day in mapping:
            return mapping[day]
        return day

    def _denormalize_day(self, day: str) -> str:
        mapping = {
            'MON': 'Monday',
            'TUE': 'Tuesday',
            'WED': 'Wednesday',
            'THU': 'Thursday',
            'FRI': 'Friday',
            'SAT': 'Saturday',
            'SUN': 'Sunday'
        }
        return mapping.get(day, day)
