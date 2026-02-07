"""Faculty routes - Attendance, Analytics, Reports, Timetable, Profile"""
from flask import Blueprint, render_template, send_file, request, jsonify
from models.user import db, User
from services.data_helper import DataHelper
from attendance_system.utils.auth_decorators import login_required, faculty_required
from services.chart_helper import (
    generate_attendance_weekly_chart,
    generate_attendance_monthly_chart,
    generate_subject_attendance_chart
)
import csv
import io
from datetime import datetime

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')


@faculty_bp.route("/dashboard")
@faculty_required
def fdashboard():
    """Faculty dashboard showing assigned subjects and classes"""
    faculty_data = DataHelper.get_faculty()
    
    # Handle case where get_faculty() returns a list or None
    if isinstance(faculty_data, list):
        faculty = faculty_data[0] if faculty_data else None
    else:
        faculty = faculty_data
    
    subjects = DataHelper.get_subjects()
    lectures = DataHelper.get_lectures()
    
    # Get department info for the faculty
    department = None
    if faculty and faculty.get('dept_id'):
        dept = DataHelper.get_department(faculty.get('dept_id'))
        department = {'dept_name': dept.get('dept_name', 'N/A')} if isinstance(dept, dict) else {'dept_name': 'N/A'}
    else:
        department = {'dept_name': 'N/A'}
    
    # Compute stats for dashboard
    stats = {
        'total_lectures': len(lectures) if lectures else 0,
        'remaining': max(0, (len(lectures) - 1) if lectures else 0),
        'subjects': len(subjects) if subjects else 0,
        'avg_attendance': 87.5  # Sample data
    }
    
    # Teaching stats for template
    teaching_stats = {
        'lectures_conducted': len(lectures) if lectures else 0,
        'total_subjects': len(subjects) if subjects else 0,
        'proxy_taken': 0,
        'mentoring_count': 0
    }
    
    return render_template("faculty/dashboard.html", 
                          faculty=faculty, 
                          subjects=subjects, 
                          lectures=lectures,
                          stats=stats,
                          teaching_stats=teaching_stats,
                          department=department,
                          datetime=datetime)


@faculty_bp.route("/attendance")
@faculty_required
def fattendance():
    """Record attendance for lectures"""
    faculty = DataHelper.get_faculty()
    subjects = DataHelper.get_subjects()
    lectures = DataHelper.get_lectures()
    return render_template("faculty/attendance.html", 
                          faculty=faculty, subjects=subjects, lectures=lectures, datetime=datetime)


@faculty_bp.route("/analytics")
def fanalytics():
    """View attendance analytics and statistics"""
    faculty = DataHelper.get_faculty()
    attendance_data = DataHelper.get_attendance_records()

    total_lectures = len(DataHelper.get_lectures())
    avg_attendance = DataHelper._np_mean([a.get('attendance_percentage', 0) for a in attendance_data])

    analytics_payload = DataHelper.get_faculty_analytics_payload()
    class_stats = analytics_payload['class_stats']
    day_stats = analytics_payload['day_stats']

    best_class = max(class_stats, key=lambda item: item['percentage']) if class_stats else None
    lowest_day = min(day_stats, key=lambda item: item['percentage']) if day_stats else None

    # Generate charts
    charts = {}
    
    # Weekly attendance chart
    weekly_data = {
        'Mon': 42,
        'Tue': 40,
        'Wed': 43,
        'Thu': 41,
        'Fri': 38
    }
    charts['weekly_attendance'] = generate_attendance_weekly_chart(weekly_data)
    
    # Monthly trend chart
    monthly_data = {
        'Week 1': 92.5,
        'Week 2': 88.3,
        'Week 3': 90.1,
        'Week 4': 87.6
    }
    charts['monthly_trend'] = generate_attendance_monthly_chart(monthly_data)
    
    # Subject attendance chart
    subject_data = {}
    subjects = DataHelper.get_subjects()
    for subject in subjects if subjects else []:
        subject_name = subject.get('subject_name', 'Unknown')
        subject_data[subject_name] = 87.5
    
    if subject_data:
        charts['subject_attendance'] = generate_subject_attendance_chart(subject_data)

    return render_template(
        "faculty/analytics.html",
        faculty=faculty,
        attendance_data=attendance_data,
        total_lectures=total_lectures,
        avg_attendance=round(avg_attendance, 2),
        class_stats=class_stats,
        day_stats=day_stats,
        charts=charts,
        best_class=best_class,
        lowest_day=lowest_day
    )


