"""
Super Admin routes - System-wide Dashboard and Administration
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from services.data_helper import DataHelper
from models.user import db
from models.college import College
from utils.auth_decorators import login_required, superadmin_required
from services.chart_helper import (
    generate_role_distribution_chart,
    generate_department_comparison_chart,
    generate_class_strength_chart,
    generate_attendance_monthly_chart
)

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')


def _get_superadmin_context():
    """Get superadmin user context"""
    superadmin_user = DataHelper.get_user('superadmin')
    return {'user': superadmin_user}


@superadmin_bp.route("/dashboard")
@superadmin_required
def sudashboard():
    """Super Admin Dashboard - System Overview"""
    context = _get_superadmin_context()
    
    # Get system-wide statistics
    colleges = DataHelper.get_all_colleges()
    total_students = DataHelper.get_total_students_count()
    total_faculty = DataHelper.get_total_faculty_count()
    total_departments = DataHelper.get_total_departments_count()
    
    # Get pending approvals count
    pending_colleges_count = College.query.filter_by(is_approved=False).count()
    
    # Get recent activities
    recent_registrations = DataHelper.get_recent_users(limit=5)
    
    # College-wise statistics
    college_stats = []
    for college in colleges:
        stats = DataHelper.get_college_statistics(college['college_id'])
        college_stats.append({
            'college': college,
            'stats': stats
        })
    
    # Generate charts
    charts = {}
    
    # Role distribution chart
    role_data = {
        'SUPERADMIN': 1,
        'ADMIN': 1,
        'HOD': total_departments,
        'FACULTY': total_faculty,
        'STUDENT': total_students,
        'PARENT': int(total_students * 0.8)  # Estimate
    }
    charts['role_distribution'] = generate_role_distribution_chart(role_data)
    
    # Department comparison chart
    dept_data = {}
    for college in colleges:
        depts = DataHelper.get_departments()
        for dept in depts if depts else []:
            dept_name = dept.get('dept_name', 'Unknown')
            student_count = len(DataHelper.get_students()) if DataHelper.get_students() else 0
            dept_data[dept_name] = student_count
    
    if dept_data:
        charts['department_comparison'] = generate_department_comparison_chart(dept_data)
    
    # Class strength chart (divisions)
    divisions_data = {}
    divisions = DataHelper.get_divisions()
    for div in divisions if divisions else []:
        div_name = div.get('division_name', 'Unknown')
        student_count = len(DataHelper.get_students()) if DataHelper.get_students() else 0
        divisions_data[div_name] = student_count
    
    if divisions_data:
        charts['class_strength'] = generate_class_strength_chart(divisions_data)
    
    # Monthly attendance trend (sample data)
    monthly_data = {
        'Week 1': 92.5,
        'Week 2': 88.3,
        'Week 3': 90.1,
        'Week 4': 87.6
    }
    charts['monthly_attendance'] = generate_attendance_monthly_chart(monthly_data)
    
    return render_template("superadmin/dashboard.html",
                          context=context,
                          colleges=colleges,
                          college_stats=college_stats,
                          total_students=total_students,
                          total_faculty=total_faculty,
                          total_departments=total_departments,
                          pending_colleges_count=pending_colleges_count,
                          recent_registrations=recent_registrations,
                          charts=charts)


@superadmin_bp.route("")
def superadmin_redirect():
    """Redirect to super admin dashboard"""
    return sudashboard()


@superadmin_bp.route("/colleges")
def colleges():
    """View all colleges"""
    context = _get_superadmin_context()
    colleges_list = DataHelper.get_all_colleges()
    
    # Get detailed stats for each college
    colleges_with_stats = []
    for college in colleges_list:
        stats = DataHelper.get_college_statistics(college['college_id'])
        colleges_with_stats.append({
            **college,
            'stats': stats
        })
    
    return render_template("superadmin/colleges.html",
                          context=context,
                          colleges=colleges_with_stats)


@superadmin_bp.route("/college/<int:college_id>")
def college_details(college_id):
    """View specific college details"""
    context = _get_superadmin_context()
    college = DataHelper.get_college()
    
    # Get college data
    departments = DataHelper.get_departments()
    students = DataHelper.get_students()
    faculty = DataHelper.get_faculty_members()
    divisions = DataHelper.get_divisions()
    
    # Get statistics
    stats = DataHelper.get_college_statistics(college_id)
    
    return render_template("superadmin/college_details.html",
                          context=context,
                          college=college,
                          departments=departments,
                          students=students,
                          faculty=faculty,
                          divisions=divisions,
                          stats=stats)


@superadmin_bp.route("/students")
def students():
    """View all students across all colleges"""
    context = _get_superadmin_context()
    all_students = DataHelper.get_students()
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    
    return render_template("superadmin/students.html",
                          context=context,
                          students=all_students,
                          departments=departments,
                          divisions=divisions)


@superadmin_bp.route("/departments")
def departments():
    """View all departments across all colleges"""
    context = _get_superadmin_context()
    all_departments = DataHelper.get_departments()
    
    # Get detailed stats for each department
    departments_with_stats = []
    for dept in all_departments:
        dept_students = [s for s in DataHelper.get_students() if s.get('dept_id') == dept['dept_id']]
        dept_faculty = [f for f in DataHelper.get_faculty_members() if f.get('dept_id') == dept['dept_id']]
        
        departments_with_stats.append({
            **dept,
            'student_count': len(dept_students),
            'faculty_count': len(dept_faculty)
        })
    
    return render_template("superadmin/departments.html",
                          context=context,
                          departments=departments_with_stats)


@superadmin_bp.route("/faculty")
def faculty():
    """View all faculty across all colleges"""
    context = _get_superadmin_context()
    all_faculty = DataHelper.get_faculty_members()
    departments = DataHelper.get_departments()
    
    return render_template("superadmin/faculty.html",
                          context=context,
                          faculty=all_faculty,
                          departments=departments)


@superadmin_bp.route("/users")
def users():
    """Manage all system users"""
    context = _get_superadmin_context()
    all_users = DataHelper.get_all_users_list()
    
    # Group users by role
    users_by_role = {
        'superadmin': [],
        'college_admin': [],
        'hod': [],
        'faculty': [],
        'student': [],
        'parent': []
    }
    
    for user in all_users:
        role_id = user.get('role_id')
        if role_id == 1:
            users_by_role['superadmin'].append(user)
        elif role_id == 2:
            users_by_role['hod'].append(user)
        elif role_id == 3:
            users_by_role['faculty'].append(user)
        elif role_id == 4:
            users_by_role['student'].append(user)
        elif role_id == 5:
            users_by_role['parent'].append(user)
    
    return render_template("superadmin/users.html",
                          context=context,
                          users_by_role=users_by_role,
                          total_users=len(all_users))


@superadmin_bp.route("/analytics")
def analytics():
    """System-wide analytics and reports"""
    context = _get_superadmin_context()
    
    # Get attendance analytics
    attendance_overview = DataHelper.get_system_attendance_overview()
    
    # Department-wise performance
    dept_performance = DataHelper.get_department_performance()

    charts = DataHelper.get_superadmin_charts(dept_performance)
    
    return render_template("superadmin/analytics.html",
                          context=context,
                          attendance_overview=attendance_overview,
                          dept_performance=dept_performance,
                          charts=charts)


@superadmin_bp.route("/profile")
@superadmin_required
def superadmin_profile():
    """Super Admin Profile"""
    context = _get_superadmin_context()
    
    # Get system statistics
    system_stats = {
        'total_colleges': DataHelper.get_total_colleges_count(),
        'total_users': DataHelper.get_total_users_count(),
        'active_admins': DataHelper.get_active_admins_count(),
        'last_login': None  # Placeholder
    }
    
    return render_template("superadmin/profile.html",
                          title="Super Admin Profile",
                          user=context.get('user'),
                          context=context,
                          system_stats=system_stats)


@superadmin_bp.route("/approvals")
def approvals():
    """View pending college approvals"""
    context = _get_superadmin_context()
    
    # Get pending colleges
    pending_colleges = College.query.filter_by(is_approved=False).all()
    
    return render_template("superadmin/approvals.html",
                          title="Pending Approvals",
                          context=context,
                          pending_colleges=pending_colleges)


@superadmin_bp.route("/approve/college/<int:college_id>", methods=['POST'])
def approve_college(college_id):
    """Approve a college"""
    try:
        college = College.query.get(college_id)
        if college:
            college.is_approved = True
            db.session.commit()
            return jsonify({'success': True, 'message': f'College "{college.college_name}" approved successfully'})
        return jsonify({'success': False, 'message': 'College not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@superadmin_bp.route("/reject/college/<int:college_id>", methods=['POST'])
def reject_college(college_id):
    """Reject/Delete a college"""
    try:
        college = College.query.get(college_id)
        if college:
            college_name = college.college_name
            db.session.delete(college)
            db.session.commit()
            return jsonify({'success': True, 'message': f'College "{college_name}" rejected and removed'})
        return jsonify({'success': False, 'message': 'College not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
