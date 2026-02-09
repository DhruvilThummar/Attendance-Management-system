"""
Parent routes - Child attendance tracking and profile
"""
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
from models.user import db, User
from services.data_helper import DataHelper
from attendance_system.utils.auth_decorators import login_required, parent_required
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
@parent_required
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
            overall_pct = sum(float(r.get('attendance_percentage', 0)) for r in attendance_records) / len(attendance_records)
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
    all_subjects = {}  # Use dict to avoid duplicates, key by subject_id
    for child_data in children_attendance:
        for subject in child_data.get('subject_wise', []):
            subject_id = subject.get('subject_id')
            if subject_id and subject_id not in all_subjects:
                all_subjects[subject_id] = {
                    'subject_id': subject_id,
                    'subject_name': subject.get('subject_name', 'Unknown')
                }
    
    # Convert to list
    all_subjects_list = list(all_subjects.values())
    
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
        for subject in all_subjects_list:
            subject_name = subject.get('subject_name', 'Unknown')
            subject_data[subject_name] = 87.5
        
        if subject_data:
            charts['subject_attendance'] = generate_subject_attendance_chart(subject_data)
    
    return render_template("parent/dashboard.html",
                         context=context,
                         children_attendance=children_attendance,
                         time_period=time_period,
                         alerts=all_alerts,
                         subjects=all_subjects_list,
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
        overall_pct = sum(float(r.get('attendance_percentage', 0)) for r in attendance_records) / len(attendance_records)
        total_lectures = sum(r.get('total_lectures', 0) for r in attendance_records)
        attended = sum(int((float(r.get('attendance_percentage', 0)) / 100) * r.get('total_lectures', 0)) for r in attendance_records)
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


@parent_bp.route("/profile/update", methods=['POST'])
@parent_required
def parent_update_profile():
    """Update parent profile information"""
    try:
        data = request.get_json()
        
        # Get current user
        user_data = DataHelper.get_user('parent')
        if not user_data:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get user record
        user = User.query.get(user_data['user_id'])
        
        if not user:
            return jsonify({'success': False, 'message': 'User record not found'}), 404
        
        # Update user information
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.mobile = data.get('mobile', user.mobile)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating profile: {str(e)}'}), 500


@parent_bp.route("/profile/change-password", methods=['POST'])
@parent_required
def parent_change_password():
    """Change parent password"""
    try:
        data = request.get_json()
        
        # Get current user
        user_data = DataHelper.get_user('parent')
        if not user_data:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        user = User.query.get(user_data['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Verify current password
        if not user.check_password(data.get('current_password')):
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
        
        # Update password
        user.set_password(data.get('new_password'))
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error changing password: {str(e)}'}), 500


@parent_bp.route("/profile")
@parent_required
def parent_profile():
    """Parent Profile with child information"""
    context = _get_parent_context()
    parent_user = context.get('user', {})
    children = context.get('children', [])
    
    # Get details for all children
    children_details = []
    all_alerts = []
    total_attendance = 0
    
    # Initialize attendance stats
    attendance_stats = {
        'total_lectures': 0,
        'present': 0,
        'absent': 0,
        'percentage': 0
    }
    
    for child in children:
        student_id = child.get('student_id', child.get('id'))
        student = DataHelper.get_student(student_id)
        
        # Get overall attendance
        attendance_records = DataHelper.get_child_attendance(student_id)
        
        if attendance_records:
            overall_pct = sum(float(r.get('attendance_percentage', 0)) for r in attendance_records) / len(attendance_records)
            
            # Calculate attendance stats from records
            for record in attendance_records:
                attendance_stats['total_lectures'] += record.get('total_lectures', 0)
                attendance_stats['present'] += record.get('present_count', 0)
                attendance_stats['absent'] += record.get('absent_count', 0)
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
    
    # Calculate attendance percentage
    if attendance_stats['total_lectures'] > 0:
        attendance_stats['percentage'] = round(
            (attendance_stats['present'] / attendance_stats['total_lectures']) * 100, 2
        )
    
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
                         attendance_stats=attendance_stats,
                         total_alerts=len(all_alerts),
                         all_alerts=all_alerts)


@parent_bp.route("/analytics")
@parent_required
def panalytics():
    """Parent Analytics - Child's attendance analytics dashboard"""
    context = _get_parent_context()
    
    if not context['children']:
        return render_template("parent/analytics.html",
                             context=context,
                             children=[],
                             selected_child={},
                             charts={},
                             stats={})
    
    # Get selected child (first child or from query params)
    selected_child_id = request.args.get('child_id')
    selected_child = context['children'][0]
    
    if selected_child_id:
        for child in context['children']:
            if str(child.get('student_id')) == str(selected_child_id):
                selected_child = child
                break
    
    student_id = selected_child.get('student_id', selected_child.get('id'))
    
    # Get child's attendance records only
    attendance_records = DataHelper.get_child_attendance(student_id)
    
    # Calculate statistics
    stats = {
        'total_lectures': 0,
        'attended_lectures': 0,
        'overall_attendance': 0.0,
        'status': 'Good',
        'child_name': selected_child.get('name', 'Unknown')
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
    
    return render_template("parent/analytics.html",
                         context=context,
                         children=context['children'],
                         selected_child=selected_child,
                         charts=charts,
                         stats=stats,
                         attendance_records=attendance_records)
