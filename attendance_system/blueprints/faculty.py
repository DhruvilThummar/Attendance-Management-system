"""Faculty-specific routes."""
from __future__ import annotations
from flask import Blueprint, render_template, g, redirect, url_for, flash, request
from ..app import role_required
from ..db_manager import execute, fetch_one

bp = Blueprint("faculty", __name__)

@bp.route("/")
@role_required("Faculty")
def dashboard():
    user_id = g.user['id']
    from datetime import date
    
    # Get date from request or default to today
    selected_date_str = request.args.get('date')
    if selected_date_str:
        selected_date = selected_date_str
    else:
        selected_date = date.today().isoformat()
        
    # Determine the Day of Week (e.g. "Monday")
    from datetime import datetime
    dt = datetime.strptime(selected_date, '%Y-%m-%d')
    day_name = dt.strftime('%A')
    
    # Find Faculty ID
    try:
        faculty = fetch_one("SELECT id FROM faculties WHERE user_id = %s", (user_id,))
        if not faculty:
            # Fallback for demo if not properly linked (though seed does it)
            faculty_id = 999 
        else:
            faculty_id = faculty[0]
            
        # 1. Get Timetable entries for this Faculty and Day
        # Join with Subjects and Divisions
        # Query: timetable(id, slot) + subjects(name, code) + divisions(name)
        # Note: 'lectures' table is for specific generated dates. 
        # If we use generated lectures, we query 'lectures' table.
        # Let's use the 'lectures' table as the source of truth for "Today's Schedule".
        # If no lectures exist, we fall back to timetable template? 
        # The user requested "select date". So we should look at 'lectures' table which has `date`.
        
        rows = execute("""
            SELECT l.id, t.slot, s.name, s.code, d.name, 
                   (SELECT COUNT(*) FROM attendance a WHERE a.lecture_id = l.id) as marked_count
            FROM lectures l
            JOIN timetable t ON l.timetable_id = t.id
            JOIN subjects s ON t.subject_id = s.id
            JOIN divisions d ON t.division_id = d.id
            WHERE t.faculty_id = %s AND l.date = %s
            ORDER BY t.slot
        """, (faculty_id, selected_date))
        
        lectures = []
        for r in rows:
            lectures.append({
                "id": r[0],
                "slot": r[1],
                "subject": f"{r[3]} - {r[2]}",
                "division": r[4],
                "status": "Completed" if r[5] > 0 else "Pending"
            })
            
    except Exception as e:
        print(f"Error fetching dashboard: {e}")
        lectures = []
    
    # Faculty approves Students
    pending_rows = execute("SELECT id, email, role FROM users WHERE role = 'Student' AND is_approved = FALSE")
    pending_approvals = [{"id": r[0], "email": r[1], "role": r[2]} for r in pending_rows]
    
    return render_template("faculty/dashboard.html", lectures=lectures, pending_approvals=pending_approvals, selected_date=selected_date)

@bp.route("/attendance/<int:lecture_id>", methods=["GET", "POST"])
@role_required("Faculty")
def mark_attendance(lecture_id):
    if request.method == "POST":
        # Process attendance form
        # Form data: student_id: status (P/A)
        try:
            # Clean old attendance for this lecture if re-marking
            # execute("DELETE FROM attendance WHERE lecture_id = %s", (lecture_id,))
            
            # Simple loop over form keys
            count = 0
            for key, value in request.form.items():
                if key.startswith("student_"):
                    student_id = int(key.split("_")[1])
                    status = value
                    # Insert or update
                    # For simplicity, assuming nice inputs
                    # In real app, batch insert
                    execute("""
                        INSERT INTO attendance (lecture_id, student_id, status)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE status = %s
                    """, (lecture_id, student_id, status, status))
                    count += 1
            flash(f"Attendance marked for {count} students.", "success")
            return redirect(url_for("faculty.dashboard"))
        except Exception as e:
            flash(f"Error marking attendance: {e}", "danger")

    # Fetch students for this lecture (mock logic: fetch all students in Div A for now)
    # real logic: lecture -> timetable -> division -> students
    # But since lecture table is empty/mocked in dashboard, let's just fetch all students.
    students_rows = execute("""
        SELECT s.id, u.email, s.enrollment_no, s.roll_no, s.branch,
               (SELECT status FROM attendance WHERE lecture_id = %s AND student_id = s.id) as current_status
        FROM students s
        JOIN users u ON s.user_id = u.id
    """, (lecture_id,))
    students = [{
        "id": r[0], 
        "name": r[1].split('@')[0], 
        "enrollment": r[2],
        "roll_no": r[3] or "N/A",
        "branch": r[4] or "General",
        "status": r[5] or "P" # Default to P
    } for r in students_rows]
    
    return render_template("faculty/mark_attendance.html", lecture_id=lecture_id, students=students)

@bp.route("/approve/<int:user_id>", methods=["POST"])
@role_required("Faculty")
def approve_user(user_id):
    user = fetch_one("SELECT role FROM users WHERE id = %s", (user_id,))
    if user and user[0] == 'Student':
        execute("UPDATE users SET is_approved = TRUE WHERE id = %s", (user_id,))
        # Auto-create student record stub
        # Ideally, we ask for Enrollment No & Division during approval or signup.
        # For now, placeholder enrollment
        import uuid
        enroll = f"E{uuid.uuid4().hex[:6].upper()}"
        execute("INSERT INTO students (user_id, enrollment_no) VALUES (%s, %s)", (user_id, enroll))
        flash(f"Student approved. Assigned Enrollment: {enroll}", "success")
    else:
        flash("Invalid approval request.", "danger")
    return redirect(url_for("faculty.dashboard"))

@bp.route("/reject/<int:user_id>", methods=["POST"])
@role_required("Faculty")
def reject_user(user_id):
    user = fetch_one("SELECT role FROM users WHERE id = %s", (user_id,))
    if user and user[0] == 'Student':
        execute("DELETE FROM users WHERE id = %s", (user_id,))
        flash("Student request rejected.", "warning")
    else:
        flash("Invalid request.", "danger")
    return redirect(url_for("faculty.dashboard"))
