"""
Student routes - Personal attendance tracking and profile
"""
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
from services.data_helper import DataHelper
from services.chart_helper import (
    generate_attendance_weekly_chart,
    generate_attendance_monthly_chart,
    generate_subject_attendance_chart
)

student_bp = Blueprint('student', __name__, url_prefix='/student')


def _get_student_context():
    """Get current student user and their details"""
    student_user = DataHelper.get_user('student')
    if not student_user:
        return {'user': None, 'student': None}
    
    # Get student details by user_id
    students = DataHelper.get_students()
    student = None
    for s in students:
        if s.get('user_id') == student_user['user_id']:
            student = s
            break
    
    return {
        'user': student_user,
        'student': student
    }


@student_bp.route("/dashboard")
def sdashboard():
    """Student Dashboard - Personal attendance overview"""
    context = _get_student_context()
    time_period = request.args.get('period', 'overall')
    
    # Default attendance data structure
    default_attendance_data = {
        'overall_pct': 0,
        'total_lectures': 0,
        'attended_lectures': 0,
        'weekly': [],
        'monthly': [],
        'subject_wise': [],
        'records': []
    }
    
    if not context['student']:
        charts = {
            'weekly_attendance': generate_attendance_weekly_chart({'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0}),
            'monthly_trend': generate_attendance_monthly_chart({'Week 1': 0, 'Week 2': 0, 'Week 3': 0, 'Week 4': 0})
        }
        return render_template("student/dashboard.html",
                             context=context,
                             attendance_data=default_attendance_data,
                             time_period=time_period,
                             alerts=[],
                             subjects=[],
                             charts=charts)
    
    student_id = context['student']['student_id']
    
    # Get overall attendance
    attendance_records = DataHelper.get_child_attendance(student_id)
    
    # Calculate overall percentage
    if attendance_records:
        overall_pct = sum(r.get('attendance_percentage', 0) for r in attendance_records) / len(attendance_records)
        total_lectures = sum(r.get('total_lectures', 0) for r in attendance_records)
        attended = sum(r.get('attended_lectures', 0) for r in attendance_records)
    else:
        overall_pct = 0
        total_lectures = 0
        attended = 0
    
    # Get weekly and monthly attendance
    weekly_data = DataHelper.get_child_attendance_by_period(student_id, 'weekly')
    monthly_data = DataHelper.get_child_attendance_by_period(student_id, 'monthly')
    
    # Get subject-wise attendance
    subject_wise = DataHelper.get_child_subject_wise_attendance(student_id)
    
    # Get alerts
    alerts = DataHelper.get_child_alerts(student_id)
    
    attendance_data = {
        'overall_pct': round(overall_pct, 2),
        'total_lectures': total_lectures,
        'attended_lectures': attended,
        'weekly': weekly_data,
        'monthly': monthly_data,
        'subject_wise': subject_wise,
        'records': attendance_records
    }
    
    # Generate charts
    charts = {}
    
    # Weekly attendance chart
    weekly_chart_data = {
        'Mon': 6,
        'Tue': 6,
        'Wed': 5,
        'Thu': 6,
        'Fri': 5
    }
    charts['weekly_attendance'] = generate_attendance_weekly_chart(weekly_chart_data)
    
    # Monthly trend
    monthly_chart_data = {
        'Week 1': 91.5,
        'Week 2': 88.3,
        'Week 3': 90.1,
        'Week 4': 87.6
    }
    charts['monthly_trend'] = generate_attendance_monthly_chart(monthly_chart_data)
    
    # Subject-wise attendance
    subject_data = {}
    if subject_wise:
        for subject in subject_wise:
            subject_name = subject.get('subject_name', 'Unknown')
            attendance_pct = subject.get('attendance_percentage', 0)
            subject_data[subject_name] = attendance_pct
    
    if subject_data:
        charts['subject_attendance'] = generate_subject_attendance_chart(subject_data)
    
    return render_template("student/dashboard.html",
                         context=context,
                         attendance_data=attendance_data,
                         time_period=time_period,
                         alerts=alerts,
                         subjects=subject_wise,
                         charts=charts)


@student_bp.route("")
def student_redirect():
    """Redirect to student dashboard"""
    return sdashboard()


@student_bp.route("/attendance")
def student_attendance():
    """Detailed attendance view with all analytics"""
    context = _get_student_context()
    
    if not context['student']:
        return render_template("student/attendance.html",
                             context=context,
                             overall_attendance={},
                             weekly_data=[],
                             monthly_data=[],
                             subject_wise_data=[],
                             alerts=[])
    
    student_id = context['student']['student_id']
    
    # Get overall attendance records
    attendance_records = DataHelper.get_child_attendance(student_id)
    
    # Calculate overall percentage
    if attendance_records:
        overall_pct = sum(r.get('attendance_percentage', 0) for r in attendance_records) / len(attendance_records)
        total_lectures = sum(r.get('total_lectures', 0) for r in attendance_records)
        attended = sum(r.get('attended_lectures', 0) for r in attendance_records)
    else:
        overall_pct = 0
        total_lectures = 0
        attended = 0
    
    overall_attendance = {
        'percentage': round(overall_pct, 2),
        'total_lectures': total_lectures,
        'attended_lectures': attended,
        'records': attendance_records
    }
    
    # Get weekly attendance
    weekly_data = DataHelper.get_child_attendance_by_period(student_id, 'weekly')
    
    # Get monthly attendance
    monthly_data = DataHelper.get_child_attendance_by_period(student_id, 'monthly')
    
    # Get subject-wise attendance
    subject_wise_data = DataHelper.get_child_subject_wise_attendance(student_id)
    
    # Get alerts
    alerts = DataHelper.get_child_alerts(student_id)
    
    return render_template("student/attendance.html",
                         context=context,
                         overall_attendance=overall_attendance,
                         weekly_data=weekly_data,
                         monthly_data=monthly_data,
                         subject_wise_data=subject_wise_data,
                         alerts=alerts)


@student_bp.route("/attendance/data")
def attendance_data_api():
    """API endpoint for attendance data with time period filter"""
    context = _get_student_context()
    
    if not context['student']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    student_id = context['student']['student_id']
    period = request.args.get('period', 'overall')
    subject_id = request.args.get('subject_id', type=int)
    
    if period == 'weekly':
        data = DataHelper.get_child_attendance_by_period(student_id, 'weekly', subject_id)
    elif period == 'monthly':
        data = DataHelper.get_child_attendance_by_period(student_id, 'monthly', subject_id)
    else:
        data = DataHelper.get_child_attendance(student_id, subject_id)
    
    return jsonify({'attendance': data})


@student_bp.route("/profile")
def student_profile():
    """Student Profile with attendance summary"""
    context = _get_student_context()
    
    if not context['student']:
        return render_template("student/profile.html",
                             title="Student Profile",
                             context=context,
                             student=None,
                             attendance_summary={},
                             subject_wise=[],
                             alerts=[])
    
    student_id = context['student']['student_id']
    
    # Get attendance summary
    attendance_records = DataHelper.get_child_attendance(student_id)
    
    if attendance_records:
        overall_pct = sum(r.get('attendance_percentage', 0) for r in attendance_records) / len(attendance_records)
        total_lectures = sum(r.get('total_lectures', 0) for r in attendance_records)
        attended = sum(r.get('attended_lectures', 0) for r in attendance_records)
    else:
        overall_pct = 0
        total_lectures = 0
        attended = 0
    
    attendance_summary = {
        'percentage': round(overall_pct, 2),
        'total_lectures': total_lectures,
        'attended_lectures': attended,
        'absent_lectures': total_lectures - attended
    }
    
    # Get subject-wise attendance
    subject_wise = DataHelper.get_child_subject_wise_attendance(student_id)
    
    # Get alerts
    alerts = DataHelper.get_child_alerts(student_id)
    
    return render_template("student/profile.html",
                         title="Student Profile",
                         context=context,
                         student=context['student'],
                         attendance_summary=attendance_summary,
                         subject_wise=subject_wise,
                         alerts=alerts)
