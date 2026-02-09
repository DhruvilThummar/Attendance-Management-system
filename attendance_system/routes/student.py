"""
Student routes - Personal attendance tracking and profile
"""
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
from services.data_helper import DataHelper
from attendance_system.utils.auth_decorators import login_required, student_required
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
@student_required
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
        # Convert Decimal values to float to avoid type mismatch
        percentages = [float(r.get('attendance_percentage', 0)) for r in attendance_records]
        overall_pct = sum(percentages) / len(percentages)
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
        # Convert Decimal values to float to avoid type mismatch
        percentages = [float(r.get('attendance_percentage', 0)) for r in attendance_records]
        overall_pct = sum(percentages) / len(percentages)
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
@student_required
def student_profile():
    """Student Profile with attendance summary"""
    context = _get_student_context()
    
    if not context['student']:
        return render_template("student/profile.html",
                             title="Student Profile",
                             context=context,
                             user=context.get('user'),
                             student=None,
                             college=None,
                             department=None,
                             division=None,
                             semester=None,
                             mentor=None,
                             attendance_summary={},
                             subject_wise=[],
                             alerts=[])
    
    student_id = context['student']['student_id']
    student_data = context['student']
    
    # Get related entities from database
    from models.college import College
    from models.department import Department
    from models.division import Division
    from models.subject import Semester
    from models.faculty import Faculty
    from models.user import User
    
    college = College.query.get(context['user']['college_id']) if context['user'] else None
    department = Department.query.get(student_data.get('dept_id')) if student_data.get('dept_id') else None
    division = Division.query.get(student_data.get('division_id')) if student_data.get('division_id') else None
    semester = Semester.query.get(student_data.get('semester_id')) if student_data.get('semester_id') else None
    
    # Get mentor if exists
    mentor = None
    if student_data.get('mentor_id'):
        mentor_faculty = Faculty.query.get(student_data.get('mentor_id'))
        if mentor_faculty:
            mentor = {'name': mentor_faculty.short_name or (mentor_faculty.user.name if mentor_faculty.user else 'N/A')}
    
    # Get attendance summary
    attendance_records = DataHelper.get_child_attendance(student_id)
    
    if attendance_records:
        # Convert Decimal values to float to avoid type mismatch
        percentages = [float(r.get('attendance_percentage', 0)) for r in attendance_records]
        overall_pct = sum(percentages) / len(percentages)
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
                         user=context['user'],
                         student=student_data,
                         college=college,
                         department=department,
                         division=division,
                         semester=semester,
                         mentor=mentor,
                         attendance_summary=attendance_summary,
                         subject_wise=subject_wise,
                         alerts=alerts)


@student_bp.route("/analytics")
@student_required
def sanalytics():
    """Student Analytics - Personal attendance analytics dashboard"""
    context = _get_student_context()
    
    if not context['student']:
        return render_template("student/analytics.html",
                             context=context,
                             charts={},
                             stats={})
    
    student_id = context['student']['student_id']
    
    # Get student's attendance records only
    attendance_records = DataHelper.get_child_attendance(student_id)
    
    # Calculate statistics
    stats = {
        'total_lectures': 0,
        'attended_lectures': 0,
        'overall_attendance': 0.0,
        'status': 'Good'
    }
    
    if attendance_records:
        stats['total_lectures'] = sum(r.get('total_lectures', 0) for r in attendance_records)
        stats['attended_lectures'] = sum(r.get('attended_lectures', 0) for r in attendance_records)
        
        if stats['total_lectures'] > 0:
            stats['overall_attendance'] = round(
                (stats['attended_lectures'] / stats['total_lectures']) * 100, 2
            )
            stats['status'] = 'Good' if stats['overall_attendance'] >= 85 else \
                            'Average' if stats['overall_attendance'] >= 75 else 'Warning'
    
    # Prepare data for charts
    weekly_data = {}
    monthly_data = {}
    subject_data = {}
    
    # Weekly attendance data
    from datetime import datetime as dt, timedelta
    today = dt.today()
    one_week_ago = today - timedelta(days=7)
    
    weekly_records = [r for r in (attendance_records or []) 
                     if r.get('last_updated') and 
                     dt.fromisoformat(str(r.get('last_updated'))).date() >= one_week_ago.date()]
    
    days_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    for record in weekly_records:
        if record.get('last_updated'):
            try:
                date_obj = dt.fromisoformat(str(record.get('last_updated')))
                day_name = days_map.get(date_obj.weekday(), 'Unknown')
                if day_name not in weekly_data:
                    weekly_data[day_name] = []
                weekly_data[day_name].append(float(record.get('attendance_percentage', 0)))
            except:
                pass
    
    # Calculate averages for weekly
    for day, percentages in weekly_data.items():
        weekly_data[day] = round(sum(percentages) / len(percentages), 1) if percentages else 0.0
    
    # Add missing days
    for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
        if day not in weekly_data:
            weekly_data[day] = 0.0
    
    # Subject-wise attendance
    for record in (attendance_records or []):
        subject_name = record.get('subject_name', 'Unknown')
        pct = float(record.get('attendance_percentage', 0))
        subject_data[subject_name] = pct
    
    # Monthly attendance (last 4 weeks)
    four_weeks_ago = today - timedelta(days=28)
    monthly_records = [r for r in (attendance_records or []) 
                      if r.get('last_updated') and 
                      dt.fromisoformat(str(r.get('last_updated'))).date() >= four_weeks_ago.date()]
    
    week_attendance = {}
    for record in monthly_records:
        if record.get('last_updated'):
            try:
                date_obj = dt.fromisoformat(str(record.get('last_updated')))
                week_num = date_obj.isocalendar()[1]
                week_key = f'Week {week_num % 4 if week_num % 4 > 0 else 4}'
                if week_key not in week_attendance:
                    week_attendance[week_key] = []
                week_attendance[week_key].append(float(record.get('attendance_percentage', 0)))
            except:
                pass
    
    for week, percentages in week_attendance.items():
        monthly_data[week] = round(sum(percentages) / len(percentages), 1) if percentages else 0.0
    
    if not monthly_data:
        for i in range(1, 5):
            monthly_data[f'Week {i}'] = 0.0
    
    # Generate charts
    charts = {
        'weekly_attendance': generate_attendance_weekly_chart(weekly_data) if weekly_data else None,
        'monthly_trend': generate_attendance_monthly_chart(monthly_data) if monthly_data else None,
        'subject_attendance': generate_subject_attendance_chart(subject_data) if subject_data else None
    }
    
    return render_template("student/analytics.html",
                         context=context,
                         charts=charts,
                         stats=stats,
                         attendance_records=attendance_records)
