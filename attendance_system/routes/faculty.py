"""
Faculty management routes
"""
from flask import Blueprint, jsonify, request, session
from ..db_manager import create_connection
from ..decorators.rbac import login_required, admin_only

faculty_bp = Blueprint("faculty", __name__, url_prefix="/api")


@faculty_bp.route("/faculty", methods=["GET"])
@login_required
def get_faculty():
    """
    Get list of faculty members with optional filters.
    
    Query params:
        - dept_id: Filter by department
    
    Returns:
        JSON response with faculty list
    """
    try:
        dept_id = request.args.get("dept_id")
        
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                f.faculty_id,
                f.user_id,
                u.name,
                u.email,
                u.mobile,
                f.short_name,
                f.dept_id,
                d.dept_name,
                u.is_approved
            FROM faculty f
            JOIN users u ON f.user_id = u.user_id
            LEFT JOIN department d ON f.dept_id = d.dept_id
            WHERE 1=1
        """
        
        params = []
        
        if dept_id:
            query += " AND f.dept_id = %s"
            params.append(dept_id)
        
        query += " ORDER BY u.name"
        
        cursor.execute(query, params)
        faculty = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "faculty": faculty})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@faculty_bp.route("/faculty/<int:faculty_id>", methods=["GET"])
@login_required
def get_faculty_member(faculty_id):
    """
    Get details of a specific faculty member.
    
    Returns:
        JSON response with faculty details
    """
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                f.faculty_id,
                f.user_id,
                u.name,
                u.email,
                u.mobile,
                f.short_name,
                f.dept_id,
                d.dept_name,
                u.is_approved,
                u.created_at
            FROM faculty f
            JOIN users u ON f.user_id = u.user_id
            LEFT JOIN department d ON f.dept_id = d.dept_id
            WHERE f.faculty_id = %s
        """, (faculty_id,))
        
        faculty_member = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not faculty_member:
            return jsonify({"success": False, "message": "Faculty not found"}), 404
        
        return jsonify({"success": True, "faculty": faculty_member})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@faculty_bp.route("/faculty/<int:faculty_id>", methods=["PUT"])
@login_required
@admin_only
def update_faculty(faculty_id):
    """
    Update faculty details.
    
    PUT body:
        - name: Faculty name
        - email: Faculty email
        - mobile: Faculty mobile
        - short_name: Short name/code
        - dept_id: Department ID
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Get user_id for this faculty
        cursor.execute("SELECT user_id FROM faculty WHERE faculty_id = %s", (faculty_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({"success": False, "message": "Faculty not found"}), 404
        
        user_id = result[0]
        
        # Update users table
        if "name" in data or "email" in data or "mobile" in data:
            updates = []
            params = []
            
            if "name" in data:
                updates.append("name = %s")
                params.append(data["name"])
            if "email" in data:
                updates.append("email = %s")
                params.append(data["email"])
            if "mobile" in data:
                updates.append("mobile = %s")
                params.append(data["mobile"])
            
            params.append(user_id)
            
            cursor.execute(
                f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s",
                params
            )
        
        # Update faculty table
        faculty_updates = []
        faculty_params = []
        
        if "short_name" in data:
            faculty_updates.append("short_name = %s")
            faculty_params.append(data["short_name"])
        if "dept_id" in data:
            faculty_updates.append("dept_id = %s")
            faculty_params.append(data["dept_id"])
        
        if faculty_updates:
            faculty_params.append(faculty_id)
            cursor.execute(
                f"UPDATE faculty SET {', '.join(faculty_updates)} WHERE faculty_id = %s",
                faculty_params
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Faculty updated successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@faculty_bp.route("/faculty/<int:faculty_id>/subjects", methods=["GET"])
@login_required
def get_faculty_subjects(faculty_id):
    """
    Get subjects assigned to a faculty member.
    
    Returns:
        JSON response with subject list
    """
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT DISTINCT
                s.subject_id,
                s.subject_code,
                s.subject_name,
                d.division_name
            FROM timetable t
            JOIN subject s ON t.subject_id = s.subject_id
            LEFT JOIN division d ON t.division_id = d.division_id
            WHERE t.faculty_id = %s
            ORDER BY s.subject_name
        """, (faculty_id,))
        
        subjects = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "subjects": subjects})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
