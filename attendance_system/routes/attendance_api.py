"""Attendance API routes."""

from __future__ import annotations

from flask import request, jsonify, session
from datetime import datetime

from . import api
from ..db_manager import create_connection
from ..decorators.rbac import login_required, faculty_only
from ..services.attendance_service import AttendanceService

attendance_svc = AttendanceService()


@api.route("/attendance/mark", methods=["POST"])
@login_required
@faculty_only
def mark_attendance():
    """
    Mark attendance for students.
    
    POST body:
        - lecture_id: ID of the lecture
        - student_ids: List of present student IDs
        - date: Date of attendance (YYYY-MM-DD)
        - remarks: Optional remarks
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    lecture_id = data.get("lecture_id")
    student_ids = data.get("student_ids", [])
    attendance_date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    remarks = data.get("remarks")
    
    if not lecture_id:
        return jsonify({"success": False, "message": "Lecture ID is required"}), 400
    
    try:
        faculty_id = session.get("user_id")
        
        # Mark attendance for each student
        for student_id in student_ids:
            attendance_svc.mark_attendance(
                student_id=student_id,
                lecture_id=lecture_id,
                date=attendance_date,
                status="present",
                marked_by=faculty_id,
                remarks=remarks
            )
        
        return jsonify({
            "success": True,
            "message": f"Attendance marked for {len(student_ids)} students"
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/attendance/student/<int:student_id>", methods=["GET"])
@login_required
def get_student_attendance(student_id):
    """
    Get attendance records for a specific student.
    
    Query params:
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        - subject_id: Filter by subject
    
    Returns:
        JSON response with attendance records
    """
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    subject_id = request.args.get("subject_id")
    
    try:
        records = attendance_svc.get_student_attendance(
            student_id=student_id,
            start_date=start_date,
            end_date=end_date,
            subject_id=subject_id
        )
        
        percentage = attendance_svc.calculate_percentage(student_id)
        
        return jsonify({
            "success": True,
            "records": records,
            "attendance_percentage": percentage
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/attendance/lecture/<int:lecture_id>", methods=["GET"])
@login_required
def get_lecture_attendance(lecture_id):
    """
    Get attendance records for a specific lecture.
    
    Returns:
        JSON response with attendance records
    """
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                a.attendance_id,
                a.student_id,
                u.first_name,
                u.last_name,
                a.status,
                a.date,
                a.remarks
            FROM attendance a
            JOIN users u ON a.student_id = u.user_id
            WHERE a.lecture_id = %s
            ORDER BY u.last_name, u.first_name
        """, (lecture_id,))
        
        records = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "records": records})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/attendance/update/<int:attendance_id>", methods=["PUT"])
@login_required
@faculty_only
def update_attendance(attendance_id):
    """
    Update an existing attendance record.
    
    PUT body:
        - status: "present", "absent", "late", "excused"
        - remarks: Optional remarks
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    status = data.get("status")
    remarks = data.get("remarks")
    
    if not status:
        return jsonify({"success": False, "message": "Status is required"}), 400
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE attendance 
               SET status = %s, remarks = %s, updated_at = NOW()
               WHERE attendance_id = %s""",
            (status, remarks, attendance_id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Attendance updated successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/attendance/bulk-mark", methods=["POST"])
@login_required
@faculty_only
def bulk_mark_attendance():
    """
    Mark attendance for multiple students at once.
    
    POST body:
        - lecture_id: ID of the lecture
        - attendance_data: List of {student_id, status, remarks}
        - date: Date of attendance (YYYY-MM-DD)
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    lecture_id = data.get("lecture_id")
    attendance_data = data.get("attendance_data", [])
    attendance_date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    if not lecture_id or not attendance_data:
        return jsonify({"success": False, "message": "Lecture ID and attendance data are required"}), 400
    
    try:
        faculty_id = session.get("user_id")
        conn = create_connection()
        cursor = conn.cursor()
        
        # Insert or update attendance records
        for record in attendance_data:
            cursor.execute(
                """INSERT INTO attendance 
                   (student_id, lecture_id, date, status, remarks, marked_by)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE
                   status = VALUES(status),
                   remarks = VALUES(remarks),
                   updated_at = NOW()""",
                (
                    record["student_id"],
                    lecture_id,
                    attendance_date,
                    record.get("status", "present"),
                    record.get("remarks"),
                    faculty_id
                )
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": f"Bulk attendance marked for {len(attendance_data)} students"
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/attendance/statistics", methods=["GET"])
@login_required
def attendance_statistics():
    """
    Get attendance statistics.
    
    Query params:
        - type: "student", "class", "subject"
        - id: Corresponding ID
        - period: "week", "month", "semester"
    
    Returns:
        JSON response with statistics
    """
    stats_type = request.args.get("type", "student")
    entity_id = request.args.get("id")
    period = request.args.get("period", "month")
    
    try:
        stats = attendance_svc.get_statistics(stats_type, entity_id, period)
        return jsonify({"success": True, "statistics": stats})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
