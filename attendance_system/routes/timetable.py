"""
Timetable management routes
"""
from flask import Blueprint, jsonify, request, session
from ..db_manager import create_connection
from ..decorators.rbac import login_required, faculty_only

timetable_bp = Blueprint("timetable", __name__, url_prefix="/api")


@timetable_bp.route("/timetable", methods=["GET"])
@login_required
def get_timetable():
    """
    Get timetable entries with optional filters.
    
    Query params:
        - division_id: Filter by division
        - faculty_id: Filter by faculty
        - day_of_week: Filter by day (Monday, Tuesday, etc.)
    
    Returns:
        JSON response with timetable entries
    """
    try:
        division_id = request.args.get("division_id")
        faculty_id = request.args.get("faculty_id")
        day_of_week = request.args.get("day_of_week")
        
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                t.timetable_id,
                t.subject_id,
                s.subject_code,
                s.subject_name,
                t.faculty_id,
                u.name as faculty_name,
                f.short_name as faculty_short_name,
                t.division_id,
                d.division_name,
                t.day_of_week,
                t.lecture_no,
                t.room_no,
                t.building_block,
                t.start_time,
                t.end_time
            FROM timetable t
            JOIN subject s ON t.subject_id = s.subject_id
            JOIN faculty f ON t.faculty_id = f.faculty_id
            JOIN users u ON f.user_id = u.user_id
            LEFT JOIN division d ON t.division_id = d.division_id
            WHERE 1=1
        """
        
        params = []
        
        if division_id:
            query += " AND t.division_id = %s"
            params.append(division_id)
        
        if faculty_id:
            query += " AND t.faculty_id = %s"
            params.append(faculty_id)
        
        if day_of_week:
            query += " AND t.day_of_week = %s"
            params.append(day_of_week)
        
        query += " ORDER BY t.day_of_week, t.start_time"
        
        cursor.execute(query, params)
        timetable = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "timetable": timetable})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@timetable_bp.route("/timetable/<int:timetable_id>", methods=["GET"])
@login_required
def get_timetable_entry(timetable_id):
    """
    Get details of a specific timetable entry.
    
    Returns:
        JSON response with timetable entry
    """
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                t.timetable_id,
                t.subject_id,
                s.subject_code,
                s.subject_name,
                t.faculty_id,
                u.name as faculty_name,
                f.short_name as faculty_short_name,
                t.division_id,
                d.division_name,
                t.day_of_week,
                t.lecture_no,
                t.room_no,
                t.building_block,
                t.start_time,
                t.end_time
            FROM timetable t
            JOIN subject s ON t.subject_id = s.subject_id
            JOIN faculty f ON t.faculty_id = f.faculty_id
            JOIN users u ON f.user_id = u.user_id
            LEFT JOIN division d ON t.division_id = d.division_id
            WHERE t.timetable_id = %s
        """, (timetable_id,))
        
        entry = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not entry:
            return jsonify({"success": False, "message": "Timetable entry not found"}), 404
        
        return jsonify({"success": True, "entry": entry})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@timetable_bp.route("/timetable", methods=["POST"])
@login_required
@faculty_only
def create_timetable_entry():
    """
    Create a new timetable entry.
    
    POST body:
        - subject_id: Subject ID
        - faculty_id: Faculty ID
        - division_id: Division ID
        - day_of_week: Day (Monday, Tuesday, etc.)
        - lecture_no: Lecture number
        - room_no: Room number
        - building_block: Building block
        - start_time: Start time (HH:MM:SS)
        - end_time: End time (HH:MM:SS)
    
    Returns:
        JSON response with success status and new timetable_id
    """
    data = request.get_json()
    
    required_fields = ["subject_id", "faculty_id", "division_id", "day_of_week", 
                      "lecture_no", "start_time", "end_time"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"{field} is required"}), 400
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO timetable 
            (subject_id, faculty_id, division_id, day_of_week, lecture_no, 
             room_no, building_block, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["subject_id"],
            data["faculty_id"],
            data["division_id"],
            data["day_of_week"],
            data["lecture_no"],
            data.get("room_no"),
            data.get("building_block"),
            data["start_time"],
            data["end_time"]
        ))
        
        timetable_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": "Timetable entry created successfully",
            "timetable_id": timetable_id
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@timetable_bp.route("/timetable/<int:timetable_id>", methods=["PUT"])
@login_required
@faculty_only
def update_timetable_entry(timetable_id):
    """
    Update a timetable entry.
    
    PUT body:
        - Any timetable field to update
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    allowed_fields = ["subject_id", "faculty_id", "division_id", "day_of_week", 
                     "lecture_no", "room_no", "building_block", "start_time", "end_time"]
    
    updates = []
    params = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = %s")
            params.append(data[field])
    
    if not updates:
        return jsonify({"success": False, "message": "No fields to update"}), 400
    
    params.append(timetable_id)
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            f"UPDATE timetable SET {', '.join(updates)} WHERE timetable_id = %s",
            params
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Timetable entry updated successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@timetable_bp.route("/timetable/<int:timetable_id>", methods=["DELETE"])
@login_required
@faculty_only
def delete_timetable_entry(timetable_id):
    """
    Delete a timetable entry.
    
    Returns:
        JSON response with success status
    """
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM timetable WHERE timetable_id = %s", (timetable_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Timetable entry deleted successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
