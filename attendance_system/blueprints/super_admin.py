"""Super Admin routes for managing colleges."""
from __future__ import annotations
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..app import role_required
from ..db_manager import execute, fetch_one

bp = Blueprint("super_admin", __name__)

@bp.route("/")
@role_required("SuperAdmin")
def dashboard():
    # Fetch stats
    stats = {}
    stats['active_colleges'] = fetch_one("SELECT COUNT(*) FROM colleges WHERE subscription_status = 'Active'")[0]
    stats['total_users'] = fetch_one("SELECT COUNT(*) FROM users")[0]
    
    # List all colleges
    colleges_rows = execute("SELECT id, name, subscription_status, created_at FROM colleges ORDER BY created_at DESC")
    colleges = [{"id": r[0], "name": r[1], "status": r[2], "created_at": r[3]} for r in colleges_rows]
    
    return render_template("super_admin/dashboard.html", stats=stats, colleges=colleges)

@bp.route("/add_college", methods=["POST"])
@role_required("SuperAdmin")
def add_college():
    name = request.form.get("name")
    if not name:
        flash("College name is required", "danger")
        return redirect(url_for("super_admin.dashboard"))
        
    try:
        execute("INSERT INTO colleges (name) VALUES (%s)", (name,))
        flash(f"College '{name}' added successfully.", "success")
    except Exception as e:
        flash(f"Error adding college: {e}", "danger")
        
    return redirect(url_for("super_admin.dashboard"))

@bp.route("/delete_college/<int:college_id>", methods=["POST"])
@role_required("SuperAdmin")
def delete_college(college_id):
    try:
        execute("DELETE FROM colleges WHERE id = %s", (college_id,))
        flash("College deleted.", "warning")
    except Exception as e:
        flash(f"Error deleting college: {e}", "danger")
    return redirect(url_for("super_admin.dashboard"))
