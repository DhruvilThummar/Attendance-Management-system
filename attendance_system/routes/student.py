"""
Student routes - Dashboard and Profile
"""
from flask import Blueprint, render_template
from services.data_helper import DataHelper

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route("/dashboard")
def sdashboard():
    """Student Dashboard"""
    student = DataHelper.get_students()
    attendance_stats = DataHelper.get_attendance_records()
    return render_template("student/sbase.html", 
                          title="Student Dashboard",
                          student=student,
                          attendance_stats=attendance_stats)


@student_bp.route("")
def student_redirect():
    """Redirect to student dashboard"""
    return sdashboard()


@student_bp.route("/profile")
def student_profile():
    """Student Profile"""
    student = DataHelper.get_students()
    college = DataHelper.get_college()
    return render_template("student/profile.html",
                          title="Student Profile",
                          student=student,
                          college=college)
