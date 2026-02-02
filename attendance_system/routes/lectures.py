"""
Lecture management routes
"""
from flask import Blueprint, jsonify, request, session
from datetime import datetime
from ..db_manager import create_connection
from ..decorators.rbac import login_required, faculty_only

lectures_bp = Blueprint("lectures", __name__, url_prefix="/api")


@lectures_bp.route("/lectures", methods=["GET"])
@login_required
def get_lectures():
    """
    Get lectures with optional filters.
    
    Query params:
        - faculty_id: Filter by faculty
        - division_id: Filter by division
        - date: Filter by specific date (YYYY-MM-DD)
    
    Returns:
        JSON response with lecture list
    """
    try:
        faculty_id = request.args.get("faculty_id")
        division_id = request.args.get("division_id")
        date_str = request.args.get("date")
        
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                l.lecture_id,
                l.timetable_id,
                l.lecture_date,
                l.actual_start_time,
                l.actual_end_time,
                t.subject_id,
                s.subject_code,
                s.subject_name,
                t.faculty_id,
                u.name as faculty_name,
                f.short_name as faculty_short_name,
                t.division_id,
                d.division_name,
                t.lecture_no,
                t.room_no,
                t.building_block
            FROM lecture l
            JOIN timetable t ON l.timetable_id = t.timetable_id
            JOIN subject s ON t.subject_id = s.subject_id
            JOIN faculty f ON t.faculty_id = f.faculty_id
            JOIN users u ON f.user_id = u.user_id
            LEFT JOIN division d ON t.division_id = d.division_id
            WHERE 1=1
        """
        
        params = []
        
        if faculty_id:
            query += " AND t.faculty_id = %s"
            params.append(faculty_id)
        
        if division_id:
            query += " AND t.division_id = %s"
            params.append(division_id)
        
        if date_str:
            query += " AND l.lecture_date = %s"
            params.append(date_str)
        
        query += " ORDER BY l.lecture_date DESC, l.actual_start_time DESC"
        
        cursor.execute(query, params)
        lectures = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "lectures": lectures})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@lectures_bp.route("/lectures/<int:lecture_id>", methods=["GET"])
@login_required
def get_lecture(lecture_id):
    """
    Get details of a specific lecture.
    
    Returns:
        JSON response with lecture details
    """
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                l.lecture_id,
                l.timetable_id,
                l.lecture_date,
                l.actual_start_time,
                l.actual_end_time,
                t.subject_id,
                s.subject_code,
                s.subject_name,
                t.faculty_id,
                u.name as faculty_name,
                f.short_name as faculty_short_name,
                t.division_id,
                d.division_name,
                t.lecture_no,
                t.room_no,
                t.building_block
            FROM lecture l
            JOIN timetable t ON l.timetable_id = t.timetable_id
            JOIN subject s ON t.subject_id = s.subject_id
            JOIN faculty f ON t.faculty_id = f.faculty_id
            JOIN users u ON f.user_id = u.user_id
            LEFT JOIN division d ON t.division_id = d.division_id
            WHERE l.lecture_id = %s
        """, (lecture_id,))
        
        lecture = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not lecture:
            return jsonify({"success": False, "message": "Lecture not found"}), 404
        
        return jsonify({"success": True, "lecture": lecture})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@lectures_bp.route("/lectures", methods=["POST"])
@login_required
@faculty_only
def create_lecture():
    """
    Create a new lecture.
    
    POST body:
        - timetable_id: Timetable entry ID
        - lecture_date: Date of lecture (YYYY-MM-DD)
        - actual_start_time: Actual start time (HH:MM:SS, optional)
        - actual_end_time: Actual end time (HH:MM:SS, optional)
    
    Returns:
        JSON response with success status and new lecture_id
    """
    data = request.get_json()
    
    if "timetable_id" not in data or "lecture_date" not in data:
        return jsonify({"success": False, "message": "timetable_id and lecture_date are required"}), 400
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO lecture 
            (timetable_id, lecture_date, actual_start_time, actual_end_time)
            VALUES (%s, %s, %s, %s)
        """, (
            data["timetable_id"],
            data["lecture_date"],
            data.get("actual_start_time"),
            data.get("actual_end_time")
        ))
        
        lecture_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": "Lecture created successfully",
            "lecture_id": lecture_id
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@lectures_bp.route("/lectures/<int:lecture_id>/students", methods=["GET"])
@login_required
def get_lecture_students(lecture_id):
    """
    Get list of students for a lecture (based on the division).
    
    Returns:
        JSON response with student list
    """
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        # First get the division_id for this lecture
        cursor.execute("""
            SELECT t.division_id
            FROM lecture l
            JOIN timetable t ON l.timetable_id = t.timetable_id
            WHERE l.lecture_id = %s
        """, (lecture_id,))
        
        result = cursor.fetchone()
        if not result or not result["division_id"]:
            return jsonify({"success": False, "message": "Lecture or division not found"}), 404
        
        division_id = result["division_id"]
        
        # Get all students in this division
        cursor.execute("""
            SELECT 
                s.student_id,
                u.name,
                s.roll_no,
                s.enrollment_no,
                a.attendance_id,
                ast.status_name,
                a.marked_at
            FROM student s
            JOIN users u ON s.user_id = u.user_id
            LEFT JOIN attendance a ON s.student_id = a.student_id AND a.lecture_id = %s
            LEFT JOIN attendance_status ast ON a.status_id = ast.status_id
            WHERE s.division_id = %s
            ORDER BY s.roll_no
        """, (lecture_id, division_id))
        
        students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "students": students})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@lectures_bp.route("/lectures/<int:lecture_id>", methods=["PUT"])
@login_required
@faculty_only
def update_lecture(lecture_id):
    """
    Update lecture details.
    
    PUT body:
        - actual_start_time: Actual start time
        - actual_end_time: Actual end time
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    updates = []
    params = []
    
    if "actual_start_time" in data:
        updates.append("actual_start_time = %s")
        params.append(data["actual_start_time"])
    
    if "actual_end_time" in data:
        updates.append("actual_end_time = %s")
        params.append(data["actual_end_time"])
    
    if not updates:
        return jsonify({"success": False, "message": "No fields to update"}), 400
    
    params.append(lecture_id)
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            f"UPDATE lecture SET {', '.join(updates)} WHERE lecture_id = %s",
            params
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Lecture updated successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@lectures_bp.route("/lectures/<int:lecture_id>", methods=["DELETE"])
@login_required
@faculty_only
def delete_lecture(lecture_id):
    """
    Delete a lecture.
    
    Returns:
        JSON response with success status
    """
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Note: This will fail if there are attendance records for this lecture
        # due to foreign key constraints. Consider adding cascade delete or
        # checking for attendance records first.
        cursor.execute("DELETE FROM lecture WHERE lecture_id = %s", (lecture_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Lecture deleted successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
