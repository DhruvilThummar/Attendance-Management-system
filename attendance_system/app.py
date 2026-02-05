from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
app = Flask(__name__)

# ==================== MOCK DATA ====================

# Mock User Data
mock_users = {
    'student': {
        'user_id': 1,
        'name': 'Raj Kumar',
        'email': 'raj.kumar@college.edu',
        'mobile': '9876543210',
        'is_approved': True,
        'created_at': datetime(2023, 8, 15),
        'avatar': None
    },
    'faculty': {
        'user_id': 2,
        'name': 'Dr. Priya Sharma',
        'email': 'priya.sharma@college.edu',
        'mobile': '9876543211',
        'is_approved': True,
        'created_at': datetime(2022, 6, 10),
        'avatar': None
    },
    'hod': {
        'user_id': 3,
        'name': 'Prof. Amit Patel',
        'email': 'amit.patel@college.edu',
        'mobile': '9876543212',
        'is_approved': True,
        'created_at': datetime(2020, 3, 5),
        'avatar': None
    },
    'college_admin': {
        'user_id': 4,
        'name': 'Ms. Neha Singh',
        'email': 'neha.singh@college.edu',
        'mobile': '9876543213',
        'is_approved': True,
        'created_at': datetime(2021, 1, 20),
        'avatar': None
    },
    'parent': {
        'user_id': 5,
        'name': 'Shyam Kumar',
        'email': 'shyam.kumar@email.com',
        'mobile': '9876543214',
        'is_approved': True,
        'created_at': datetime(2023, 9, 1),
        'avatar': None
    },
    'superadmin': {
        'user_id': 6,
        'name': 'Admin User',
        'email': 'admin@attendance.system',
        'mobile': '9999999999',
        'is_approved': True,
        'created_at': datetime(2020, 1, 1),
        'avatar': None
    }
}

# Mock Student Data
mock_student = {
    'student_id': 1,
    'user_id': 1,
    'enrollment_no': 'EN2023001',
    'roll_no': 101,
    'short_name': 'RK'
}

# Mock Faculty Data
mock_faculty = {
    'faculty_id': 1,
    'user_id': 2,
    'short_name': 'PS'
}

# Mock College Data
mock_college = {
    'college_id': 1,
    'college_name': 'ABC Engineering College'
}

# Mock Department Data
mock_department = {
    'dept_id': 1,
    'college_id': 1,
    'dept_name': 'Computer Science & Engineering'
}

# Mock Division Data
mock_division = {
    'division_id': 1,
    'dept_id': 1,
    'division_name': 'A'
}

# Mock Semester Data
mock_semester = {
    'semester_id': 1,
    'semester_no': 3,
    'academic_year': '2023-24'
}

# Mock Attendance Stats for Student/Parent
mock_attendance_stats = {
    'total_lectures': 45,
    'present': 38,
    'absent': 7,
    'percentage': 84.44
}

# Mock Teaching Stats for Faculty
mock_teaching_stats = {
    'lectures_conducted': 120,
    'total_subjects': 4,
    'proxy_taken': 2,
    'mentoring_count': 15
}

# Mock Department Stats for HOD
mock_dept_stats = {
    'total_students': 150,
    'total_faculty': 12,
    'total_divisions': 3,
    'total_subjects': 24,
    'avg_attendance': 82.5
}

# Mock College Stats for College Admin
mock_college_stats = {
    'total_departments': 5,
    'total_faculty': 60,
    'total_students': 750,
    'total_users': 850,
    'avg_attendance': 81.25
}

# Mock System Stats for Super Admin
mock_system_stats = {
    'total_colleges': 5,
    'total_departments': 25,
    'total_users': 4250,
    'total_students': 3750,
    'total_faculty': 300,
    'pending_approvals': 12,
    'active_sessions': 45
}
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/profiles")
@app.route("/profile-test")
def profile_test():
    return render_template("profile_test.html")

@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login")
def login():    
    return render_template("login.html")

@app.route("/register")
def register():    
    return render_template("register.html")


# ========== super admin routes -============
@app.route("/superadmindashboard")
def dashboard():    
    return render_template("superadmin/subase.html", title="Super Admin Dashboard")

@app.route("/superadmin/profile")
def superadmin_profile():    
    return render_template("superadmin/profile.html", 
                         title="Super Admin Profile",
                         user=mock_users['superadmin'],
                         system_stats=mock_system_stats)


# ========== college routes -============
@app.route("/collegedashboard")
def college_dashboard():
    # Mock data for dashboard
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

@app.route("/college/profile")
def college_profile():    
    return render_template("college/profile.html", 
                         title="College Profile",
                         user=mock_users['college_admin'],
                         college=mock_college,
                         college_stats=mock_college_stats)

# ========== hod routes -============
@app.route("/hoddashboard")
def hdashboard():    
    return render_template("hod/hbase.html", title="HOD Dashboard") 

@app.route("/hod/profile")
def hod_profile():    
    return render_template("hod/profile.html", 
                         title="HOD Profile",
                         user=mock_users['hod'],
                         faculty=mock_faculty,
                         college=mock_college,
                         department=mock_department,
                         dept_stats=mock_dept_stats)


