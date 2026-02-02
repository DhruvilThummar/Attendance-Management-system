"""Registration API routes."""

from __future__ import annotations

from flask import request, jsonify
from werkzeug.security import generate_password_hash

from . import api
from ..db_manager import create_connection


@api.route("/registration", methods=["POST"])
@api.route("/auth/register", methods=["POST"])
def registration():
    """Registration route for new users (JSON)."""
    data = request.get_json() or request.form

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    mobile = data.get("mobile")
    college_id = data.get("college_id")
    role_id = data.get("role_id")

    if not all([name, email, password, college_id, role_id]):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "Email already exists"}), 409

        # Hash password and insert new user
        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (college_id, name, email, password_hash, mobile, role_id, is_approved)
            VALUES (%s, %s, %s, %s, %s, %s, 0)
            """,
            (college_id, name, email, password_hash, mobile, role_id),
        )
        user_id = cursor.lastrowid

        # Role-specific inserts (optional)
        if str(role_id) == "3":  # FACULTY
            dept_id = data.get("dept_id")
            if dept_id:
                cursor.execute(
                    """
                    INSERT INTO faculty (user_id, dept_id, short_name)
                    VALUES (%s, %s, %s)
                    """,
                    (user_id, dept_id, name.split(" ")[0]),
                )
        elif str(role_id) == "4":  # STUDENT
            dept_id = data.get("dept_id")
            division_id = data.get("division_id")
            enrollment_no = data.get("enrollment_no")
            roll_no = data.get("roll_no")
            semester_id = data.get("semester_id")

            if all([dept_id, division_id, enrollment_no, roll_no, semester_id]):
                cursor.execute(
                    """
                    INSERT INTO student (user_id, dept_id, division_id, enrollment_no, roll_no, semester_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (user_id, dept_id, division_id, enrollment_no, roll_no, semester_id),
                )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Registration successful. Await admin approval.",
            "redirect": "/login"
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
