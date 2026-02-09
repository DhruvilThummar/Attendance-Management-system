"""
HOD (Head of Department) routes - dashboard, management pages, and APIs
"""
import csv
import io

from flask import Blueprint, render_template, request, jsonify, abort, make_response, send_file

from models.user import db, User
from services.data_helper import DataHelper
from services.export_service import ExportService
from attendance_system.utils.auth_decorators import login_required, hod_required
from services.chart_helper import (
    generate_attendance_monthly_chart,
    generate_subject_attendance_chart,
    generate_class_strength_chart
)
from datetime import datetime

hod_bp = Blueprint('hod', __name__, url_prefix='/hod')


def _get_hod_context():
    """Resolve the active HOD, faculty record, and department"""
    hod_user = DataHelper.get_hod_user()
    hod_faculty = DataHelper.get_faculty_member(user_id=hod_user['user_id']) if hod_user else None
    department = DataHelper.get_department_by_hod(hod_faculty['faculty_id']) if hod_faculty else None

    if not department:
        departments = DataHelper.get_departments()
        department = departments[0] if departments else None

    return {
        'user': hod_user,
        'faculty': hod_faculty,
        'department': department,
        'dept_id': department['dept_id'] if department else None
    }


@hod_bp.route("/dashboard")
@hod_required
def hdashboard():
    """Render HOD dashboard with department insights"""
    context = _get_hod_context()
    
    # Fallback to sample data if department not configured
    if not context['dept_id']:
        default_charts = {
            'monthly_attendance': generate_attendance_monthly_chart({'Week 1': 0, 'Week 2': 0, 'Week 3': 0, 'Week 4': 0}),
            'subject_attendance': generate_subject_attendance_chart({}),
            'class_strength': generate_class_strength_chart({})
        }
        return render_template(
            "hod/dashboard.html",
            context=context,
            stats={},
            faculty=[],
            divisions=[],
            subjects=[],
            attendance_summary={},
            timetable_overview={},
            timetable_days=[],
            charts=default_charts
        )

    dept_id = context['dept_id']
    department_stats = DataHelper.get_department_stats(dept_id)
    faculty_members = DataHelper.get_faculty(dept_id=dept_id)
    divisions = DataHelper.get_divisions(dept_id=dept_id)
    subjects = DataHelper.get_subjects(dept_id=dept_id)
    attendance_summary = DataHelper.get_division_attendance_summary(dept_id)
    timetable_overview = DataHelper.get_timetable_overview(dept_id)

    # Generate charts
    charts = {}
    
    # Monthly attendance trend
    monthly_data = {
        'Week 1': 91.5,
        'Week 2': 89.3,
        'Week 3': 92.1,
        'Week 4': 88.6
    }
    charts['monthly_attendance'] = generate_attendance_monthly_chart(monthly_data)
    
    # Subject-wise attendance
    subject_data = {}
    for subject in subjects if subjects else []:
        subject_name = subject.get('subject_name', 'Unknown')
        subject_data[subject_name] = 87.5
    
    if subject_data:
        charts['subject_attendance'] = generate_subject_attendance_chart(subject_data)
    
    # Class/Division strength
    class_data = {}
    for div in divisions if divisions else []:
        div_name = div.get('division_name', 'Unknown')
        class_data[div_name] = 60
    
    if class_data:
        charts['class_strength'] = generate_class_strength_chart(class_data)

    return render_template(
        "hod/dashboard.html",
        context=context,
        stats=department_stats,
        faculty=faculty_members,
        divisions=divisions,
        subjects=subjects,
        attendance_summary=attendance_summary,
        timetable_overview=timetable_overview,
        timetable_days=DataHelper.get_timetable_days(dept_id),
        charts=charts
    )


@hod_bp.route("")
def hod_redirect():
    """Redirect to HOD dashboard"""
    return hdashboard()