# ========== faculty routes -============
@app.route("/facultydashboard")
def fdashboard():
    # Today's Timetable Mock Data
    today = datetime.now().strftime('%A').upper()[:3] # MON, TUE, etc.
    timetable = [
        {
            'timetable_id': 1,
            'subject_name': 'Web Technologies',
            'subject_code': 'CS301',
            'division_name': 'CSE-A',
            'start_time': '09:00 AM',
            'end_time': '10:00 AM',
            'room_no': '401',
            'is_completed': True
        },
        {
            'timetable_id': 2,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'division_name': 'CSE-B',
            'start_time': '10:00 AM',
            'end_time': '11:00 AM',
            'room_no': '402',
            'is_completed': False
        },
        {
            'timetable_id': 3,
            'subject_name': 'Operating Systems',
            'subject_code': 'CS303',
            'division_name': 'CSE-A',
            'start_time': '11:15 AM',
            'end_time': '12:15 PM',
            'room_no': '401',
            'is_completed': False
        }
    ]

    # Proxy Lectures Mock Data
    proxies = [
        {
            'proxy_id': 1,
            'subject_name': 'Data Structures',
            'division_name': 'ECE-A',
            'lecture_date': datetime.now().strftime('%Y-%m-%d'),
            'lecture_no': 4,
            'original_faculty': 'Dr. Rajesh Kumar',
            'status': 'PENDING'
        }
    ]

    stats = {
        'total_lectures': 4,
        'completed': 1,
        'remaining': 3,
        'proxy_pending': 1
    }

    return render_template("faculty/dashboard.html", 
                         title="Faculty Dashboard",
                         user=mock_users['faculty'],
                         faculty=mock_faculty,
                         department=mock_department,
                         teaching_stats=mock_teaching_stats,
                         timetable=timetable,
                         proxies=proxies,
                         stats=stats,
                         datetime=datetime)

@app.route("/faculty/attendance")
def faculty_attendance():
    # For now, show a selection of divisions/subjects
    divisions = [
        {'div_id': 1, 'division_name': 'CSE-A', 'subjects': [{'id': 1, 'name': 'Web Technologies'}, {'id': 2, 'name': 'Operating Systems'}]},
        {'div_id': 2, 'division_name': 'CSE-B', 'subjects': [{'id': 3, 'name': 'Database Management'}]}
    ]
    return render_template("faculty/attendance.html", 
                         title="Attendance Management",
                         user=mock_users['faculty'],
                         divisions=divisions,
                         datetime=datetime)

@app.route("/faculty/analytics")
def faculty_analytics():
    # Mock analytics data
    class_wise_attendance = [
        {'division': 'CSE-A', 'percentage': 85},
        {'division': 'CSE-B', 'percentage': 78},
        {'division': 'ECE-A', 'percentage': 92},
    ]
    day_wise_attendance = [
        {'day': 'Monday', 'percentage': 88},
        {'day': 'Tuesday', 'percentage': 82},
        {'day': 'Wednesday', 'percentage': 85},
        {'day': 'Thursday', 'percentage': 80},
        {'day': 'Friday', 'percentage': 84},
        {'day': 'Saturday', 'percentage': 75},
    ]
    return render_template("faculty/analytics.html", 
                         title="Attendance Analytics",
                         user=mock_users['faculty'],
                         class_stats=class_wise_attendance,
                         day_stats=day_wise_attendance)

@app.route("/faculty/reports")
def faculty_reports():
    # Mock individual student report data
    students = [
        {'id': 1, 'roll_no': '101', 'name': 'Raj Kumar', 'attendance': 92},
        {'id': 2, 'roll_no': '102', 'name': 'Priya Singh', 'attendance': 88},
        {'id': 3, 'roll_no': '103', 'name': 'Amit Verma', 'attendance': 75},
    ]
    return render_template("faculty/reports.html", 
                         title="Attendance Reports",
                         user=mock_users['faculty'],
                         students=students,
                         datetime=datetime)

@app.route("/faculty/timetable")
def faculty_timetable():
    return render_template("faculty/timetable.html", 
                         title="Weekly Timetable",
                         user=mock_users['faculty'])

@app.route("/faculty/profile")
def faculty_profile():    
    return render_template("faculty/profile.html", 
                         title="Faculty Profile",
                         user=mock_users['faculty'],
                         faculty=mock_faculty,
                         college=mock_college,
                         department=mock_department,
                         teaching_stats=mock_teaching_stats,
                         datetime=datetime)


# ========== student routes -============
@app.route("/studentdashboard")
def sdashboard():    
    return render_template("student/sbase.html", title="Student Dashboard")

@app.route("/student/profile")
def student_profile():
    return render_template("student/profile.html", 
                         title="Student Profile",
                         user=mock_users['student'],
                         student=mock_student,
                         college=mock_college,
                         department=mock_department,
                         division=mock_division,
                         semester=mock_semester,
                         attendance_stats=mock_attendance_stats)



# ========== parent routes -============
@app.route("/parentdashboard")
def pdashboard():    
    return render_template("parent/pbase.html", title="Parent Dashboard")

@app.route("/parent/profile")
def parent_profile():
    return render_template("parent/profile.html", 
                         title="Parent Profile",
                         user=mock_users['parent'],
                         student=mock_users['student'],
                         college=mock_college,
                         department=mock_department,
                         division=mock_division,
                         semester=mock_semester,
                         attendance_stats=mock_attendance_stats)


# ========== college admin routes -============
@app.route("/college/departments")
def college_departments():
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

@app.route("/college/divisions")
def college_divisions():
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

@app.route("/college/faculty")
def college_faculty():
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

@app.route("/college/students")
def college_students():
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

@app.route("/college/attendance-analytics")
def college_attendance_analytics():
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


# ========== Missing college admin routes -============
@app.route("/college/divisions/create")
def college_divisions_create():
    """Route for creating a new division"""
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

@app.route("/college/students/by-division")
def college_students_by_division():
    """Route for viewing students by division"""
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

@app.route("/college/faculty/hod-list")
def college_faculty_hod_list():
    """Route for viewing HOD information"""
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

@app.route("/college/settings")
def college_settings():
    """Route for college settings"""
    return render_template("college/settings.html",
                         title="College Settings",
                         college=mock_college,
                         user=mock_users['college_admin'])


if __name__ == "__main__":
    app.run(debug=True)