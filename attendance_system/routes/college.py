"""
College Admin routes - Dashboard, Departments, Divisions, Faculty, Students, Analytics, Settings
"""
from flask import Blueprint, render_template

college_bp = Blueprint('college', __name__, url_prefix='/college')

def get_mock_data():
    from app import mock_users, mock_college, mock_college_stats
    return mock_users, mock_college, mock_college_stats


@college_bp.route("/dashboard")
def college_dashboard():
    """College Dashboard with departments and divisions overview"""
    mock_users, _, _ = get_mock_data()
    departments = [
        {
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'dept_code': 'CSE',
            'hod_id': 3,
            'hod_name': 'Prof. Amit Patel',
            'divisions_count': 3,
            'faculty_count': 12,
            'student_count': 150,
            'description': 'Department of Computer Science'
        },
        {
            'dept_id': 2,
            'dept_name': 'Electronics Engineering',
            'dept_code': 'ECE',
            'hod_id': 4,
            'hod_name': 'Prof. Rajesh Kumar',
            'divisions_count': 2,
            'faculty_count': 10,
            'student_count': 120,
            'description': 'Department of Electronics'
        },
        {
            'dept_id': 3,
            'dept_name': 'Mechanical Engineering',
            'dept_code': 'ME',
            'hod_id': 5,
            'hod_name': 'Prof. Vijay Singh',
            'divisions_count': 2,
            'faculty_count': 8,
            'student_count': 100,
            'description': 'Department of Mechanical Engineering'
        }
    ]

    divisions = [
        {'div_id': 1, 'division_name': 'A', 'division_code': 'CSE-A', 'capacity': 60, 'student_count': 55, 'class_teacher': 'Prof. Dr. Sharma'},
        {'div_id': 2, 'division_name': 'B', 'division_code': 'CSE-B', 'capacity': 60, 'student_count': 58, 'class_teacher': 'Dr. Anjali Kumar'},
    ]

    faculty_count = 30
    student_count = 370

    return render_template("college/dashboard.html",
                         title="College Dashboard",
                         user=mock_users['college_admin'],
                         departments=departments,
                         divisions=divisions,
                         faculty_count=faculty_count,
                         student_count=student_count)


@college_bp.route("/profile")
def college_profile():
    """College Profile"""
    _, mock_college, mock_college_stats = get_mock_data()
    mock_users, _, _ = get_mock_data()
    return render_template("college/profile.html",
                         title="College Profile",
                         user=mock_users['college_admin'],
                         college=mock_college,
                         college_stats=mock_college_stats)


@college_bp.route("/departments")
def college_departments():
    """College Departments List"""
    departments = [
        {
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'dept_code': 'CSE',
            'hod_id': 3,
            'hod_name': 'Prof. Amit Patel',
            'divisions_count': 3,
            'faculty_count': 12,
            'student_count': 150,
            'description': 'Department of Computer Science & Engineering'
        },
        {
            'dept_id': 2,
            'dept_name': 'Electronics Engineering',
            'dept_code': 'ECE',
            'hod_id': 4,
            'hod_name': 'Prof. Rajesh Kumar',
            'divisions_count': 2,
            'faculty_count': 10,
            'student_count': 120,
            'description': 'Department of Electronics Engineering'
        },
        {
            'dept_id': 3,
            'dept_name': 'Mechanical Engineering',
            'dept_code': 'ME',
            'hod_id': 5,
            'hod_name': 'Prof. Vijay Singh',
            'divisions_count': 2,
            'faculty_count': 8,
            'student_count': 100,
            'description': 'Department of Mechanical Engineering'
        }
    ]

    faculty = [
        {'faculty_id': 3, 'name': 'Prof. Amit Patel'},
        {'faculty_id': 4, 'name': 'Prof. Rajesh Kumar'},
        {'faculty_id': 5, 'name': 'Prof. Vijay Singh'},
    ]

    return render_template("college/departments.html",
                         title="Departments",
                         departments=departments,
                         all_faculty=faculty)


