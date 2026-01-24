"""HOD-specific routes."""
from __future__ import annotations
from flask import Blueprint, render_template, request, flash, g, redirect, url_for, current_app
import os
from ..app import role_required
from ..models.hod import HOD
from ..services.report_service import generate_defaulter_report
from ..services.rules_service import get_defaulters_list
from ..db_manager import fetch_one, execute

bp = Blueprint("hod", __name__)

@bp.route("/")
@role_required("HOD")
def dashboard():
    try:
        user_id = g.user['id']
        
        # Get HOD's college_id
        college_row = fetch_one("SELECT college_id FROM users WHERE id = %s", (user_id,))
        if not college_row or not college_row[0]:
            flash("HOD college information not found. Please contact administrator.", "danger")
            return render_template("hod/dashboard.html", stats={}, pending_approvals=[], faculties=[], events=[])
        
        college_id = college_row[0]
        
        # Get HOD department
        hod_row = fetch_one(f"SELECT department_id FROM {HOD.__table__} WHERE user_id = %s", (user_id,))
        dept_id = hod_row[0] if hod_row else None
        
        # Calculate Real Statistics (filtered by college)
        # Total Students in this college
        total_students_row = fetch_one("""
            SELECT COUNT(*) FROM students s
            JOIN users u ON s.user_id = u.id
            WHERE u.college_id = %s
        """, (college_id,))
        total_students = total_students_row[0] if total_students_row else 0
        
        # Average Attendance (college-wide)
        avg_attendance_row = fetch_one("""
            SELECT AVG(
                CASE 
                    WHEN l.id IS NOT NULL THEN 
                        (SELECT COUNT(*) FROM attendance WHERE lecture_id = l.id AND status = 'Present') * 100.0 / 
                        NULLIF((SELECT COUNT(*) FROM attendance WHERE lecture_id = l.id), 0)
                    ELSE 0 
                END
            ) as avg_att
            FROM lectures l
            JOIN timetable t ON l.timetable_id = t.id
            JOIN divisions d ON t.division_id = d.id
            WHERE d.college_id = %s AND l.date <= CURRENT_DATE
        """, (college_id,))
        avg_attendance = round(avg_attendance_row[0], 1) if avg_attendance_row and avg_attendance_row[0] else 0.0
        
        # Count Defaulters (students with <75% attendance)
        defaulters_count_row = fetch_one("""
            SELECT COUNT(DISTINCT s.id) FROM students s
            JOIN users u ON s.user_id = u.id
            WHERE u.college_id = %s
            AND (
                SELECT COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)
                FROM attendance a
                JOIN lectures l ON a.lecture_id = l.id
                WHERE a.student_id = s.id
            ) < 75
        """, (college_id,))
        defaulters_count = defaulters_count_row[0] if defaulters_count_row else 0
        
        stats = {
            'total_students': total_students,
            'avg_attendance': avg_attendance,
            'defaulters_count': defaulters_count
        }
        
        # HOD approves Faculty (filtered by college)
        pending_rows = execute("""
            SELECT id, email, role FROM users 
            WHERE role = 'Faculty' AND is_approved = FALSE AND college_id = %s
        """, (college_id,))
        pending_approvals = [{"id": r[0], "email": r[1], "role": r[2]} for r in pending_rows]
        
        # Fetch Faculties for Proxy Dropdown (filtered by college)
        fac_rows = execute("""
            SELECT f.id, COALESCE(u.name, u.email) as name 
            FROM faculties f 
            JOIN users u ON f.user_id = u.id
            WHERE u.college_id = %s
        """, (college_id,))
        faculties = [{"id": r[0], "name": r[1]} for r in fac_rows]
        
        # Fetch Upcoming Events (filtered by college)
        event_rows = execute("""
            SELECT title, start_date, type FROM academic_calendar 
            WHERE start_date >= CURRENT_DATE AND college_id = %s
            ORDER BY start_date ASC LIMIT 5
        """, (college_id,))
        events = [{"title": r[0], "date": r[1], "type": r[2]} for r in event_rows]
        
        return render_template("hod/dashboard.html", 
                             stats=stats, 
                             pending_approvals=pending_approvals, 
                             faculties=faculties, 
                             events=events)
    
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        return render_template("hod/dashboard.html", stats={}, pending_approvals=[], faculties=[], events=[])