@hod_bp.route("/faculty")
def hod_faculty_directory():
    """Show faculty directory for the department"""
    context = _get_hod_context()
    
    # Fallback if no department
    if not context['dept_id']:
        return render_template(
            "hod/faculty.html",
            context=context,
            faculty_cards=[],
            subject_catalog=[]
        )

    dept_id = context['dept_id']
    faculty_members = DataHelper.get_faculty(dept_id=dept_id)
    timetable_entries = DataHelper.get_timetable(dept_id=dept_id)

    load_map = {}
    for entry in timetable_entries:
        load_entry = load_map.setdefault(
            entry['faculty_id'],
            {'lectures': 0, 'subjects': set(), 'divisions': set()}
        )
        load_entry['lectures'] += 1
        load_entry['subjects'].add(entry['subject_name'])
        load_entry['divisions'].add(entry['division_name'])

    faculty_cards = []
    for member in faculty_members:
        assignments = load_map.get(member['faculty_id'], {'lectures': 0, 'subjects': set(), 'divisions': set()})
        faculty_cards.append(
            {
                **member,
                'lectures_per_week': assignments['lectures'],
                'subjects': sorted(assignments['subjects']),
                'divisions': sorted(assignments['divisions'])
            }
        )

    return render_template(
        "hod/faculty.html",
        context=context,
        faculty_cards=faculty_cards,
        subject_catalog=DataHelper.get_subjects(dept_id=dept_id)
    )


@hod_bp.route("/subjects")
def hod_subjects():
    """List subjects offered in the department"""
    context = _get_hod_context()
    
    # Fallback if no department
    if not context['dept_id']:
        return render_template(
            "hod/subjects.html",
            context=context,
            grouped_subjects={}
        )

    grouped_subjects = DataHelper.get_subjects_grouped_by_semester(context['dept_id'])

    return render_template(
        "hod/subjects.html",
        context=context,
        grouped_subjects=grouped_subjects
    )


@hod_bp.route("/subjects/add", methods=['POST'])
@hod_required
def hod_add_subject():
    """Add a new subject"""
    from models.subject import Subject
    try:
        data = request.get_json()
        context = _get_hod_context()
        
        new_subject = Subject(
            dept_id=context['dept_id'],
            semester_id=data.get('semester_id'),
            subject_name=data.get('subject_name'),
            subject_code=data.get('subject_code'),
            credits=data.get('credits')
        )
        db.session.add(new_subject)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subject added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/subjects/edit", methods=['POST'])
@hod_required
def hod_edit_subject():
    """Edit an existing subject"""
    from models.subject import Subject
    try:
        data = request.get_json()
        subject = Subject.query.get(data.get('subject_id'))
        
        if not subject:
            return jsonify({'success': False, 'message': 'Subject not found'}), 404
        
        subject.subject_name = data.get('subject_name')
        subject.subject_code = data.get('subject_code')
        subject.semester_id = data.get('semester_id')
        subject.credits = data.get('credits')
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subject updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/subjects/delete/<int:subject_id>", methods=['DELETE'])
@hod_required
def hod_delete_subject(subject_id):
    """Delete a subject"""
    from models.subject import Subject
    try:
        subject = Subject.query.get(subject_id)
        
        if not subject:
            return jsonify({'success': False, 'message': 'Subject not found'}), 404
        
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subject deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/analytics/data")
def hod_analytics_data():
    """Provide filtered attendance data as JSON"""
    context = _get_hod_context()
    
    # Fallback if no department
    if not context['dept_id']:
        return jsonify({'records': []})

    division_id = request.args.get('division_id', type=int)
    subject_id = request.args.get('subject_id', type=int)

    records = DataHelper.get_attendance_records(
        dept_id=context['dept_id'],
        division_id=division_id,
        subject_id=subject_id
    )

    return jsonify({'records': records})


@hod_bp.route("/attendance/report")
def hod_attendance_report():
    """Download attendance report as CSV"""
    context = _get_hod_context()

    if not context['dept_id']:
        return jsonify({'success': False, 'message': 'Department not configured'}), 400

    division_id = request.args.get('division_id', type=int)
    subject_id = request.args.get('subject_id', type=int)

    records = DataHelper.get_attendance_records(
        dept_id=context['dept_id'],
        division_id=division_id,
        subject_id=subject_id
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Student ID',
        'Student Name',
        'Department',
        'Division',
        'Subject',
        'Subject Code',
        'Total Lectures',
        'Attended Lectures',
        'Attendance %',
        'Status',
        'Last Updated'
    ])

    for record in records:
        writer.writerow([
            record.get('student_id', ''),
            record.get('student_name', ''),
            record.get('dept_name', ''),
            record.get('division_name', ''),
            record.get('subject_name', ''),
            record.get('subject_code', ''),
            record.get('total_lectures', 0),
            record.get('attended_lectures', 0),
            record.get('attendance_percentage', 0),
            record.get('status', ''),
            record.get('last_updated', '')
        ])

    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=hod_attendance_report.csv'
    return response