@college_bp.route("/divisions")
def college_divisions():
    """College Divisions List"""
    departments = [
        {
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'dept_code': 'CSE',
            'divisions': [
                {'div_id': 1, 'division_name': 'A', 'division_code': 'CSE-A', 'capacity': 60, 'student_count': 55, 'class_teacher': 'Prof. Dr. Sharma'},
                {'div_id': 2, 'division_name': 'B', 'division_code': 'CSE-B', 'capacity': 60, 'student_count': 58, 'class_teacher': 'Dr. Anjali Kumar'},
                {'div_id': 3, 'division_name': 'C', 'division_code': 'CSE-C', 'capacity': 60, 'student_count': 37, 'class_teacher': 'Dr. Priya Sharma'},
            ]
        },
        {
            'dept_id': 2,
            'dept_name': 'Electronics Engineering',
            'divisions': [
                {'div_id': 4, 'division_name': 'A', 'division_code': 'ECE-A', 'capacity': 60, 'student_count': 60, 'class_teacher': 'Prof. Rajesh Kumar'},
                {'div_id': 5, 'division_name': 'B', 'division_code': 'ECE-B', 'capacity': 60, 'student_count': 60, 'class_teacher': 'Dr. Deepak Singh'},
            ]
        },
        {
            'dept_id': 3,
            'dept_name': 'Mechanical Engineering',
            'divisions': [
                {'div_id': 6, 'division_name': 'A', 'division_code': 'ME-A', 'capacity': 50, 'student_count': 50, 'class_teacher': 'Prof. Vijay Singh'},
                {'div_id': 7, 'division_name': 'B', 'division_code': 'ME-B', 'capacity': 50, 'student_count': 50, 'class_teacher': 'Dr. Rohit Patel'},
            ]
        }
    ]

    faculty = [
        {'faculty_id': 1, 'name': 'Prof. Dr. Sharma'},
        {'faculty_id': 2, 'name': 'Dr. Anjali Kumar'},
        {'faculty_id': 3, 'name': 'Dr. Priya Sharma'},
    ]

    return render_template("college/divisions.html",
                         title="Divisions",
                         departments=departments,
                         all_faculty=faculty)


@college_bp.route("/divisions/create")
def college_divisions_create():
    """Create New Division"""
    departments = [
        {'dept_id': 1, 'dept_name': 'Computer Science & Engineering'},
        {'dept_id': 2, 'dept_name': 'Electronics Engineering'},
        {'dept_id': 3, 'dept_name': 'Mechanical Engineering'}
    ]
    faculty = [
        {'faculty_id': 1, 'name': 'Prof. Dr. Sharma'},
        {'faculty_id': 2, 'name': 'Dr. Anjali Kumar'},
    ]
    return render_template("college/divisions.html",
                         title="Create Division",
                         departments=departments,
                         all_faculty=faculty)


@college_bp.route("/faculty")
def college_faculty():
    """College Faculty List"""
    departments = [
        {'dept_id': 1, 'dept_name': 'Computer Science & Engineering'},
        {'dept_id': 2, 'dept_name': 'Electronics Engineering'},
        {'dept_id': 3, 'dept_name': 'Mechanical Engineering'}
    ]

    faculty_list = [
        {
            'faculty_id': 1,
            'name': 'Dr. Priya Sharma',
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'email': 'priya.sharma@college.edu',
            'phone': '9876543210',
            'specialization': 'Web Development',
            'subjects': ['Web Tech', 'Database Management'],
            'is_hod': False
        },
        {
            'faculty_id': 2,
            'name': 'Prof. Amit Patel',
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'email': 'amit.patel@college.edu',
            'phone': '9876543211',
            'specialization': 'Artificial Intelligence',
            'subjects': ['Machine Learning', 'AI'],
            'is_hod': True,
            'appointed_date': '2020-06-15'
        },
        {
            'faculty_id': 3,
            'name': 'Dr. Rajesh Kumar',
            'dept_id': 2,
            'dept_name': 'Electronics Engineering',
            'email': 'rajesh.kumar@college.edu',
            'phone': '9876543212',
            'specialization': 'Embedded Systems',
            'subjects': ['Microcontrollers', 'IoT'],
            'is_hod': True,
            'appointed_date': '2019-03-20'
        },
    ]

    return render_template("college/faculty.html",
                         title="Faculty Management",
                         departments=departments,
                         faculty_list=faculty_list)


