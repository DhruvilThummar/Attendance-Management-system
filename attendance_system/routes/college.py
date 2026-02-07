"""
College Admin routes - Dashboard, Departments, Divisions, Faculty, Students, Analytics, Settings
"""
from flask import Blueprint, render_template
from services.data_helper import DataHelper
from services.chart_helper import (
    generate_department_comparison_chart,
    generate_class_strength_chart,
    generate_attendance_monthly_chart
)

college_bp = Blueprint('college', __name__, url_prefix='/college')


@college_bp.route("/dashboard")
def college_dashboard():
    """College Dashboard with departments and divisions overview"""
    college = DataHelper.get_college()
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    
    # Generate charts
    charts = {}
    
    # Department comparison chart
    dept_data = {}
    for dept in departments if departments else []:
        dept_name = dept.get('dept_name', 'Unknown')
        student_count = 45  # Sample data
        dept_data[dept_name] = student_count
    
    if dept_data:
        charts['department_comparison'] = generate_department_comparison_chart(dept_data)
    
    # Class strength chart
    class_data = {}
    for div in divisions if divisions else []:
        div_name = div.get('division_name', 'Unknown')
        student_count = 60
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
                         charts=charts)


@college_bp.route("/profile")
def college_profile():
    """College Profile"""
    college = DataHelper.get_college()
    return render_template("college/profile.html",
                         title="College Profile",
                         college=college)


@college_bp.route("/departments")
def college_departments():
    """College Departments List"""
    departments = DataHelper.get_departments()
    return render_template("college/departments.html",
        {'faculty_id': 5, 'name': 'Prof. Vijay Singh'},
                            title="Departments",
                            departments=departments)                

    return render_template("college/departments.html",  
                         title="Departments",
                         departments=departments,
                         all_faculty=faculty)


@college_bp.route("/divisions")
def college_divisions():
    """College Divisions List"""
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    
    return render_template("college/divisions.html",
                         title="Divisions",
                         departments=departments,
                         divisions=divisions)


@college_bp.route("/divisions/create")
def college_divisions_create():
    """Create New Division"""
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


@college_bp.route("/students")
def college_students():
    """College Students List"""
    departments = DataHelper.get_departments()
    divisions = DataHelper.get_divisions()
    students = DataHelper.get_students()
    
    return render_template("college/students.html",
                         title="Student Management",
                         departments=departments,
                         divisions=divisions,
                         students=students)


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
