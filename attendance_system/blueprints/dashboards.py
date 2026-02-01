"""
Role-Based Dashboard Routes
===========================

Routes for different user roles:
- Faculty Dashboard: Mark and edit attendance
- HOD Dashboard: Manage timetables, view reports
- Student Dashboard: View personal attendance
- Parent Dashboard: View child's attendance
- College Admin Dashboard: View all data
- Admin Dashboard: System administration

Author: Development Team
Version: 1.0
"""

from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime

# Import decorators
from ..decorators.rbac import (
    login_required,
    faculty_only,
    student_only,
    hod_only,
    parent_only,
    college_only,
    admin_only
)

# Import services
from ..services.attendance_service import AttendanceService
from ..services.timetable_service import TimetableService
from ..services.report_service import ReportService

# Create blueprint
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboard')

# Initialize services
attendance_svc = AttendanceService()
timetable_svc = TimetableService()
report_svc = ReportService()


# ============================================================================
#   STUDENT DASHBOARD
# ============================================================================

@dashboards.route('/student', methods=['GET'])
@login_required
@student_only
def student_dashboard():
    """
    Student Dashboard
    
    Shows:
    - Personal attendance percentage
    - Attendance by subject
    - Daily attendance details
    - Upcoming classes
    
    Route: GET /dashboard/student
    """
    student_id = session.get('user_id')
    
    # Get attendance data
    attendance_percentage = attendance_svc.calculate_percentage(student_id)
    student_records = attendance_svc.get_student_attendance(student_id)
    
    context = {
        'page_title': 'Student Dashboard',
        'attendance_percentage': attendance_percentage,
        'records': student_records
    }
    
    return render_template('student/dashboard.html', **context)


@dashboards.route('/student/attendance', methods=['GET'])
@login_required
@student_only
def student_attendance_details():
    """
    Student Attendance Details Page
    
    Route: GET /dashboard/student/attendance
    """
    student_id = session.get('user_id')
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    
    records = attendance_svc.get_student_attendance(
        student_id=student_id,
        month=month,
        year=year
    )
    
    context = {
        'page_title': 'My Attendance',
        'attendance_records': records
    }
    
    return render_template('student/attendance.html', **context)


# ============================================================================
#   FACULTY DASHBOARD
# ============================================================================

@dashboards.route('/faculty', methods=['GET'])
@login_required
@faculty_only
def faculty_dashboard():
    """
    Faculty Dashboard
    
    Shows:
    - My schedule
    - Today's classes
    - Recent attendance
    - Quick actions (mark attendance, view reports)
    
    Route: GET /dashboard/faculty
    """
    faculty_id = session.get('user_id')
    
    # Get faculty schedule
    faculty_schedule = timetable_svc.get_faculty_schedule(faculty_id)
    
    context = {
        'page_title': 'Faculty Dashboard',
        'schedule': faculty_schedule
    }
    
    return render_template('faculty/dashboard.html', **context)


@dashboards.route('/faculty/mark-attendance', methods=['GET', 'POST'])
@login_required
@faculty_only
def mark_attendance():
    """
    Mark Attendance for Class
    
    GET: Show form to select lecture and students
    POST: Save attendance records
    
    Route: GET/POST /dashboard/faculty/mark-attendance
    """
    faculty_id = session.get('user_id')
    
    if request.method == 'POST':
        # Process attendance marking
        data = request.get_json()
        lecture_id = data.get('lecture_id')
        attendance_records = data.get('attendance', [])
        
        results = []
        for record in attendance_records:
            result = attendance_svc.mark_attendance(
                lecture_id=lecture_id,
                student_id=record['student_id'],
                status=record['status'],
                faculty_id=faculty_id,
                remarks=record.get('remarks', '')
            )
            results.append(result)
        
        return jsonify({
            'success': all(r['success'] for r in results),
            'message': 'Attendance marked successfully',
            'results': results
        })
    
    # GET: Show form
    context = {
        'page_title': 'Mark Attendance'
    }
    
    return render_template('faculty/mark_attendance.html', **context)


@dashboards.route('/faculty/edit-attendance', methods=['GET', 'POST'])
@login_required
@faculty_only
def edit_attendance():
    """
    Edit Existing Attendance Records
    
    GET: Show list of attendance records to edit
    POST: Update attendance record
    
    Route: GET/POST /dashboard/faculty/edit-attendance
    """
    if request.method == 'POST':
        data = request.get_json()
        attendance_id = data.get('attendance_id')
        new_status = data.get('status')
        remarks = data.get('remarks', '')
        
        result = attendance_svc.edit_attendance(
            attendance_id=attendance_id,
            new_status=new_status,
            remarks=remarks
        )
        
        return jsonify(result)
    
    # GET: Show attendance records
    context = {
        'page_title': 'Edit Attendance'
    }
    
    return render_template('faculty/edit_attendance.html', **context)


