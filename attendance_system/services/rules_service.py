"""Attendance threshold rules implementation."""
from __future__ import annotations
import logging
from ..db_manager import execute, fetch_one
from ..models.notification import Notification

logger = logging.getLogger(__name__)
THRESHOLD = 75.0

def get_attendance_percentage(student_id: int, subject_id: int) -> float:
    """Calculate attendance percentage for a student in a specific subject."""
    # 1. Get total lectures for the subject
    # Join lectures -> timetable -> subject
    query_total = """
        SELECT COUNT(l.id) 
        FROM lectures l
        JOIN timetable t ON l.timetable_id = t.id
        WHERE t.subject_id = %s
    """
    row_total = fetch_one(query_total, (subject_id,))
    total = row_total[0] if row_total else 0
    
    if total == 0:
        return 100.0  # No lectures yet, so 100% attendance (or 0? usually 100 is safer to avoid alarm)

    # 2. Get attended lectures
    query_attended = """
        SELECT COUNT(a.id)
        FROM attendance a
        JOIN lectures l ON a.lecture_id = l.id
        JOIN timetable t ON l.timetable_id = t.id
        WHERE a.student_id = %s AND t.subject_id = %s AND a.status = 'P'
    """
    row_attended = fetch_one(query_attended, (student_id, subject_id))
    attended = row_attended[0] if row_attended else 0
    
    return (attended / total) * 100.0

def check_and_notify_defaulter(student_id: int, subject_id: int) -> bool:
    """Check if student is below threshold and notify if so."""
    percentage = get_attendance_percentage(student_id, subject_id)
    if percentage < THRESHOLD:
        # Check if notification already sent essentially (optional, to avoid spam)
        # For now, just create a notification
        msg = f"Warning: Your attendance in Subject ID {subject_id} is {percentage:.1f}%, which is below the 75% threshold."
        # Assuming we have a user_id for the student, we need to fetch it.
        # But we only have student_id. We need to look up student->user_id
        q = "SELECT user_id FROM students WHERE id = %s"
        r = fetch_one(q, (student_id,))
        if r and r[0]:
            user_id = r[0]
            # Use notification service logic or model directly
            Notification(user_id=user_id, message=msg, seen=False).save()
            return True
    return False

def get_defaulters_list(subject_id: int, division_id: int) -> list[dict]:
    """Get list of defaulters for a subject and division."""
    # Get all students in division
    query_students = "SELECT id, enrollment_no FROM students WHERE division_id = %s"
    students = execute(query_students, (division_id,))
    
    defaulters = []
    for sid, enrollment in students:
        pct = get_attendance_percentage(sid, subject_id)
        if pct < THRESHOLD:
            defaulters.append({
                "student_id": sid,
                "enrollment_no": enrollment,
                "percentage": pct
            })
    return defaulters