@faculty_bp.route("/reports")
def freports():
    """View and manage attendance reports"""
    faculty = DataHelper.get_faculty()
    subjects = DataHelper.get_subjects()
    students = DataHelper.get_students()
    attendance_data = DataHelper.get_attendance_records()
    
    return render_template("faculty/reports.html",
                          faculty=faculty,
                          subjects=subjects,
                          students=students,
                          attendance_data=attendance_data,
                          datetime=datetime)


@faculty_bp.route("/timetable")
def ftimetable():
    """View faculty timetable"""
    faculty = DataHelper.get_faculty()
    timetable = DataHelper.get_timetable()
    subjects = DataHelper.get_subjects()
    
    return render_template("faculty/timetable.html",
                          faculty=faculty,
                          timetable=timetable,
                          subjects=subjects)


@faculty_bp.route("/profile")
@faculty_required
def fprofile():
    """View and edit faculty profile"""
    from attendance_system.models.user import User
    from attendance_system.models.college import College
    from attendance_system.models.department import Department
    from attendance_system.models.faculty import Faculty
    
    # Get current user
    user_data = DataHelper.get_user('faculty')
    if not user_data:
        return render_template("faculty/profile.html",
                             user=None,
                             faculty=None,
                             college=None,
                             department=None,
                             teaching_stats={})
    
    # Get faculty record
    faculty_record = Faculty.query.filter_by(user_id=user_data['user_id']).first()
    faculty = DataHelper._faculty_dict(faculty_record) if faculty_record else None
    
    # Get college
    college = College.query.get(user_data['college_id']) if user_data.get('college_id') else None
    
    # Get department
    department = None
    if faculty and faculty.get('dept_id'):
        department = Department.query.get(faculty.get('dept_id'))
    
    # Compute teaching statistics
    subjects = DataHelper.get_subjects(dept_id=faculty.get('dept_id') if faculty else None)
    lectures = DataHelper.get_lectures()
    teaching_stats = {
        'total_subjects': len(subjects) if subjects else 0,
        'lectures_conducted': len(lectures) if lectures else 0,
        'proxy_taken': 0,
        'mentoring_count': 0
    }
    
    return render_template("faculty/profile.html",
                          user=user_data,
                          faculty=faculty,
                          college=college,
                          department=department,
                          teaching_stats=teaching_stats)


@faculty_bp.route("/download-report", methods=['GET', 'POST'])
def download_report():
    """Download attendance report as CSV"""
    attendance_data = DataHelper.get_attendance_records()
    students = DataHelper.get_students()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Student ID', 'Student Name', 'Subject', 'Attendance Percentage', 'Status'])
    
    # Write data
    for record in attendance_data:
        writer.writerow([
            record.get('student_id', ''),
            record.get('student_name', ''),
            record.get('subject', ''),
            f"{record.get('attendance_percentage', 0):.2f}%",
            record.get('status', '')
        ])
    
    # Convert to bytes
    output.seek(0)
    bytes_io = io.BytesIO()
    bytes_io.write(output.getvalue().encode('utf-8'))
    bytes_io.seek(0)
    
    return send_file(
        bytes_io,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'attendance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )


@faculty_bp.route("/approvals")
def faculty_approvals():
    """View pending student and parent approvals"""
    faculty = DataHelper.get_faculty()
    
    # Get pending students and parents
    pending_users = User.query.filter(
        User.is_approved == False,
        User.role_id.in_([5, 6])  # STUDENT=5, PARENT=6
    ).all()
    
    return render_template("faculty/approvals.html",
                          title="Pending Approvals",
                          faculty=faculty,
                          pending_users=pending_users)


@faculty_bp.route("/approve/user/<int:user_id>", methods=['POST'])
def faculty_approve_user(user_id):
    """Approve a student or parent"""
    try:
        user = User.query.get(user_id)
        if user and user.role_id in [5, 6]:  # STUDENT, PARENT
            user.is_approved = True
            db.session.commit()
            return jsonify({'success': True, 'message': f'{user.role.role_name} "{user.name}" approved successfully'})
        return jsonify({'success': False, 'message': 'User not found or invalid role'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@faculty_bp.route("/reject/user/<int:user_id>", methods=['POST'])
def faculty_reject_user(user_id):
    """Reject/Delete a user"""
    try:
        user = User.query.get(user_id)
        if user:
            user_name = user.name
            user_role = user.role.role_name
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': f'{user_role} "{user_name}" rejected and removed'})
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
