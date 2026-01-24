"""Admin-specific routes."""
from __future__ import annotations
from datetime import date, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from ..app import role_required
from ..db_manager import fetch_one, execute
from ..services.calendar_service import generate_lectures
from ..services.schedule_parser_service import parse_schedule_pdf, save_extracted_schedule

bp = Blueprint("admin", __name__)

@bp.route("/")
@role_required("CollegeAdmin")
def dashboard():
    # Fetch stats
    stats = {}
    stats['students'] = fetch_one("SELECT COUNT(*) FROM students")[0]
    stats['faculty'] = fetch_one("SELECT COUNT(*) FROM faculties")[0] 
    stats['subjects'] = fetch_one("SELECT COUNT(*) FROM subjects")[0]
    
    # Fetch pending approvals (HODs only for Admin)
    # Admin approves HODs
    pending_rows = execute("SELECT id, email, role FROM users WHERE role = 'HOD' AND is_approved = FALSE")
    pending_approvals = [{"id": r[0], "email": r[1], "role": r[2]} for r in pending_rows]
    
    # Get all divisions for upload form
    div_rows = execute("SELECT id, name FROM divisions")
    divisions = [{"id": r[0], "name": r[1]} for r in div_rows]
    
    return render_template("admin/dashboard.html", stats=stats, pending_approvals=pending_approvals, divisions=divisions)

@bp.route("/upload_timetable", methods=["POST"])
@role_required("CollegeAdmin")
def upload_timetable():
    if 'timetable_pdf' not in request.files:
        flash("No file part", "danger")
        return redirect(url_for("admin.dashboard"))
        
    file = request.files['timetable_pdf']
    division_id = request.form.get('division_id')
    
    if file.filename == '' or not division_id:
        flash("No selected file or division", "danger")
        return redirect(url_for("admin.dashboard"))
        
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        # Ensure upload folder exists
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_path, exist_ok=True)
        
        filepath = os.path.join(upload_path, filename)
        file.save(filepath)
        
        try:
            entries = parse_schedule_pdf(filepath)
            count = save_extracted_schedule(entries, int(division_id))
            flash(f"Successfully extracted {count} schedule entries from PDF!", "success")
        except Exception as e:
            flash(f"Error parsing PDF: {e}", "danger")
            
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
            
    else:
        flash("Invalid file type. Please upload a PDF.", "danger")
        
    return redirect(url_for("admin.dashboard"))

@bp.route("/approve/<int:user_id>", methods=["POST"])
@role_required("CollegeAdmin")
def approve_user(user_id):
    user = fetch_one("SELECT role FROM users WHERE id = %s", (user_id,))
    if user and user[0] == 'HOD':
        execute("UPDATE users SET is_approved = TRUE WHERE id = %s", (user_id,))
        execute("INSERT INTO hods (user_id) VALUES (%s)", (user_id,))
        flash("HOD approved successfully.", "success")
    else:
        flash("Invalid approval request.", "danger")
    return redirect(url_for("admin.dashboard"))

@bp.route("/reject/<int:user_id>", methods=["POST"])
@role_required("CollegeAdmin")
def reject_user(user_id):
    user = fetch_one("SELECT role FROM users WHERE id = %s", (user_id,))
    if user and user[0] == 'HOD':
        execute("DELETE FROM users WHERE id = %s", (user_id,))
        flash("Request rejected and deleted.", "warning")
    else:
        flash("Invalid rejection request.", "danger")
    return redirect(url_for("admin.dashboard"))

@bp.route("/generate_schedule", methods=["POST"])
@role_required("CollegeAdmin")
def generate_schedule():
    today = date.today()
    end = today + timedelta(days=7)
    try:
        count = generate_lectures(today, end)
        flash(f"Successfully generated {count} lectures for {today} to {end}.", "success")
    except Exception as e:
        flash(f"Error generating lectures: {e}", "danger")
    return redirect(url_for("admin.dashboard"))
