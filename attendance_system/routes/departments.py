"""Departments API routes."""

from __future__ import annotations

from flask import render_template, request, jsonify

from . import api
from ..db_manager import get_connection
from ..decorators.rbac import login_required, admin_only


@api.route("/departments", methods=["GET"])
@login_required
def departments_page():
    """
    Departments page route.
    
    Returns:
        departments.html template
    """
    return render_template("departments.html")


@api.route("/departments/list", methods=["GET"])
@login_required
def list_departments():
    """
    Get list of all departments.
    
    Returns:
        JSON response with departments list
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                department_id,
                department_name,
                department_code,
                hod_id,
                created_at
            FROM departments
            ORDER BY department_name
        """)
        
        departments = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "departments": departments})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/departments/create", methods=["POST"])
@login_required
@admin_only
def create_department():
    """
    Create a new department.
    
    POST body:
        - department_name: Name of the department
        - department_code: Short code for the department
        - hod_id: Head of Department user ID (optional)
    
    Returns:
        JSON response with success status
    """
    data = request.get_json()
    
    department_name = data.get("department_name")
    department_code = data.get("department_code")
    hod_id = data.get("hod_id")
    
    if not all([department_name, department_code]):
        return jsonify({"success": False, "message": "Department name and code are required"}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO departments (department_name, department_code, hod_id)
               VALUES (%s, %s, %s)""",
            (department_name, department_code, hod_id)
        )
        
        conn.commit()
        department_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Department created successfully",
            "department_id": department_id
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/departments/<int:department_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def manage_department(department_id):
    """
    Get, update, or delete a specific department.
    
    GET: Get department details
    PUT: Update department
    DELETE: Delete department
    
    Returns:
        JSON response with department data or success status
    """
    if request.method == "GET":
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM departments WHERE department_id = %s",
                (department_id,)
            )
            department = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if department:
                return jsonify({"success": True, "department": department})
            else:
                return jsonify({"success": False, "message": "Department not found"}), 404
                
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    
    elif request.method == "PUT":
        # Update department - requires admin privileges
        data = request.get_json()
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            update_fields = []
            values = []
            
            if "department_name" in data:
                update_fields.append("department_name = %s")
                values.append(data["department_name"])
            if "department_code" in data:
                update_fields.append("department_code = %s")
                values.append(data["department_code"])
            if "hod_id" in data:
                update_fields.append("hod_id = %s")
                values.append(data["hod_id"])
            
            if not update_fields:
                return jsonify({"success": False, "message": "No fields to update"}), 400
            
            values.append(department_id)
            query = f"UPDATE departments SET {', '.join(update_fields)} WHERE department_id = %s"
            
            cursor.execute(query, values)
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return jsonify({"success": True, "message": "Department updated successfully"})
            
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    
    elif request.method == "DELETE":
        # Delete department - requires admin privileges
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM departments WHERE department_id = %s", (department_id,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return jsonify({"success": True, "message": "Department deleted successfully"})
            
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500