@bp.route("/approve/<int:user_id>", methods=["POST"])
@role_required("HOD")
def approve_user(user_id):
    try:
        user = fetch_one("SELECT role, college_id FROM users WHERE id = %s", (user_id,))
        if user and user[0] == 'Faculty':
            # Get HOD's department for default assignment
            hod_user_id = g.user['id']
            hod_dept = fetch_one(f"SELECT department_id FROM {HOD.__table__} WHERE user_id = %s", (hod_user_id,))
            dept = hod_dept[0] if hod_dept and hod_dept[0] else 'General'
            
            # Approve user
            execute("UPDATE users SET is_approved = TRUE WHERE id = %s", (user_id,))
            
            # Create faculty record with proper department
            # Check if faculty record already exists
            existing = fetch_one("SELECT id FROM faculties WHERE user_id = %s", (user_id,))
            if not existing:
                execute("INSERT INTO faculties (user_id, department) VALUES (%s, %s)", (user_id, str(dept)))
            
            flash("Faculty approved successfully.", "success")
        else:
            flash("Invalid approval request.", "danger")
    except Exception as e:
        flash(f"Error approving faculty: {str(e)}", "danger")
    
    return redirect(url_for("hod.dashboard"))

@bp.route("/reject/<int:user_id>", methods=["POST"])
@role_required("HOD")
def reject_user(user_id):
    user = fetch_one("SELECT role FROM users WHERE id = %s", (user_id,))
    if user and user[0] == 'Faculty':
        execute("DELETE FROM users WHERE id = %s", (user_id,))
        flash("Faculty request rejected.", "warning")
    else:
        flash("Invalid request.", "danger")
    return redirect(url_for("hod.dashboard"))

@bp.route("/add_student", methods=["POST"])
@role_required("HOD")
def add_student():
    name = request.form.get("name")
    enrollment = request.form.get("enrollment")
    phone = request.form.get("phone")
    mentor = request.form.get("mentor")
    roll_no = request.form.get("roll_no")
    branch = request.form.get("branch")
    
    if not all([name, enrollment, roll_no]):
        flash("Name, Enrollment, and Roll No are required.", "danger")
        return redirect(url_for("hod.dashboard"))
        
    email = f"{enrollment}@mail.ljku.edu.in".lower()
    password = "StudentPassword123!" # Default password
    
    try:
        from ..models.user import User
        from ..models.student import Student
        
        # Get College ID from logged-in HOD
        user_id = g.user['id']
        # Fetch HOD's college_id via Users table JOIN or directly if stored in session/g.user
        # Assuming HOD user has college_id set.
        current_college_id = fetch_one("SELECT college_id FROM users WHERE id=%s", (user_id,))[0]
        
        # Check if user exists
        exists = fetch_one("SELECT id FROM users WHERE email = %s", (email,))
        if exists:
            flash(f"Student with email {email} already exists.", "warning")
            return redirect(url_for("hod.dashboard"))

        # Create User linked to College
        user = User(email=email, password=password, role="Student", is_approved=True, college_id=current_college_id)
        user.save()
        # Update name manually
        execute("UPDATE users SET name=%s WHERE id=%s", (name, user.id))
        
        # Create Student
        student = Student(user_id=user.id, enrollment_no=enrollment, roll_no=roll_no, branch=branch, phone_number=phone, mentor_name=mentor)
        student.save()
        
        flash(f"Student {name} added successfully. Email: {email}", "success")
        
    except Exception as e:
        flash(f"Error adding student: {e}", "danger")
        
    return redirect(url_for("hod.dashboard"))

@bp.route("/reports/defaulters")
@role_required("HOD")
def download_defaulter_list():
    try:
        # Get College ID
        user_id = g.user['id']
        current_college_id = fetch_one("SELECT college_id FROM users WHERE id=%s", (user_id,))[0]
        
        defs = get_defaulters_list(current_college_id, 1) # College ID dynamic, Dept ID still hardcoded/todo
        path = generate_defaulter_report(current_college_id, defs)
        
        if not os.path.isabs(path):
             path = os.path.join(current_app.root_path, '..', path)
             
        from flask import send_file
        return send_file(path, as_attachment=True, download_name="defaulter_list.pdf")
    except Exception as e:
        flash(f"Error generating report: {e}", "danger")
        return redirect(url_for("hod.dashboard"))

@bp.route("/reports/faculty_performance")
@role_required("HOD")
def download_faculty_report():
    import csv
    import io
    from flask import Response
    
    # Filter by college? Ideally yes.
    user_id = g.user['id']
    current_college_id = fetch_one("SELECT college_id FROM users WHERE id=%s", (user_id,))[0]

    rows = execute("""
        SELECT s.name as subject, u.name as faculty, COUNT(l.id) as lectures_taken
        FROM timetable t
        JOIN subjects s ON t.subject_id = s.id
        JOIN faculties f ON t.faculty_id = f.id
        JOIN users u ON f.user_id = u.id
        LEFT JOIN lectures l ON t.id = l.timetable_id AND l.date <= CURRENT_DATE
        WHERE s.college_id = %s
        GROUP BY s.name, u.name
    """, (current_college_id,))
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Subject', 'Faculty', 'Lectures Taken'])
    writer.writerows(rows)
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=faculty_performance.csv"}
    )