@hod_bp.route("/timetable")
def hod_timetable():
    """Manage and review department timetable"""
    context = _get_hod_context()
    
    # Fallback if no department
    if not context['dept_id']:
        return render_template(
            "hod/timetable.html",
            context=context,
            divisions=[],
            subjects=[],
            faculty_members=[],
            timetable_overview={},
            timetable_days=[]
        )

    dept_id = context['dept_id']
    divisions = DataHelper.get_divisions(dept_id=dept_id)
    subjects = DataHelper.get_subjects(dept_id=dept_id)
    faculty_members = DataHelper.get_faculty(dept_id=dept_id)

    return render_template(
        "hod/timetable.html",
        context=context,
        divisions=divisions,
        subjects=subjects,
        faculty_members=faculty_members,
        timetable_overview=DataHelper.get_timetable_overview(dept_id),
        timetable_days=DataHelper.get_timetable_days(dept_id)
    )


@hod_bp.route("/timetable/data")
def hod_timetable_data():
    """Return timetable entries filtered by division and day"""
    context = _get_hod_context()
    
    # Fallback if no department
    if not context['dept_id']:
        return jsonify({'timetable': []})

    division_id = request.args.get('division_id', type=int)
    day = request.args.get('day')

    entries = DataHelper.get_timetable(
        dept_id=context['dept_id'],
        division_id=division_id,
        day=day
    )

    return jsonify({'entries': entries})


@hod_bp.route("/timetable/entry", methods=['POST'])
def hod_save_timetable_entry():
    """Create or update timetable entry"""
    payload = request.get_json() or {}
    required = ['division_id', 'subject_id', 'faculty_id', 'day', 'start_time', 'end_time']

    missing = [field for field in required if field not in payload]
    if missing:
        abort(400, description=f"Missing required fields: {', '.join(missing)}")

    normalized_payload = {
        'entry_id': payload.get('entry_id'),
        'division_id': int(payload['division_id']),
        'subject_id': int(payload['subject_id']),
        'faculty_id': int(payload['faculty_id']),
        'day': payload['day'],
        'start_time': payload['start_time'],
        'end_time': payload['end_time'],
        'room_no': payload.get('room_no', ''),
        'mode': payload.get('mode', 'Lecture')
    }

    try:
        entry = DataHelper.save_timetable_entry(normalized_payload)
    except ValueError as exc:
        abort(400, description=str(exc))

    return jsonify({'status': 'success', 'entry': entry})


@hod_bp.route("/timetable/entry/<int:entry_id>", methods=['DELETE'])
def hod_delete_timetable_entry(entry_id):
    """Delete timetable entry"""
    if not DataHelper.delete_timetable_entry(entry_id):
        abort(404, description="Timetable entry not found")
    return jsonify({'status': 'success', 'entry_id': entry_id})


@hod_bp.route("/profile")
@hod_required
def hod_profile():
    """HOD Profile"""
    context = _get_hod_context()
    
    # Fallback if no department
    if not context['dept_id']:
        return render_template(
            "hod/profile.html",
            title="HOD Profile",
            user=context['user'],
            faculty=context['faculty'],
            department=context['department'],
            college=DataHelper.get_college(),
            dept_stats={}
        )

    dept_stats = DataHelper.get_department_stats(context['dept_id'])

    return render_template(
        "hod/profile.html",
        title="HOD Profile",
        user=context['user'],
        faculty=context['faculty'],
        department=context['department'],
        college=DataHelper.get_college(),
        dept_stats=dept_stats
    )


