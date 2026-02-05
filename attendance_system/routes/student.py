"""
Student routes - Dashboard and Profile
"""
from flask import Blueprint, render_template

student_bp = Blueprint('student', __name__, url_prefix='/student')

def get_mock_data():
    from app import mock_users, mock_student, mock_college, mock_department, mock_division, mock_semester, mock_attendance_stats
    return mock_users, mock_student, mock_college, mock_department, mock_division, mock_semester, mock_attendance_stats


@student_bp.route("/dashboard")
def sdashboard():
    """Student Dashboard"""
    return render_template("student/sbase.html", title="Student Dashboard")


@student_bp.route("")
def student_redirect():
    """Redirect to student dashboard"""
    return sdashboard()


@student_bp.route("/profile")
def student_profile():
    """Student Profile"""
    mock_users, mock_student, mock_college, mock_department, mock_division, mock_semester, mock_attendance_stats = get_mock_data()
    return render_template("student/profile.html",
                         title="Student Profile",
                         user=mock_users['student'],
                         student=mock_student,
                         college=mock_college,
                         department=mock_department,
                         division=mock_division,
                         semester=mock_semester,
                         attendance_stats=mock_attendance_stats)


@student_bp.route("/dashboard")
def sdashboard():
    """Student Dashboard"""
    return render_template("student/sbase.html", title="Student Dashboard")


@student_bp.route("")
def student_redirect():
    """Redirect to student dashboard"""
    return sdashboard()


@student_bp.route("/profile")
def student_profile():
    """Student Profile"""
    return render_template("student/profile.html",
                         title="Student Profile",
                         user=mock_users['student'],
                         student=mock_student,
                         college=mock_college,
                         department=mock_department,
                         division=mock_division,
                         semester=mock_semester,
                         attendance_stats=mock_attendance_stats)
