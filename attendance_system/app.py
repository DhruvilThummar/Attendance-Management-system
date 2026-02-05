"""
Attendance Management System - Main Flask Application

This is the main application entry point that initializes Flask,
loads configuration, and registers all blueprints (routes).

The application is organized into modular route blueprints:
- routes/main.py: Home, About, Contact pages
- routes/auth.py: Login, Register
- routes/superadmin.py: Super Admin dashboard and profile
- routes/college.py: College admin routes
- routes/hod.py: Head of Department routes
- routes/faculty.py: Faculty routes
- routes/student.py: Student routes
- routes/parent.py: Parent routes
"""

from flask import Flask
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

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
    'division_name': 'A',
    'division_code': 'CSE-A'
}

# Mock Semester Data
mock_semester = {
    'semester_id': 1,
    'semester': 3,
    'year': 1,
    'division_id': 1
}

# Mock Teaching Statistics
mock_teaching_stats = {
    'total_lectures': 120,
    'completed_lectures': 95,
    'pending_lectures': 25,
    'avg_attendance': 82.5
}

# Mock Department Statistics
mock_dept_stats = {
    'total_students': 150,
    'total_faculty': 12,
    'total_divisions': 3,
    'avg_attendance': 81.25
}

# Mock Attendance Statistics
mock_attendance_stats = {
    'total_lectures': 45,
    'present': 42,
    'absent': 3,
    'attendance_percentage': 93.3
}

# Mock College Statistics
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


# ==================== REGISTER BLUEPRINTS ====================

def register_blueprints():
    """Register all route blueprints with the Flask application"""
    from routes import register_blueprints as register_all
    register_all(app)


# Register blueprints
register_blueprints()


if __name__ == "__main__":
    app.run(debug=True)
