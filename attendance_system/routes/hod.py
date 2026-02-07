"""
HOD (Head of Department) routes - dashboard, management pages, and APIs
"""
from flask import Blueprint, render_template, request, jsonify, abort

from models.user import db, User
from services.data_helper import DataHelper
from utils.auth_decorators import login_required, hod_required
from services.chart_helper import (
    generate_attendance_monthly_chart,
    generate_subject_attendance_chart,
    generate_class_strength_chart
)

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


@hod_bp.route("/attendance")
def hod_attendance():
    """Division wise attendance analytics"""
    context = _get_hod_context()
    
    # Fallback if no department
    if not context['dept_id']:
        return render_template(
            "hod/attendance.html",
            context=context,
            attendance_summary={},
            divisions=[],
            subjects=[]
        )

    summary = DataHelper.get_division_attendance_summary(context['dept_id'])

    return render_template(
        "hod/attendance.html",
        context=context,
        attendance_summary=summary,
        divisions=DataHelper.get_divisions(dept_id=context['dept_id']),
        subjects=DataHelper.get_subjects(dept_id=context['dept_id'])
    )


@hod_bp.route("/attendance/data")
def hod_attendance_data():
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
