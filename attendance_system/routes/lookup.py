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

        cursor.execute(
            """
            SELECT
                semester_id AS id,
                CONCAT('Semester ', semester_no, ' ', academic_year) AS name,
                semester_id,
                semester_no,
                academic_year
            FROM semester
            ORDER BY semester_no
            """
        )
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
                """
                SELECT
                    division_id AS id,
                    division_name AS name,
                    division_id,
                    division_name,
                    dept_id
                FROM division
                WHERE dept_id = %s
                ORDER BY division_name
                """,
                (dept_id,),
            )
        else:
            cursor.execute(
                """
                SELECT
                    division_id AS id,
                    division_name AS name,
                    division_id,
                    division_name,
                    dept_id
                FROM division
                ORDER BY division_name
                """
            )

        divisions = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(divisions)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/subjects", methods=["GET"])
def list_subjects():
    """Return subjects, optionally filtered by department or semester."""
    dept_id = request.args.get("dept_id")
    semester_id = request.args.get("semester_id")

    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        where = []
        params = []
        if dept_id:
            where.append("dept_id = %s")
            params.append(dept_id)
        if semester_id:
            where.append("semester_id = %s")
            params.append(semester_id)

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        cursor.execute(
            f"""
            SELECT
                subject_id AS id,
                subject_name AS name,
                subject_id,
                subject_name,
                subject_code,
                dept_id,
                semester_id
            FROM subject
            {where_sql}
            ORDER BY subject_name
            """,
            params or None,
        )
        subjects = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(subjects)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500