@college_bp.route("/faculty/hod-list")
def college_faculty_hod_list():
    """HOD (Head of Department) List"""
    hod_data = [
        {
            'hod_id': 1,
            'name': 'Prof. Amit Patel',
            'email': 'amit.patel@college.edu',
            'phone': '9876543210',
            'dept_name': 'Computer Science & Engineering',
            'dept_id': 1,
            'qualification': 'Ph.D. in Computer Science',
            'experience': '15 years',
            'specialization': 'AI & Machine Learning'
        },
        {
            'hod_id': 2,
            'name': 'Prof. Rajesh Kumar',
            'email': 'rajesh.kumar@college.edu',
            'phone': '9876543211',
            'dept_name': 'Electronics Engineering',
            'dept_id': 2,
            'qualification': 'Ph.D. in Electronics',
            'experience': '12 years',
            'specialization': 'VLSI Design'
        },
        {
            'hod_id': 3,
            'name': 'Prof. Vijay Singh',
            'email': 'vijay.singh@college.edu',
            'phone': '9876543212',
            'dept_name': 'Mechanical Engineering',
            'dept_id': 3,
            'qualification': 'Ph.D. in Mechanical Engineering',
            'experience': '18 years',
            'specialization': 'Manufacturing & Production'
        }
    ]
    return render_template("college/faculty.html",
                         title="HOD Information",
                         hod_data=hod_data)


@college_bp.route("/students")
def college_students():
    """College Students List"""
    departments = [
        {
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'student_count': 150,
            'divisions': [
                {'div_id': 1, 'division_name': 'A', 'student_count': 55},
                {'div_id': 2, 'division_name': 'B', 'student_count': 58},
                {'div_id': 3, 'division_name': 'C', 'student_count': 37},
            ]
        },
        {
            'dept_id': 2,
            'dept_name': 'Electronics Engineering',
            'student_count': 120,
            'divisions': [
                {'div_id': 4, 'division_name': 'A', 'student_count': 60},
                {'div_id': 5, 'division_name': 'B', 'student_count': 60},
            ]
        },
        {
            'dept_id': 3,
            'dept_name': 'Mechanical Engineering',
            'student_count': 100,
            'divisions': [
                {'div_id': 6, 'division_name': 'A', 'student_count': 50},
                {'div_id': 7, 'division_name': 'B', 'student_count': 50},
            ]
        }
    ]

    students = [
        {
            'student_id': 1,
            'roll_number': 'CSE001',
            'name': 'Raj Kumar',
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'div_id': 1,
            'division_name': 'A',
            'email': 'raj.kumar@college.edu',
            'phone': '9876543210'
        },
        {
            'student_id': 2,
            'roll_number': 'CSE002',
            'name': 'Priya Singh',
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'div_id': 1,
            'division_name': 'A',
            'email': 'priya.singh@college.edu',
            'phone': '9876543211'
        },
        {
            'student_id': 3,
            'roll_number': 'ECE001',
            'name': 'Amit Verma',
            'dept_id': 2,
            'dept_name': 'Electronics Engineering',
            'div_id': 4,
            'division_name': 'A',
            'email': 'amit.verma@college.edu',
            'phone': '9876543212'
        },
    ]

    student_count = sum(dept['student_count'] for dept in departments)

    return render_template("college/students.html",
                         title="Student Management",
                         departments=departments,
                         students=students,
                         student_count=student_count)


