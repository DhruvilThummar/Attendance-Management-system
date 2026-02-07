"""
Parent routes - Child attendance tracking and profile
"""
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
from services.data_helper import DataHelper
from services.chart_helper import (
    generate_attendance_weekly_chart,
    generate_attendance_monthly_chart,
    generate_subject_attendance_chart
)

parent_bp = Blueprint('parent', __name__, url_prefix='/parent')


def _get_parent_context():
    """Get parent user and their children"""
    parent_user = DataHelper.get_user('parent')
    children = DataHelper.get_parent_children(parent_user['user_id']) if parent_user else []
    return {
        'user': parent_user,
        'children': children
    }


@parent_bp.route("/dashboard")
def pdashboard():
    """Parent Dashboard - Child attendance overview"""
    context = _get_parent_context()
    time_period = request.args.get('period', 'overall')
    
    if not context['children']:
        return render_template("parent/dashboard.html",
                             context=context,
                             children_attendance=[],
                             time_period=time_period,
                             alerts=[],
                             subjects=[])
    
    # Get data for all children
    children_attendance = []
    all_alerts = []
    
    for child in context['children']:
        student_id = child.get('student_id', child.get('id'))
        student_info = DataHelper.get_student(student_id)
        
        # Get overall attendance
        attendance_records = DataHelper.get_child_attendance(student_id)
        
        # Calculate overall percentage
        if attendance_records:
            overall_pct = sum(r.get('attendance_percentage', 0) for r in attendance_records) / len(attendance_records)
        else:
            overall_pct = 0
        
        # Get weekly attendance
        weekly = DataHelper.get_child_attendance_by_period(student_id, 'weekly')
        
        # Get monthly attendance
        monthly = DataHelper.get_child_attendance_by_period(student_id, 'monthly')
        
        # Get subject-wise attendance
        subject_wise = DataHelper.get_child_subject_wise_attendance(student_id)
        
        # Get alerts
        child_alerts = DataHelper.get_child_alerts(student_id)
        all_alerts.extend(child_alerts)
        
        children_attendance.append({
            'student': student_info,
            'overall_attendance_pct': round(overall_pct, 2),
            'weekly_attendance': weekly,
            'monthly_attendance': monthly,
            'subject_wise': subject_wise,
            'alerts': child_alerts
        })
    
    # Get unique subjects for filter
    all_subjects = set()
    for child_data in children_attendance:
        for subject in child_data.get('subject_wise', []):
            all_subjects.add({
                'subject_id': subject['subject_id'],
                'subject_name': subject['subject_name']
            })
    
    # Generate charts for first child (or primary child)
    charts = {}
    if context['children']:
        first_child_id = context['children'][0].get('student_id', context['children'][0].get('id'))
        
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
        for subject in all_subjects:
            subject_name = subject.get('subject_name', 'Unknown')
            subject_data[subject_name] = 87.5
        
        if subject_data:
            charts['subject_attendance'] = generate_subject_attendance_chart(subject_data)
    
    return render_template("parent/dashboard.html",
                         context=context,
                         children_attendance=children_attendance,
                         time_period=time_period,
                         alerts=all_alerts,
                         subjects=list(all_subjects),
                         charts=charts)


@parent_bp.route("")
def parent_redirect():
    """Redirect to parent dashboard"""
    return pdashboard()


