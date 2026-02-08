"""
College Admin routes - Dashboard, Departments, Divisions, Faculty, Students, Analytics, Settings
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.division import Division
from models.user import db, User
from services.data_helper import DataHelper
from attendance_system.utils.auth_decorators import login_required, college_admin_required
from services.chart_helper import (
    generate_department_comparison_chart,
    generate_class_strength_chart,
    generate_attendance_monthly_chart
)

college_bp = Blueprint('college', __name__, url_prefix='/college')


@college_bp.route("/dashboard")
@college_admin_required
def college_dashboard():
    """College Dashboard with departments and divisions overview"""
    college = DataHelper.get_college()
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    
    # Calculate total student count
    total_student_count = sum(dept.get('student_count', 0) for dept in (departments or []))
    
    # Generate charts
    charts = {}
    
    # Department comparison chart
    dept_data = {}
    for dept in departments if departments else []:
        dept_name = dept.get('dept_name', 'Unknown')
        student_count = dept.get('student_count', 45)  # Get from data or use default
        dept_data[dept_name] = student_count
    
    if dept_data:
        charts['department_comparison'] = generate_department_comparison_chart(dept_data)
    
    # Class strength chart
    class_data = {}
    for div in divisions if divisions else []:
        div_name = div.get('division_name', 'Unknown')
        student_count = div.get('student_count', 60)  # Get from data or use default
        class_data[div_name] = student_count
    
    if class_data:
        charts['class_strength'] = generate_class_strength_chart(class_data)
    
    # Monthly attendance chart
    monthly_data = {
        'Week 1': 91.5,
        'Week 2': 89.3,
        'Week 3': 92.1,
        'Week 4': 88.6
    }
    charts['monthly_attendance'] = generate_attendance_monthly_chart(monthly_data)
    
    return render_template("college/dashboard.html",
                         title="College Dashboard",
                         college=college,
                         departments=departments,
                         divisions=divisions,
                         student_count=total_student_count,
                         charts=charts)


@college_bp.route("/profile")
@college_admin_required
def college_profile():
    """College Profile"""
    from models.user import User
    from models.college import College
    
    # Get current user
    user_data = DataHelper.get_user('college')
    
    # Get college
    college = None
    if user_data and user_data.get('college_id'):
        college = College.query.get(user_data['college_id'])
    
    college_id = college.college_id if college else None
    college_stats = DataHelper.get_college_statistics(college_id) if college_id else {
        'total_departments': 0,
        'total_faculty': 0,
        'total_students': 0,
        'total_divisions': 0,
        'avg_attendance': 0,
        'total_users': 0
    }
    
    return render_template("college/profile.html",
                         title="College Profile",
                         user=user_data,
                         college=college,
                         college_stats=college_stats)


@college_bp.route("/departments")
def college_departments():
    """College Departments List"""
    departments = DataHelper.get_departments()
    faculty = DataHelper.get_faculty()
    return render_template("college/departments.html",
                         title="Departments",
                         departments=departments,
                         faculty=faculty)


@college_bp.route("/divisions")
def college_divisions():
    """College Divisions List"""
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    
    return render_template("college/divisions.html",
                         title="Divisions",
                         departments=departments,
                         divisions=divisions)


@college_bp.route("/divisions/create", methods=['GET', 'POST'])
def college_divisions_create():
    """Create New Division"""
    if request.method == 'POST':
        dept_id = request.form.get('dept_id')
        division_name = request.form.get('division_name')
        division_code = request.form.get('division_code')
        capacity = request.form.get('capacity')
        
        if not dept_id or not division_name:
            flash('Department and Division Name are required.', 'error')
        else:
            try:
                new_division = Division(
                    dept_id=dept_id,
                    division_name=division_name,
                    # division_code=division_code, # Not in model? Check model again.
                    capacity=int(capacity) if capacity else 60
                )
                db.session.add(new_division)
                db.session.commit()
                flash('Division created successfully!', 'success')
                return redirect(url_for('college.college_divisions'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating division: {str(e)}', 'error')

    departments = DataHelper.get_departments()
    
    return render_template("college/create_division.html",
                         title="Create Division",
                         departments=departments)


@college_bp.route("/faculty")
def college_faculty():
    """College Faculty List"""
    departments = DataHelper.get_departments()
    faculty = DataHelper.get_faculty()
    
    return render_template("college/faculty.html",
                         title="Faculty Management",
                         departments=departments,
                         faculty=faculty)


@college_bp.route("/faculty/hod-list")
def college_faculty_hod_list():
    """College HOD List"""
    departments = DataHelper.get_departments()
    hod_list = []
    
    for dept in departments if departments else []:
        if dept.get('hod_faculty_id'):
            hod_faculty = DataHelper.get_faculty_member(dept['hod_faculty_id'])
            if hod_faculty:
                hod_list.append({
                    'department': dept,
                    'hod': hod_faculty
                })
    
    return render_template("college/hod_list.html",
                         title="HOD Management",
                         departments=departments,
                         hod_list=hod_list)


@college_bp.route("/students")
def college_students():
    """College Students List"""
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    students = DataHelper.get_students()
    
    # Calculate total student count
    student_count = len(students) if students else 0
    
    # Add student count to each department
    for dept in departments if departments else []:
        dept_students = [s for s in (students or []) if s.get('dept_id') == dept.get('dept_id')]
        dept['student_count'] = len(dept_students)
    
    return render_template("college/students.html",
                         title="Student Management",
                         departments=departments,
                         divisions=divisions,
                         students=students,
                         student_count=student_count)


@college_bp.route("/students/by-division")
def college_students_by_division():
    """College Students Filtered by Division"""
    division_id = request.args.get('div_id')
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    
    students = DataHelper.get_students()
    if division_id:
        students = [s for s in students if s.get('div_id') == division_id]
    
    # Calculate total student count
    student_count = len(students) if students else 0
    
    # Add student count to each department
    for dept in departments if departments else []:
        dept_students = [s for s in (students or []) if s.get('dept_id') == dept.get('dept_id')]
        dept['student_count'] = len(dept_students)
    
    return render_template("college/students.html",
                         title="Student Management",
                         departments=departments,
                         divisions=divisions,
                         students=students,
                         student_count=student_count,
                         selected_division=division_id)


@college_bp.route("/attendance-analytics")
def college_attendance_analytics():
    """College Attendance Analytics"""
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    analytics_payload = DataHelper.get_college_attendance_analytics()

    return render_template(
        "college/attendance-analytics.html",
        title="Attendance Analytics",
        departments=departments,
        divisions=divisions,
        stats=analytics_payload['stats'],
        attendance_records=analytics_payload['attendance_records'],
        charts=analytics_payload['charts']
    )


@college_bp.route("/settings")
def college_settings():
    """College Settings"""
    college = DataHelper.get_college()
    
    return render_template("college/settings.html",
                         title="College Settings",
                         college=college)


@college_bp.route("/approvals")
def college_approvals():
    """View pending faculty and HOD approvals"""
    college = DataHelper.get_college()
    
    # Get pending faculty and HOD users
    pending_users = User.query.filter(
        User.college_id == college['college_id'],
        User.is_approved == False,
        User.role_id.in_([3, 4])  # HOD=3, FACULTY=4
    ).all()
    
    return render_template("college/approvals.html",
                          title="Pending Approvals",
                          college=college,
                          pending_users=pending_users)


@college_bp.route("/approve/user/<int:user_id>", methods=['POST'])
def approve_user(user_id):
    """Approve a faculty or HOD user"""
    try:
        user = User.query.get(user_id)
        if user and user.role_id in [3, 4]:  # HOD or FACULTY
            user.is_approved = True
            db.session.commit()
            return jsonify({'success': True, 'message': f'User "{user.name}" approved successfully'})
        return jsonify({'success': False, 'message': 'User not found or invalid role'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@college_bp.route("/reject/user/<int:user_id>", methods=['POST'])
def reject_user(user_id):
    """Reject/Delete a user"""
    try:
        user = User.query.get(user_id)
        if user:
            user_name = user.name
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': f'User "{user_name}" rejected and removed'})
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