@dashboards.route('/faculty/class-attendance/<int:lecture_id>', methods=['GET'])
@login_required
@faculty_only
def view_class_attendance(lecture_id):
    """
    View Attendance for a Specific Class/Lecture
    
    Route: GET /dashboard/faculty/class-attendance/<lecture_id>
    """
    # Get attendance for this lecture
    attendance_records = attendance_svc.get_class_attendance(lecture_id)
    
    context = {
        'page_title': 'Class Attendance',
        'lecture_id': lecture_id,
        'records': attendance_records
    }
    
    return render_template('faculty/class_attendance.html', **context)


# ============================================================================
#   HOD DASHBOARD
# ============================================================================

@dashboards.route('/hod', methods=['GET'])
@login_required
@hod_only
def hod_dashboard():
    """
    HOD (Head of Department) Dashboard
    
    Shows:
    - Department statistics
    - Faculty performance
    - Timetable management link
    - Department attendance overview
    
    Route: GET /dashboard/hod
    """
    hod_id = session.get('user_id')
    
    # Get department reports
    faculty_report = report_svc.faculty_performance_report(hod_id=hod_id)
    subject_report = report_svc.subject_attendance_report(hod_id=hod_id)
    
    context = {
        'page_title': 'HOD Dashboard',
        'faculty_report': faculty_report,
        'subject_report': subject_report
    }
    
    return render_template('hod/dashboard.html', **context)


