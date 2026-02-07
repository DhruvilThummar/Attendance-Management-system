"""Faculty routes - Attendance, Analytics, Reports, Timetable, Profile"""
from flask import Blueprint, render_template, send_file, request, jsonify
from services.data_helper import DataHelper
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
