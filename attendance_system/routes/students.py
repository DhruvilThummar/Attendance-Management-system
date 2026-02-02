"""
Student management routes
"""
from flask import Blueprint, jsonify, request, session
from ..db_manager import create_connection
from ..decorators.rbac import login_required, faculty_only

students_bp = Blueprint("students", __name__, url_prefix="/api")


@students_bp.route("/students", methods=["GET"])
@login_required
def get_students():
    """
    Get list of students with optional filters.
    
    Query params:
        - division_id: Filter by division
        - dept_id: Filter by department
        - semester_id: Filter by semester
    
    Returns:
        JSON response with student list
    """
    try:
        division_id = request.args.get("division_id")
        dept_id = request.args.get("dept_id")
        semester_id = request.args.get("semester_id")
        
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                s.student_id,
                s.user_id,
                u.name,
                u.email,
                u.mobile,
                s.enrollment_no,
                s.roll_no,
                s.dept_id,
                d.dept_name,
                s.division_id,
                div.division_name,
                s.semester_id,
                sem.semester_name,
                u.is_approved
            FROM student s
            JOIN users u ON s.user_id = u.user_id
            LEFT JOIN department d ON s.dept_id = d.dept_id
            LEFT JOIN division div ON s.division_id = div.division_id
            LEFT JOIN semester sem ON s.semester_id = sem.semester_id
            WHERE 1=1
        """
        
        params = []
        
        if division_id:
            query += " AND s.division_id = %s"
            params.append(division_id)
        
        if dept_id:
            query += " AND s.dept_id = %s"
            params.append(dept_id)
        
        if semester_id:
            query += " AND s.semester_id = %s"
            params.append(semester_id)
        
        query += " ORDER BY s.roll_no"
        
        cursor.execute(query, params)
        students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "students": students})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@students_bp.route("/students/<int:student_id>", methods=["GET"])
@login_required
def get_student(student_id):
    """
    Get details of a specific student.
    
    Returns:
        JSON response with student details
    """
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                s.student_id,
                s.user_id,
                u.name,
                u.email,
                u.mobile,
                s.enrollment_no,
                s.roll_no,
                s.dept_id,
                d.dept_name,
                s.division_id,
                div.division_name,
                s.semester_id,
                sem.semester_name,
                s.mentor_id,
                u.is_approved,
                u.created_at
            FROM student s
            JOIN users u ON s.user_id = u.user_id
            LEFT JOIN department d ON s.dept_id = d.dept_id
            LEFT JOIN division div ON s.division_id = div.division_id
            LEFT JOIN semester sem ON s.semester_id = sem.semester_id
            WHERE s.student_id = %s
        """, (student_id,))
        
        student = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not student:
            return jsonify({"success": False, "message": "Student not found"}), 404
        
        return jsonify({"success": True, "student": student})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@students_bp.route("/students/<int:student_id>", methods=["PUT"])
@login_required
@faculty_only
def update_student(student_id):
    """
    Update student details.
    
    PUT body:
        - name: Student name
        - email: Student email
        - mobile: Student mobile
        - roll_no: Roll number
        - division_id: Division
        - semester_id: Semester
        - mentor_id: Mentor faculty ID
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Get user_id for this student
        cursor.execute("SELECT user_id FROM student WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({"success": False, "message": "Student not found"}), 404
        
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
        
        # Update student table
        student_updates = []
        student_params = []
        
        if "roll_no" in data:
            student_updates.append("roll_no = %s")
            student_params.append(data["roll_no"])
        if "division_id" in data:
            student_updates.append("division_id = %s")
            student_params.append(data["division_id"])
        if "semester_id" in data:
            student_updates.append("semester_id = %s")
            student_params.append(data["semester_id"])
        if "mentor_id" in data:
            student_updates.append("mentor_id = %s")
            student_params.append(data["mentor_id"])
        
        if student_updates:
            student_params.append(student_id)
            cursor.execute(
                f"UPDATE student SET {', '.join(student_updates)} WHERE student_id = %s",
                student_params
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Student updated successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
