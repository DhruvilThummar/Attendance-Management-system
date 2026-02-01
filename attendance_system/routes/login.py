"""Login API routes."""

from __future__ import annotations

from flask import render_template, request, jsonify, session
from werkzeug.security import check_password_hash

from . import api
from ..db_manager import get_connection


@api.route("/login", methods=["GET", "POST"])
def login():
    """
    Login route for authentication.
    
    GET: Returns the login page
    POST: Processes login credentials and creates session
    
    Returns:
        GET: login.html template
        POST: JSON response with success/error status
    """
    if request.method == "GET":
        return render_template("login.html")
    
    # POST - Handle login submission
    data = request.get_json() or request.form
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query user from database
        cursor.execute(
            "SELECT user_id, username, password_hash, role FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user["password_hash"], password):
            # Create session
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            
            return jsonify({
                "success": True,
                "message": "Login successful",
                "redirect": f"/dashboard/{user['role'].lower()}"
            })
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/logout", methods=["POST"])
def logout():
    """
    Logout route - Clears user session.
    
    Returns:
        JSON response with success status
    """
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"})
