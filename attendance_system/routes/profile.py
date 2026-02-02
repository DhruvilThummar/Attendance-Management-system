"""
Profile management routes
"""
from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from ..db_manager import create_connection
from ..decorators.rbac import login_required

profile_bp = Blueprint("profile", __name__, url_prefix="/api")


@profile_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    """
    Get current user's profile information.
    
    Returns:
        JSON response with user profile
    """
    try:
        user_id = session.get("user_id")
        
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get basic user info
        cursor.execute("""
            SELECT 
                u.user_id,
                u.name,
                u.email,
                u.mobile,
                u.role_id,
                r.role_name,
                u.college_id,
                c.college_name,
                u.is_approved,
                u.created_at
            FROM users u
            JOIN role r ON u.role_id = r.role_id
            LEFT JOIN college c ON u.college_id = c.college_id
            WHERE u.user_id = %s
        """, (user_id,))
        
        profile = cursor.fetchone()
        
        if not profile:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Get role-specific info
        role_id = profile["role_id"]
        
        if role_id == 3:  # Faculty
            cursor.execute("""
                SELECT 
                    f.faculty_id,
                    f.short_name,
                    f.dept_id,
                    d.dept_name
                FROM faculty f
                LEFT JOIN department d ON f.dept_id = d.dept_id
                WHERE f.user_id = %s
            """, (user_id,))
            faculty_info = cursor.fetchone()
            if faculty_info:
                profile["faculty_info"] = faculty_info
        
        elif role_id == 4:  # Student
            cursor.execute("""
                SELECT 
                    s.student_id,
                    s.enrollment_no,
                    s.roll_no,
                    s.dept_id,
                    d.dept_name,
                    s.division_id,
                    div.division_name,
                    s.semester_id,
                    sem.semester_name,
                    s.mentor_id
                FROM student s
                LEFT JOIN department d ON s.dept_id = d.dept_id
                LEFT JOIN division div ON s.division_id = div.division_id
                LEFT JOIN semester sem ON s.semester_id = sem.semester_id
                WHERE s.user_id = %s
            """, (user_id,))
            student_info = cursor.fetchone()
            if student_info:
                profile["student_info"] = student_info
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "profile": profile})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@profile_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    """
    Update current user's profile information.
    
    PUT body:
        - name: User's name
        - mobile: User's mobile number
        - email: User's email (if allowed)
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    user_id = session.get("user_id")
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if "name" in data:
            updates.append("name = %s")
            params.append(data["name"])
        
        if "mobile" in data:
            updates.append("mobile = %s")
            params.append(data["mobile"])
        
        if "email" in data:
            # Check if email is already taken by another user
            cursor.execute(
                "SELECT user_id FROM users WHERE email = %s AND user_id != %s",
                (data["email"], user_id)
            )
            if cursor.fetchone():
                return jsonify({"success": False, "message": "Email already in use"}), 400
            
            updates.append("email = %s")
            params.append(data["email"])
        
        if not updates:
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        params.append(user_id)
        
        cursor.execute(
            f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s",
            params
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Profile updated successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@profile_bp.route("/profile/password", methods=["PUT"])
@login_required
def change_password():
    """
    Change current user's password.
    
    PUT body:
        - current_password: Current password
        - new_password: New password
        - confirm_password: Confirmation of new password
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    user_id = session.get("user_id")
    
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")
    
    if not all([current_password, new_password, confirm_password]):
        return jsonify({"success": False, "message": "All fields are required"}), 400
    
    if new_password != confirm_password:
        return jsonify({"success": False, "message": "New passwords do not match"}), 400
    
    if len(new_password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters"}), 400
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Verify current password
        cursor.execute("SELECT password_hash FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        if not check_password_hash(result[0], current_password):
            return jsonify({"success": False, "message": "Current password is incorrect"}), 400
        
        # Update password
        new_hash = generate_password_hash(new_password)
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE user_id = %s",
            (new_hash, user_id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Password changed successfully"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
