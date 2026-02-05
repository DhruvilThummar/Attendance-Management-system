"""
HOD (Head of Department) routes
"""
from flask import Blueprint, render_template

hod_bp = Blueprint('hod', __name__, url_prefix='/hod')

def get_mock_data():
    from app import mock_users, mock_faculty, mock_college, mock_department, mock_dept_stats
    return mock_users, mock_faculty, mock_college, mock_department, mock_dept_stats


@hod_bp.route("/dashboard")
def hdashboard():
    """HOD Dashboard"""
    return render_template("hod/hbase.html", title="HOD Dashboard")


@hod_bp.route("")
def hod_redirect():
    """Redirect to HOD dashboard"""
    return hdashboard()


@hod_bp.route("/profile")
def hod_profile():
    """HOD Profile"""
    mock_users, mock_faculty, mock_college, mock_department, mock_dept_stats = get_mock_data()
    return render_template("hod/profile.html",
                         title="HOD Profile",
                         user=mock_users['hod'],
                         faculty=mock_faculty,
                         college=mock_college,
                         department=mock_department,
                         dept_stats=mock_dept_stats)