@dashboards.route('/hod/timetable', methods=['GET', 'POST'])
@login_required
@hod_only
def manage_timetable():
    """
    Manage Department Timetable
    
    GET: Show timetable management form
    POST: Create/update schedule
    
    Route: GET/POST /dashboard/hod/timetable
    """
    if request.method == 'POST':
        data = request.get_json()
        
        result = timetable_svc.create_schedule(
            division_id=data['division_id'],
            subject_id=data['subject_id'],
            faculty_id=data['faculty_id'],
            day_of_week=data['day_of_week'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            room_no=data.get('room_no', '')
        )
        
        return jsonify(result)
    
    # GET: Show timetable
    context = {
        'page_title': 'Manage Timetable'
    }
    
    return render_template('hod/timetable.html', **context)


@dashboards.route('/hod/reports', methods=['GET'])
@login_required
@hod_only
def hod_reports():
    """
    HOD Reports
    
    Shows:
    - Faculty performance report
    - Subject attendance report
    - Division-wise statistics
    - Department attendance trends
    
    Route: GET /dashboard/hod/reports
    """
    hod_id = session.get('user_id')
    report_type = request.args.get('type', 'faculty')
    
    if report_type == 'faculty':
        report_data = report_svc.faculty_performance_report(hod_id=hod_id)
    elif report_type == 'subject':
        report_data = report_svc.subject_attendance_report(hod_id=hod_id)
    else:
        report_data = report_svc.faculty_performance_report(hod_id=hod_id)
    
    context = {
        'page_title': 'HOD Reports',
        'report_type': report_type,
        'report_data': report_data
    }
    
    return render_template('hod/reports.html', **context)


# ============================================================================
#   PARENT DASHBOARD
# ============================================================================

@dashboards.route('/parent', methods=['GET'])
@login_required
@parent_only
def parent_dashboard():
    """
    Parent Dashboard
    
    Shows:
    - Child's attendance
    - Attendance percentage
    - Daily attendance details
    - School notifications
    
    Route: GET /dashboard/parent
    """
    parent_id = session.get('user_id')
    
    # TODO: Get child(ren) linked to this parent
    children = []  # placeholder
    
    context = {
        'page_title': 'Parent Dashboard',
        'children': children
    }
    
    return render_template('parent/dashboard.html', **context)


@dashboards.route('/parent/child/<int:student_id>/attendance', methods=['GET'])
@login_required
@parent_only
def view_child_attendance(student_id):
    """
    View Child's Attendance
    
    Route: GET /dashboard/parent/child/<student_id>/attendance
    """
    parent_id = session.get('user_id')
    
    # Get child's attendance report
    report = report_svc.child_attendance_report(
        student_id=student_id,
        parent_id=parent_id
    )
    
    if not report.get('success'):
        return render_template('error.html', error=report['error']), 403
    
    context = {
        'page_title': f"Child's Attendance",
        'student_id': student_id,
        'report': report
    }
    
    return render_template('parent/child_attendance.html', **context)


# ============================================================================
#   COLLEGE ADMIN DASHBOARD
# ============================================================================

@dashboards.route('/college', methods=['GET'])
@login_required
@college_only
def college_dashboard():
    """
    College Admin Dashboard
    
    Shows:
    - College-wide statistics
    - All departments
    - All faculty
    - All students
    - Overall attendance
    
    Route: GET /dashboard/college
    """
    college_id = session.get('college_id')
    
    # Get college report
    college_report = report_svc.college_report(college_id=college_id)
    
    context = {
        'page_title': 'College Dashboard',
        'report': college_report
    }
    
    return render_template('college/dashboard.html', **context)


@dashboards.route('/college/reports', methods=['GET'])
@login_required
@college_only
def college_reports():
    """
    College-wide Reports
    
    Route: GET /dashboard/college/reports
    """
    college_id = session.get('college_id')
    
    college_report = report_svc.college_report(college_id=college_id)
    
    context = {
        'page_title': 'College Reports',
        'report': college_report
    }
    
    return render_template('college/reports.html', **context)


# ============================================================================
#   ADMIN DASHBOARD
# ============================================================================

@dashboards.route('/admin', methods=['GET'])
@login_required
@admin_only
def admin_dashboard():
    """
    System Admin Dashboard
    
    Shows:
    - System statistics
    - User management
    - System settings
    - Audit logs
    
    Route: GET /dashboard/admin
    """
    context = {
        'page_title': 'Admin Dashboard'
    }
    
    return render_template('admin/dashboard.html', **context)


@dashboards.route('/admin/users', methods=['GET', 'POST'])
@login_required
@admin_only
def manage_users():
    """
    Manage Users (Admin only)
    
    Route: GET/POST /dashboard/admin/users
    """
    context = {
        'page_title': 'Manage Users'
    }
    
    return render_template('admin/users.html', **context)


@dashboards.route('/admin/roles', methods=['GET'])
@login_required
@admin_only
def manage_roles():
    """
    Manage Roles and Permissions
    
    Route: GET /dashboard/admin/roles
    """
    context = {
        'page_title': 'Manage Roles'
    }
    
    return render_template('admin/roles.html', **context)


# ============================================================================
#   DYNAMIC DASHBOARD ROUTE
# ============================================================================

@dashboards.route('/', methods=['GET'])
@login_required
def get_dashboard():
    """
    Dynamic Dashboard Router
    
    Routes to appropriate dashboard based on user role.
    
    Route: GET /dashboard
    """
    role = session.get('role')
    
    role_routes = {
        'ADMIN': 'dashboards.admin_dashboard',
        'HOD': 'dashboards.hod_dashboard',
        'FACULTY': 'dashboards.faculty_dashboard',
        'STUDENT': 'dashboards.student_dashboard',
        'PARENT': 'dashboards.parent_dashboard',
        'COLLEGE': 'dashboards.college_dashboard'
    }
    
    from flask import redirect, url_for
    route = role_routes.get(role, 'dashboards.student_dashboard')
    return redirect(url_for(route))


# ============================================================================
#   API ENDPOINTS
# ============================================================================

@dashboards.route('/api/attendance/mark', methods=['POST'])
@login_required
@faculty_only
def api_mark_attendance():
    """
    API: Mark Attendance
    
    POST /dashboard/api/attendance/mark
    """
    data = request.get_json()
    faculty_id = session.get('user_id')
    
    result = attendance_svc.mark_attendance(
        lecture_id=data['lecture_id'],
        student_id=data['student_id'],
        status=data['status'],
        faculty_id=faculty_id,
        remarks=data.get('remarks', '')
    )
    
    return jsonify(result)


@dashboards.route('/api/attendance/<int:attendance_id>', methods=['PUT'])
@login_required
@faculty_only
def api_edit_attendance(attendance_id):
    """
    API: Edit Attendance
    
    PUT /dashboard/api/attendance/<attendance_id>
    """
    data = request.get_json()
    
    result = attendance_svc.edit_attendance(
        attendance_id=attendance_id,
        new_status=data['status'],
        remarks=data.get('remarks', '')
    )
    
    return jsonify(result)


@dashboards.route('/api/timetable/create', methods=['POST'])
@login_required
@hod_only
def api_create_schedule():
    """
    API: Create Timetable Schedule
    
    POST /dashboard/api/timetable/create
    """
    data = request.get_json()
    
    result = timetable_svc.create_schedule(
        division_id=data['division_id'],
        subject_id=data['subject_id'],
        faculty_id=data['faculty_id'],
        day_of_week=data['day_of_week'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        room_no=data.get('room_no', '')
    )
    
    return jsonify(result)
