"""
HOD (Head of Department) routes - Dashboard and Profile
"""
from flask import Blueprint, render_template
from services.data_helper import DataHelper

hod_bp = Blueprint('hod', __name__, url_prefix='/hod')


@hod_bp.route("/dashboard")
def hdashboard():
    """HOD Dashboard"""
    departments = DataHelper.get_departments()
    faculty = DataHelper.get_faculty()
    attendance_data = DataHelper.get_attendance_records()
    return render_template("hod/hbase.html",
                          title="HOD Dashboard",
                          departments=departments,
                          faculty=faculty,
                          attendance_data=attendance_data)


@hod_bp.route("")
def hod_redirect():
    """Redirect to HOD dashboard"""
    return hdashboard()


@hod_bp.route("/profile")
def hod_profile():
    """HOD Profile"""
    faculty = DataHelper.get_faculty()
    college = DataHelper.get_college()
    return render_template("hod/profile.html",
                          title="HOD Profile",
                          faculty=faculty,
                          college=college)
