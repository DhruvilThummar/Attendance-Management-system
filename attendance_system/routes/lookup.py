"""Lookup API routes for registration dropdowns."""

from __future__ import annotations

from flask import request, jsonify

from . import api
from ..db_manager import create_connection


@api.route("/roles", methods=["GET"])
def list_roles():
    """Return available roles."""
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT role_id, role_name FROM role ORDER BY role_name")
        roles = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(roles)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/colleges", methods=["GET"])
def list_colleges():
    """Return available colleges."""
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT college_id, college_name FROM college ORDER BY college_name")
        colleges = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(colleges)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/semesters", methods=["GET"])
def list_semesters():
    """Return available semesters."""
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT semester_id, semester_no, academic_year FROM semester ORDER BY semester_no")
        semesters = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(semesters)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/divisions", methods=["GET"])
def list_divisions():
    """Return divisions, optionally filtered by department."""
    dept_id = request.args.get("dept_id")

    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        if dept_id:
            cursor.execute(
                "SELECT division_id, division_name, dept_id FROM division WHERE dept_id = %s ORDER BY division_name",
                (dept_id,),
            )
        else:
            cursor.execute(
                "SELECT division_id, division_name, dept_id FROM division ORDER BY division_name"
            )

        divisions = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(divisions)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500