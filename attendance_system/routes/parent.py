"""
Parent routes - Dashboard and Profile
"""
from flask import Blueprint, render_template

parent_bp = Blueprint('parent', __name__, url_prefix='/parent')

def get_mock_data():
    from app import mock_users, mock_college, mock_department, mock_division, mock_semester, mock_attendance_stats
    return mock_users, mock_college, mock_department, mock_division, mock_semester, mock_attendance_stats


@parent_bp.route("/dashboard")
def pdashboard():
    """Parent Dashboard"""
    return render_template("parent/pbase.html", title="Parent Dashboard")


@parent_bp.route("")
def parent_redirect():
    """Redirect to parent dashboard"""
    return pdashboard()


@parent_bp.route("/profile")
def parent_profile():
    """Parent Profile"""
    mock_users, mock_college, mock_department, mock_division, mock_semester, mock_attendance_stats = get_mock_data()
    return render_template("parent/profile.html",
                         title="Parent Profile",
                         user=mock_users['parent'],
                         student=mock_users['student'],
                         college=mock_college,
                         department=mock_department,
                         division=mock_division,
                         semester=mock_semester,
                         attendance_stats=mock_attendance_stats)


@parent_bp.route("/dashboard")
def pdashboard():
    """Parent Dashboard"""
    return render_template("parent/pbase.html", title="Parent Dashboard")


@parent_bp.route("")
def parent_redirect():
    """Redirect to parent dashboard"""
    return pdashboard()


@parent_bp.route("/profile")
def parent_profile():
    """Parent Profile"""
    return render_template("parent/profile.html",
                         title="Parent Profile",
                         user=mock_users['parent'],
                         student=mock_users['student'],
                         college=mock_college,
                         department=mock_department,
                         division=mock_division,
                         semester=mock_semester,
                         attendance_stats=mock_attendance_stats)
