"""Login API routes."""

from __future__ import annotations

from flask import request, jsonify, session
import hashlib

from werkzeug.security import check_password_hash, generate_password_hash

from . import api
from ..db_manager import create_connection


@api.route("/login", methods=["POST"])
@api.route("/auth/login", methods=["POST"])
def login():
    """Login route for authentication (JSON)."""
    data = request.get_json() or request.form
    identifier = data.get("email") or data.get("username")
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"success": False, "message": "Email/username and password required"}), 400

    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                u.user_id,
                u.name,
                u.email,
                u.mobile,
                u.password_hash,
                u.role_id,
                u.college_id,
                u.is_approved,
                r.role_name,
                c.college_name
            FROM users u
            JOIN role r ON u.role_id = r.role_id
            LEFT JOIN college c ON u.college_id = c.college_id
            WHERE u.email = %s OR u.name = %s
            LIMIT 1
            """,
            (identifier, identifier),
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

        password_hash = user["password_hash"]
        valid_password = check_password_hash(password_hash, password)

        # Legacy SHA256 fallback (older users created with SHA256 hashes)
        if not valid_password and len(password_hash) == 64:
            legacy_hash = hashlib.sha256(password.encode()).hexdigest()
            valid_password = legacy_hash == password_hash

            # Upgrade to werkzeug hash after successful legacy login
            if valid_password:
                try:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET password_hash = %s WHERE user_id = %s",
                        (generate_password_hash(password), user["user_id"]),
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                except Exception:
                    # Ignore upgrade failures; login will still succeed
                    pass

        if not valid_password:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

        if not user.get("is_approved"):
            return jsonify({"success": False, "message": "Account pending approval"}), 403

        session["user_id"] = user["user_id"]
        session["role"] = user["role_name"]
        session["email"] = user["email"]

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"],
                "phone": user.get("mobile"),
                "role_id": user["role_id"],
                "role_name": user["role_name"],
                "college_id": user.get("college_id"),
                "college_name": user.get("college_name"),
            },
            "redirect": "/dashboard"
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/auth/me", methods=["GET"])
@api.route("/me", methods=["GET"])
def me():
    """Return the current authenticated user (JSON)."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                u.user_id,
                u.name,
                u.email,
                u.mobile,
                u.role_id,
                r.role_name,
                u.college_id,
                c.college_name
            FROM users u
            JOIN role r ON u.role_id = r.role_id
            LEFT JOIN college c ON u.college_id = c.college_id
            WHERE u.user_id = %s
            LIMIT 1
            """,
            (user_id,),
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        return jsonify({
            "success": True,
            "user": {
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"],
                "phone": user.get("mobile"),
                "role_id": user["role_id"],
                "role_name": user["role_name"],
                "college_id": user.get("college_id"),
                "college_name": user.get("college_name"),
            }
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/logout", methods=["POST"])
@api.route("/auth/logout", methods=["POST"])
def logout():
    """Logout route - Clears user session."""
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"})