@college_bp.route("/students/by-division")
def college_students_by_division():
    """College Students by Division"""
    departments = [
        {
            'dept_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'student_count': 150,
            'divisions': [
                {'div_id': 1, 'division_name': 'A', 'division_code': 'CSE-A', 'capacity': 60, 'student_count': 55},
                {'div_id': 2, 'division_name': 'B', 'division_code': 'CSE-B', 'capacity': 60, 'student_count': 58},
                {'div_id': 3, 'division_name': 'C', 'division_code': 'CSE-C', 'capacity': 60, 'student_count': 37},
            ]
        },
        {
            'dept_id': 2,
            'dept_name': 'Electronics Engineering',
            'student_count': 120,
            'divisions': [
                {'div_id': 4, 'division_name': 'A', 'division_code': 'ECE-A', 'capacity': 60, 'student_count': 60},
                {'div_id': 5, 'division_name': 'B', 'division_code': 'ECE-B', 'capacity': 60, 'student_count': 60},
            ]
        },
        {
            'dept_id': 3,
            'dept_name': 'Mechanical Engineering',
            'student_count': 100,
            'divisions': [
                {'div_id': 6, 'division_name': 'A', 'division_code': 'ME-A', 'capacity': 50, 'student_count': 50},
                {'div_id': 7, 'division_name': 'B', 'division_code': 'ME-B', 'capacity': 50, 'student_count': 50},
            ]
        }
    ]

    students = [
        {'student_id': 1, 'roll_number': 'CSE001', 'name': 'Raj Kumar', 'div_id': 1, 'division_name': 'A', 'dept_id': 1, 'dept_name': 'Computer Science & Engineering', 'email': 'raj.kumar@college.edu', 'phone': '9876543210'},
        {'student_id': 2, 'roll_number': 'CSE002', 'name': 'Priya Singh', 'div_id': 1, 'division_name': 'A', 'dept_id': 1, 'dept_name': 'Computer Science & Engineering', 'email': 'priya.singh@college.edu', 'phone': '9876543211'},
        {'student_id': 3, 'roll_number': 'CSE003', 'name': 'Amit Patel', 'div_id': 2, 'division_name': 'B', 'dept_id': 1, 'dept_name': 'Computer Science & Engineering', 'email': 'amit.patel@college.edu', 'phone': '9876543212'},
        {'student_id': 4, 'roll_number': 'ECE001', 'name': 'Neha Sharma', 'div_id': 4, 'division_name': 'A', 'dept_id': 2, 'dept_name': 'Electronics Engineering', 'email': 'neha.sharma@college.edu', 'phone': '9876543213'},
        {'student_id': 5, 'roll_number': 'ECE002', 'name': 'Deepak Singh', 'div_id': 4, 'division_name': 'A', 'dept_id': 2, 'dept_name': 'Electronics Engineering', 'email': 'deepak.singh@college.edu', 'phone': '9876543214'},
        {'student_id': 6, 'roll_number': 'ME001', 'name': 'Vikram Kumar', 'div_id': 6, 'division_name': 'A', 'dept_id': 3, 'dept_name': 'Mechanical Engineering', 'email': 'vikram.kumar@college.edu', 'phone': '9876543215'},
    ]

    student_count = sum(dept['student_count'] for dept in departments)

    return render_template("college/students.html",
                         title="Students By Division",
                         departments=departments,
                         students=students,
                         student_count=student_count)


@college_bp.route("/attendance-analytics")
def college_attendance_analytics():
    """College Attendance Analytics"""
    departments = [
        {'dept_id': 1, 'dept_name': 'Computer Science & Engineering'},
        {'dept_id': 2, 'dept_name': 'Electronics Engineering'},
        {'dept_id': 3, 'dept_name': 'Mechanical Engineering'}
    ]

    for dept in departments:
        dept['divisions'] = [
            {'div_id': i, 'division_name': chr(65 + i)} for i in range(2)
        ]

    stats = {
        'present_count': 280,
        'absent_count': 50,
        'late_count': 40,
        'present_percentage': 75,
        'absent_percentage': 13,
        'late_percentage': 12,
        'total_days': 22
    }

    attendance_records = [
        {
            'date': '2024-01-15',
            'dept_name': 'Computer Science & Engineering',
            'div_name': 'A',
            'present': 55,
            'absent': 3,
            'late': 2,
            'total': 60,
            'present_percentage': 91
        },
        {
            'date': '2024-01-14',
            'dept_name': 'Computer Science & Engineering',
            'div_name': 'B',
            'present': 56,
            'absent': 2,
            'late': 2,
            'total': 60,
            'present_percentage': 93
        },
    ]

    # Mock chart data
    dept_labels = ['CSE', 'ECE', 'ME']
    dept_present = [88, 85, 80]
    div_labels = ['A', 'B', 'C']
    div_present = [88, 85, 75]
    trend_dates = ['Jan 1', 'Jan 5', 'Jan 10', 'Jan 15']
    trend_values = [78, 82, 79, 85]

    return render_template("college/attendance-analytics.html",
                         title="Attendance Analytics",
                         departments=departments,
                         stats=stats,
                         attendance_records=attendance_records,
                         dept_labels=dept_labels,
                         dept_present=dept_present,
                         div_labels=div_labels,
                         div_present=div_present,
                         trend_dates=trend_dates,
                         trend_values=trend_values)


@college_bp.route("/settings")
def college_settings():
    """College Settings"""
    _, mock_college, _ = get_mock_data()
    mock_users, _, _ = get_mock_data()
    return render_template("college/settings.html",
                         title="College Settings",
                         college=mock_college,
                         user=mock_users['college_admin'])