@hod_bp.route("/profile/update", methods=['POST'])
@hod_required
def hod_update_profile():
    """Update HOD profile"""
    from models.faculty import Faculty
    try:
        data = request.get_json()
        context = _get_hod_context()
        
        # Update user information
        user = User.query.get(context['user']['user_id'])
        if user:
            user.name = data.get('name')
            user.email = data.get('email')
            user.mobile = data.get('mobile')
        
        # Update faculty information
        faculty = Faculty.query.get(context['faculty']['faculty_id'])
        if faculty:
            faculty.short_name = data.get('short_name')
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/profile/change-password", methods=['POST'])
@hod_required
def hod_change_password():
    """Change HOD password"""
    try:
        data = request.get_json()
        context = _get_hod_context()
        
        user = User.query.get(context['user']['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Verify current password
        if not user.check_password(data.get('current_password')):
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
        
        # Set new password
        user.set_password(data.get('new_password'))
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/approvals")
def hod_approvals():
    """View pending student, faculty, and parent approvals in department"""
    context = _get_hod_context()
    
    if not context['dept_id']:
        return render_template("hod/approvals.html",
                             title="Pending Approvals",
                             context=context,
                             pending_users=[])
    
    # Get pending students, faculty, and parents in this department
    pending_users = User.query.filter(
        User.is_approved == False,
        User.role_id.in_([4, 5, 6])  # FACULTY=4, STUDENT=5, PARENT=6
    ).all()
    
    # Filter by department (need to check through faculty/student relationships)
    dept_pending = []
    for user in pending_users:
        if user.role_id == 4 and user.faculty:  # Faculty
            if user.faculty.dept_id == context['dept_id']:
                dept_pending.append(user)
        elif user.role_id == 5 and user.student:  # Student
            if user.student.dept_id == context['dept_id']:
                dept_pending.append(user)
        elif user.role_id == 6:  # Parent
            dept_pending.append(user)
    
    return render_template("hod/approvals.html",
                          title="Pending Approvals",
                          context=context,
                          pending_users=dept_pending)


@hod_bp.route("/approve/user/<int:user_id>", methods=['POST'])
def hod_approve_user(user_id):
    """Approve a student, faculty, or parent"""
    try:
        user = User.query.get(user_id)
        if user and user.role_id in [4, 5, 6]:  # FACULTY, STUDENT, PARENT
            user.is_approved = True
            db.session.commit()
            return jsonify({'success': True, 'message': f'{user.role.role_name} "{user.name}" approved successfully'})
        return jsonify({'success': False, 'message': 'User not found or invalid role'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/reject/user/<int:user_id>", methods=['POST'])
def hod_reject_user(user_id):
    """Reject/Delete a user"""
    try:
        user = User.query.get(user_id)
        if user:
            user_name = user.name
            user_role = user.role.role_name
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': f'{user_role} "{user_name}" rejected and removed'})
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/compiled-attendance")
def hod_compiled_attendance():
    """View compiled attendance report by student and subject"""
    context = _get_hod_context()
    
    if not context['dept_id']:
        return render_template(
            "hod/compiled_attendance.html",
            context=context,
            report_data=[],
            divisions=[],
            subjects=[]
        )
    
    # Get filter parameters
    division_id = request.args.get('division_id', type=int)
    semester_id = request.args.get('semester_id', type=int)
    
    # Get report data
    report_data = DataHelper.get_compiled_attendance_report(
        dept_id=context['dept_id'],
        semester_id=semester_id,
        division_id=division_id
    )
    
    # Sort by roll number
    report_data = sorted(report_data, key=lambda x: x['roll_no'])
    
    divisions = DataHelper.get_divisions(dept_id=context['dept_id'])
    semesters = DataHelper.get_semesters()
    
    return render_template(
        "hod/compiled_attendance.html",
        context=context,
        report_data=report_data,
        divisions=divisions,
        semesters=semesters,
        selected_division_id=division_id,
        selected_semester_id=semester_id
    )


@hod_bp.route("/compiled-attendance/export")
def hod_compiled_attendance_export():
    """Export compiled attendance as CSV"""
    context = _get_hod_context()
    
    if not context['dept_id']:
        return jsonify({'success': False, 'message': 'Department not configured'}), 400
    
    division_id = request.args.get('division_id', type=int)
    semester_id = request.args.get('semester_id', type=int)
    
    report_data = DataHelper.get_compiled_attendance_report(
        dept_id=context['dept_id'],
        semester_id=semester_id,
        division_id=division_id
    )
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    subjects = list(set([
        subj for student in report_data 
        for subj in student['subjects'].keys()
    ]))
    
    header = [
        'Roll No',
        'Enrollment No',
        'Name',
        'Division',
        'Branch',
        'Mentor'
    ]
    
    for subject_id in sorted(subjects):
        for student in report_data:
            if subject_id in student['subjects']:
                subject = student['subjects'][subject_id]
                header.extend([
                    f"{subject['subject_code']} Attended",
                    f"{subject['subject_code']} Total",
                    f"{subject['subject_code']} %"
                ])
                break
    
    header.extend(['Total Attended', 'Total Lectures', 'Overall %'])
    writer.writerow(header)
    
    # Write data rows
    for student in report_data:
        row = [
            student['roll_no'],
            student['enrollment_no'],
            student['name'],
            student['division'],
            student['branch'],
            student['mentor']
        ]
        
        for subject_id in sorted(subjects):
            if subject_id in student['subjects']:
                subject = student['subjects'][subject_id]
                row.extend([
                    subject['attended'],
                    subject['total'],
                    f"{subject['percentage']:.2f}"
                ])
        
        row.extend([
            student['total_attended'],
            student['total_lectures'],
            f"{student['overall_percentage']:.2f}"
        ])
        
        writer.writerow(row)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=compiled_attendance_report.csv'
    return response


@hod_bp.route("/attendance")
@hod_required
def hod_attendance():
    """Mark attendance for department divisions"""
    from datetime import datetime as dt, timedelta
    from models.timetable import Timetable
    from models.subject import Subject
    from models.academic_calendar import AcademicCalendar
    
    context = _get_hod_context()
    
    if not context['dept_id']:
        return render_template("hod/attendance.html", divisions=[], error="Department not found")
    
    divisions = DataHelper.get_divisions(dept_id=context['dept_id'])
    
    # For each division, add subjects taught
    for division in divisions:
        division['subjects'] = []
        
        # Get unique subjects for this division
        timetable_entries = Timetable.query.filter_by(
            division_id=division['div_id']
        ).all()
        
        subjects_data = []
        for timetable in timetable_entries:
            subject = timetable.subject
            
            # Find next scheduled lecture date
            today = dt.now().date()
            next_lecture = None
            
            for days_ahead in range(30):
                check_date = today + timedelta(days=days_ahead)
                day_name = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'][check_date.weekday()]
                
                if timetable.day_of_week == day_name:
                    is_holiday = AcademicCalendar.query.filter_by(
                        event_date=check_date,
                        dept_id=context['dept_id']
                    ).first()
                    
                    if not is_holiday:
                        next_lecture = check_date
                        break
            
            subjects_data.append({
                'id': subject.subject_id,
                'name': subject.subject_name,
                'code': subject.subject_code,
                'faculty': timetable.faculty.short_name if timetable.faculty else 'N/A',
                'next_lecture': next_lecture.strftime('%Y-%m-%d') if next_lecture else 'No schedule'
            })
        
        division['subjects'] = subjects_data
    
    divisions = [d for d in divisions if d.get('subjects')]
    
    return render_template("hod/attendance.html", divisions=divisions, datetime=dt)


@hod_bp.route("/attendance/mark", methods=['POST'])
@hod_required
def hod_mark_attendance():
    """Mark attendance for a lecture"""
    try:
        data = request.get_json()
        division_id = data.get('division_id')
        subject_id = data.get('subject_id')
        lecture_date = data.get('lecture_date')
        attendance_data = data.get('attendance')
        
        if not all([division_id, subject_id, lecture_date, attendance_data]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        from models.timetable import Timetable
        from models.lecture import Lecture
        from models.attendance import Attendance, AttendanceStatus
        from models.academic_calendar import AcademicCalendar
        from models.student import Student
        from datetime import datetime as dt
        
        context = _get_hod_context()
        
        # Verify division belongs to HOD's department
        division = Division.query.get(division_id)
        if not division or division.dept_id != context['dept_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Parse and validate date
        try:
            lecture_date_obj = dt.strptime(lecture_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        # Check academic calendar
        is_holiday = AcademicCalendar.query.filter_by(
            event_date=lecture_date_obj,
            dept_id=context['dept_id']
        ).first()
        
        if is_holiday:
            return jsonify({'error': f'Cannot mark attendance on {is_holiday.description or "holiday"}'}), 400
        
        # Get timetable
        timetable = Timetable.query.filter_by(
            subject_id=subject_id,
            division_id=division_id
        ).first()
        
        if not timetable:
            return jsonify({'error': 'Timetable entry not found'}), 404
        
        # Verify day
        day_of_week = lecture_date_obj.strftime('%A')
        timetable_day_map = {'Monday': 'MON', 'Tuesday': 'TUE', 'Wednesday': 'WED', 'Thursday': 'THU', 'Friday': 'FRI', 'Saturday': 'SAT', 'Sunday': 'SUN'}
        expected_day = timetable_day_map.get(day_of_week, '')
        
        if expected_day != timetable.day_of_week:
            return jsonify({'error': f'No class scheduled on {day_of_week}'}), 400
        
        # Create or get lecture
        lecture = Lecture.query.filter_by(
            timetable_id=timetable.timetable_id,
            lecture_date=lecture_date_obj
        ).first()
        
        if not lecture:
            lecture = Lecture(
                timetable_id=timetable.timetable_id,
                lecture_date=lecture_date_obj
            )
            db.session.add(lecture)
            db.session.flush()
        
        # Get statuses
        present_status = AttendanceStatus.query.filter_by(status_name='PRESENT').first()
        absent_status = AttendanceStatus.query.filter_by(status_name='ABSENT').first()
        
        if not present_status or not absent_status:
            return jsonify({'error': 'Attendance status not configured'}), 500
        
        # Mark attendance
        marked_count = 0
        for record in attendance_data:
            student_id = record.get('student_id')
            status = record.get('status', 'PRESENT')
            
            student = Student.query.get(student_id)
            if not student or student.division_id != division_id:
                continue
            
            existing = Attendance.query.filter_by(
                student_id=student_id,
                lecture_id=lecture.lecture_id
            ).first()
            
            status_id = present_status.status_id if status == 'PRESENT' else absent_status.status_id
            
            if existing:
                existing.status_id = status_id
                existing.marked_at = dt.utcnow()
            else:
                new_attendance = Attendance(
                    student_id=student_id,
                    lecture_id=lecture.lecture_id,
                    status_id=status_id,
                    marked_at=dt.utcnow()
                )
                db.session.add(new_attendance)
            
            marked_count += 1
        
        db.session.commit()
        return jsonify({'message': f'Attendance marked for {marked_count} students'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@hod_bp.route("/analytics")
@hod_required
def hod_analytics():
    """View department analytics"""
    context = _get_hod_context()
    
    if not context['dept_id']:
        return render_template("hod/analytics.html", context=context, charts={})
    
    # Get department data
    attendance_data = DataHelper.get_attendance_records(dept_id=context['dept_id'])
    
    total_lectures = sum(r.get('total_lectures', 0) for r in attendance_data)
    avg_attendance = DataHelper._np_mean([a.get('attendance_percentage', 0) for a in attendance_data]) if attendance_data else 0
    
    # Generate charts
    from services.chart_helper import (
        generate_subject_attendance_chart,
        generate_attendance_monthly_chart,
        generate_class_strength_chart
    )
    
    charts = {}
    
    # Subject-wise attendance
    subject_data = {}
    for record in attendance_data:
        subject_name = record.get('subject_name', 'Unknown')
        if subject_name not in subject_data:
            subject_data[subject_name] = []
        subject_data[subject_name].append(record.get('attendance_percentage', 0))
    
    subject_stats = {name: round(DataHelper._np_mean(values), 2) for name, values in subject_data.items()}
    if subject_stats:
        charts['subject_attendance'] = generate_subject_attendance_chart(subject_stats)
    
    # Division-wise attendance
    division_data = {}
    for record in attendance_data:
        division_name = record.get('division_name', 'Unknown')
        if division_name not in division_data:
            division_data[division_name] = []
        division_data[division_name].append(record.get('attendance_percentage', 0))
    
    division_stats = {name: round(DataHelper._np_mean(values), 2) for name, values in division_data.items()}
    if division_stats:
        charts['class_strength'] = generate_class_strength_chart(division_stats)
    
    return render_template(
        "hod/analytics.html",
        context=context,
        attendance_data=attendance_data,
        total_lectures=total_lectures,
        avg_attendance=round(avg_attendance, 2),
        charts=charts
    )


@hod_bp.route("/reports")
@hod_required
def hod_reports():
    """View department reports"""
    context = _get_hod_context()
    
    if not context['dept_id']:
        return render_template("hod/reports.html", context=context, students=[])
    
    # Get attendance for all students in department
    attendance_data = DataHelper.get_attendance_records(dept_id=context['dept_id'])
    students = DataHelper.get_students(dept_id=context['dept_id'])
    
    # Build report
    student_reports = {}
    for student in students:
        student_id = student.get('student_id')
        student_records = [r for r in attendance_data if r['student_id'] == student_id]
        
        student_reports[student_id] = {
            'student_id': student_id,
            'roll_no': student.get('roll_no', ''),
            'name': student.get('name', ''),
            'enrollment_no': student.get('enrollment_no', ''),
            'division_name': student.get('division_name', ''),
            'subjectwise_attendance': {},
            'overall_attendance': 0,
            'total_lectures': 0,
            'attended_lectures': 0
        }
        
        for record in student_records:
            subject_name = record.get('subject_name', 'Unknown')
            student_reports[student_id]['subjectwise_attendance'][subject_name] = {
                'subject_code': record.get('subject_code', ''),
                'attendance_percentage': round(record.get('attendance_percentage', 0), 2),
                'total_lectures': record.get('total_lectures', 0),
                'attended_lectures': record.get('attended_lectures', 0)
            }
        
        if student_records:
            percentages = [r.get('attendance_percentage', 0) for r in student_records]
            student_reports[student_id]['overall_attendance'] = round(DataHelper._np_mean(percentages), 2)
            student_reports[student_id]['total_lectures'] = sum(r.get('total_lectures', 0) for r in student_records)
            student_reports[student_id]['attended_lectures'] = sum(r.get('attended_lectures', 0) for r in student_records)
    
    student_reports_list = sorted(student_reports.values(), key=lambda x: (x.get('division_name'), int(x.get('roll_no', 0) or 0)))
    
    return render_template(
        "hod/reports.html",
        context=context,
        students=student_reports_list,
        attendance_data=attendance_data
    )


@hod_bp.route("/approvals")
@hod_required
def hod_approvals():
    """View pending approvals for faculty and students in department"""
    context = _get_hod_context()
    
    pending_users = User.query.filter(
        User.is_approved == False,
        User.role_id.in_([3, 4, 5, 6])  # HOD, FACULTY, STUDENT, PARENT
    ).all()
    
    return render_template(
        "hod/approvals.html",
        context=context,
        pending_users=pending_users
    )


@hod_bp.route("/approve/user/<int:user_id>", methods=['POST'])
@hod_required
def hod_approve_user(user_id):
    """Approve a user"""
    try:
        user = User.query.get(user_id)
        if user and user.role_id in [3, 4, 5, 6]:
            user.is_approved = True
            db.session.commit()
            return jsonify({'success': True, 'message': f'User approved successfully'})
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/reject/user/<int:user_id>", methods=['POST'])
@hod_required
def hod_reject_user(user_id):
    """Reject a user"""
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': 'User rejected'})
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@hod_bp.route("/export/csv")
@hod_required
def export_attendance_csv():
    """Export compiled attendance report as CSV"""
    try:
        csv_output = ExportService.export_csv()
        return send_file(
            io.BytesIO(csv_output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'compiled_attendance_week12_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hod_bp.route("/export/pdf")
@hod_required
def export_attendance_pdf():
    """Export compiled attendance report as PDF"""
    try:
        pdf_output = ExportService.export_pdf()
        return send_file(
            pdf_output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'compiled_attendance_week12_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except RuntimeError as e:
        return jsonify({'error': str(e), 'message': 'reportlab library required'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
