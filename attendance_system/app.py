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
def cdashboard():    
    return render_template("college/cbase.html", title="College Dashboard")

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
    return render_template("faculty/fbase.html", title="Faculty Dashboard")

@app.route("/faculty/profile")
def faculty_profile():    
    return render_template("faculty/profile.html", 
                         title="Faculty Profile",
                         user=mock_users['faculty'],
                         faculty=mock_faculty,
                         college=mock_college,
                         department=mock_department,
                         teaching_stats=mock_teaching_stats)


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


if __name__ == "__main__":
    app.run(debug=True)