@parent_bp.route("/attendance/<int:student_id>")
def child_attendance(student_id):
    """View detailed attendance for a specific child"""
    context = _get_parent_context()
    
    # Verify child belongs to this parent
    student_found = any(c.get('student_id', c.get('id')) == student_id for c in context.get('children', []))
    if not student_found:
        return jsonify({'error': 'Unauthorized'}), 403
    
    student = DataHelper.get_student(student_id)
    
    # Get overall attendance records
    attendance_records = DataHelper.get_child_attendance(student_id)
    
    # Calculate overall percentage
    if attendance_records:
        overall_pct = sum(r.get('attendance_percentage', 0) for r in attendance_records) / len(attendance_records)
        total_lectures = sum(r.get('total_lectures', 0) for r in attendance_records)
        attended = sum(int((r.get('attendance_percentage', 0) / 100) * r.get('total_lectures', 0)) for r in attendance_records)
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
    
    return render_template("parent/attendance.html",
                         context=context,
                         student=student,
                         overall_attendance=overall_attendance,
                         weekly_data=weekly_data,
                         monthly_data=monthly_data,
                         subject_wise_data=subject_wise_data,
                         alerts=alerts)


@parent_bp.route("/attendance/data/<int:student_id>")
def attendance_data_api(student_id):
    """API endpoint for child attendance data with time period filter"""
    context = _get_parent_context()
    
    # Verify child belongs to this parent
    if not any(c['student_id'] == student_id for c in context['children']):
        return jsonify({'error': 'Unauthorized'}), 403
    
    period = request.args.get('period', 'overall')  # overall, weekly, monthly
    subject_id = request.args.get('subject_id', type=int)
    
    if period == 'weekly':
        data = DataHelper.get_child_attendance_by_period(student_id, 'weekly', subject_id)
    elif period == 'monthly':
        data = DataHelper.get_child_attendance_by_period(student_id, 'monthly', subject_id)
    else:
        data = DataHelper.get_child_attendance(student_id, subject_id)
    
    return jsonify({'attendance': data})


@parent_bp.route("/profile")
def parent_profile():
    """Parent Profile with child information"""
    context = _get_parent_context()
    parent_user = context.get('user', {})
    children = context.get('children', [])
    
    # Get details for all children
    children_details = []
    all_alerts = []
    total_attendance = 0
    
    for child in children:
        student_id = child.get('student_id', child.get('id'))
        student = DataHelper.get_student(student_id)
        
        # Get overall attendance
        attendance_records = DataHelper.get_child_attendance(student_id)
        
        if attendance_records:
            overall_pct = sum(r.get('attendance_percentage', 0) for r in attendance_records) / len(attendance_records)
        else:
            overall_pct = 0
        
        total_attendance += overall_pct
        
        # Get subject-wise attendance
        subject_wise = DataHelper.get_child_subject_wise_attendance(student_id)
        
        # Get alerts for this child
        child_alerts = DataHelper.get_child_alerts(student_id)
        for alert in child_alerts:
            alert['child_name'] = student.get('name', 'Unknown')
        all_alerts.extend(child_alerts)
        
        children_details.append({
            'student': student,
            'name': student.get('name', ''),
            'student_id': student_id,
            'enrollment_no': student.get('enrollment_no', ''),
            'division_name': student.get('division_name', ''),
            'semester': student.get('semester', ''),
            'attendance_pct': round(overall_pct, 2),
            'subject_wise': subject_wise,
            'alerts': child_alerts
        })
    
    # Calculate average attendance
    avg_attendance = round(total_attendance / len(children_details), 2) if children_details else 0
    
    # Get first child's detailed info for the profile section
    first_student = None
    department = None
    division = None
    semester = None
    
    if children_details:
        first_child = children_details[0]
        first_student = first_child.get('student', {})
        # Get additional details from DataHelper
        if first_student:
            department = {'dept_name': first_student.get('dept_name', 'N/A')}
            division = {'division_name': first_student.get('division_name', 'N/A')}
            semester = {
                'semester_no': first_student.get('semester_no', 'N/A'),
                'academic_year': first_student.get('academic_year', 'N/A')
            }
    
    return render_template("parent/profile.html",
                         title="Parent Profile",
                         context=context,
                         parent=parent_user,
                         children=children_details,
                         student=first_student,
                         department=department,
                         division=division,
                         semester=semester,
                         avg_attendance=avg_attendance,
                         total_alerts=len(all_alerts),
                         all_alerts=all_alerts)
