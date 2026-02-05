"""Faculty routes - Attendance, Analytics, Reports, Timetable, Profile"""
from flask import Blueprint, render_template, send_file, request, jsonify
from services.data_helper import DataHelper
import csv
import io
from datetime import datetime

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')


@faculty_bp.route("/dashboard")
def fdashboard():
    """Faculty dashboard showing assigned subjects and classes"""
    faculty = DataHelper.get_faculty()
    subjects = DataHelper.get_subjects()
    return render_template("faculty/dashboard.html", faculty=faculty, subjects=subjects)


@faculty_bp.route("/attendance")
def fattendance():
    """Record attendance for lectures"""
    faculty = DataHelper.get_faculty()
    subjects = DataHelper.get_subjects()
    lectures = DataHelper.get_lectures()
    return render_template("faculty/attendance.html", 
                          faculty=faculty, subjects=subjects, lectures=lectures)


@faculty_bp.route("/analytics")
def fanalytics():
    """View attendance analytics and statistics"""
    faculty = DataHelper.get_faculty()
    attendance_data = DataHelper.get_attendance_records()
    
    # Calculate statistics
    total_lectures = len(DataHelper.get_lectures())
    avg_attendance = sum([a.get('attendance_percentage', 0) for a in attendance_data]) / len(attendance_data) if attendance_data else 0
    
    return render_template("faculty/analytics.html",
                          faculty=faculty,
                          attendance_data=attendance_data,
                          total_lectures=total_lectures,
                          avg_attendance=round(avg_attendance, 2))


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
                          attendance_data=attendance_data)


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
def fprofile():
    """View and edit faculty profile"""
    faculty = DataHelper.get_faculty()
    return render_template("faculty/profile.html", faculty=faculty)


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