@bp.route("/add_timetable", methods=["POST"])
@role_required("HOD")
def add_timetable():
    day = request.form.get("day")
    slot = request.form.get("slot")
    sub_code = request.form.get("subject_code")
    fac_ident = request.form.get("faculty_identifier")
    div_name = request.form.get("division_name")
    
    try:
        user_id = g.user['id']
        current_college_id = fetch_one("SELECT college_id FROM users WHERE id=%s", (user_id,))[0]
        
        # Resolve IDs (Scoped to College)
        sub = fetch_one("SELECT id FROM subjects WHERE code=%s AND college_id=%s", (sub_code, current_college_id))
        if not sub:
            flash(f"Subject {sub_code} not found in your college.", "danger")
            return redirect(url_for("hod.dashboard"))
            
        div = fetch_one("SELECT id FROM divisions WHERE name=%s AND college_id=%s", (div_name, current_college_id))
        if not div:
             flash(f"Division {div_name} not found in your college.", "danger")
             return redirect(url_for("hod.dashboard"))
             
        # Resolve Faculty
        fac = fetch_one("""
            SELECT f.id FROM faculties f 
            JOIN users u ON f.user_id = u.id 
            WHERE (u.email = %s OR f.short_name = %s) AND u.college_id = %s
        """, (fac_ident, fac_ident, current_college_id))
        
        if not fac:
            flash(f"Faculty {fac_ident} not found in your college.", "danger")
            return redirect(url_for("hod.dashboard"))
            
        execute("INSERT INTO timetable (subject_id, faculty_id, division_id, day, slot) VALUES (%s, %s, %s, %s, %s)",
                (sub[0], fac[0], div[0], day, slot))
        
        flash("Timetable entry added successfully.", "success")
    except Exception as e:
        flash(f"Error adding timetable: {e}", "danger")
        
    return redirect(url_for("hod.dashboard"))

@bp.route("/add_calendar_event", methods=["POST"])
@role_required("HOD")
def add_calendar_event():
    title = request.form.get("title")
    etype = request.form.get("type")
    start = request.form.get("start_date")
    end = request.form.get("end_date") or start
    
    try:
        user_id = g.user['id']
        current_college_id = fetch_one("SELECT college_id FROM users WHERE id=%s", (user_id,))[0]
        
        execute("INSERT INTO academic_calendar (college_id, title, type, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
                (current_college_id, title, etype, start, end))
        flash("Event added to Academic Calendar.", "success")
    except Exception as e:
        flash(f"Error adding event: {e}", "danger")
        
    return redirect(url_for("hod.dashboard"))

@bp.route("/assign_proxy", methods=["POST"])
@role_required("HOD")
def assign_proxy():
    absent_id = request.form.get("absent_faculty")
    proxy_id = request.form.get("proxy_faculty")
    date_str = request.form.get("date")
    slot = request.form.get("slot")
    
    if not all([absent_id, proxy_id, date_str, slot]):
        flash("All fields are required.", "danger")
        return redirect(url_for("hod.dashboard"))
        
    try:
        # Find the lecture
        # Join lectures with timetable to match faculty and slot
        # We need to find the lecture ID to update it.
        # But lectures might not be generated yet? Assuming they are.
        # Or we update timetable entry for that day? No, proxy is usually one-off.
        # So we look in `lectures` table.
        
        query = """
            SELECT l.id FROM lectures l
            JOIN timetable t ON l.timetable_id = t.id
            WHERE l.date = %s AND t.faculty_id = %s AND t.slot = %s
        """
        lecture = fetch_one(query, (date_str, absent_id, slot))
        
        if not lecture:
            # If lecture row doesn't exist, we might need to find the timetable and handle 'Generate' or it's just not there.
            # Assuming lectures are generated.
            flash("Lecture not found for this date/faculty/slot. Ensure schedule is generated.", "warning")
            return redirect(url_for("hod.dashboard"))
            
        execute("UPDATE lectures SET proxy_faculty_id = %s WHERE id = %s", (proxy_id, lecture[0]))
        flash("Proxy assigned successfully.", "success")
        
    except Exception as e:
        flash(f"Error assigning proxy: {e}", "danger")
        
    return redirect(url_for("hod.dashboard"))
