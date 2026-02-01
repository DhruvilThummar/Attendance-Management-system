"""Registration API routes."""

from __future__ import annotations

from flask import render_template, request, jsonify
from werkzeug.security import generate_password_hash

from . import api
from ..db_manager import get_connection


@api.route("/registration", methods=["GET", "POST"])
def registration():
    """
    Registration route for new users.
    
    GET: Returns the registration page
    POST: Processes registration data and creates new user
    
    Returns:
        GET: register.html template
        POST: JSON response with success/error status
    """
    if request.method == "GET":
        return render_template("register.html")
    
    # POST - Handle registration submission
    data = request.get_json() or request.form
    
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role", "student")  # Default role
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    
    if not all([username, password, email, first_name, last_name]):
        return jsonify({"success": False, "message": "All fields are required"}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "Username already exists"}), 409
        
        # Hash password and insert new user
        password_hash = generate_password_hash(password)
        
        cursor.execute(
            """INSERT INTO users (username, password_hash, email, role, first_name, last_name)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (username, password_hash, email, role, first_name, last_name)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Registration successful",
            "redirect": "/api/login"
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500