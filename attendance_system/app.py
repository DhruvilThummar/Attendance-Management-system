"""
Attendance Management System - Main Flask Application

This is the main application entry point that initializes Flask,
loads configuration, database, and registers all blueprints (routes).

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
import os

from models.user import db


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+mysqlconnector://root:password@localhost:3306/attendance_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

# Initialize SQLAlchemy
db.init_app(app)

# Create all database tables if they don't exist
with app.app_context():
    try:
        db.create_all()
        print("✓ Database tables created/verified successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        print("  Make sure MySQL is running and DATABASE_URL is correct in .env")

# ==================== MOCK DATA (FOR DEVELOPMENT) ====================
# These mock data structures match the database models
# Once database is ready, replace these with actual database queries

def get_mock_data():
    """Get all mock data - structure follows database models"""
    
    # Roles
    mock_roles = {
        'ADMIN': 1,
        'HOD': 2,
        'FACULTY': 3,
        'STUDENT': 4,
        'PARENT': 5
    }
    
    # College
    mock_college = {
        'college_id': 1,
        'college_name': 'ABC Engineering College',
        'created_at': datetime(2020, 1, 1)
    }
    
    # Departments
    mock_departments = [
        {
            'dept_id': 1,
            'college_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'hod_faculty_id': 2
        },
        {
            'dept_id': 2,
            'college_id': 1,
            'dept_name': 'Electronics & Communication',
            'hod_faculty_id': None
        },
        {
            'dept_id': 3,
            'college_id': 1,
            'dept_name': 'Mechanical Engineering',
            'hod_faculty_id': None
        }
    ]
    
    # Divisions
    mock_divisions = [
        {'division_id': 1, 'dept_id': 1, 'division_name': 'A'},
        {'division_id': 2, 'dept_id': 1, 'division_name': 'B'},
        {'division_id': 3, 'dept_id': 1, 'division_name': 'C'},
        {'division_id': 4, 'dept_id': 2, 'division_name': 'A'},
        {'division_id': 5, 'dept_id': 2, 'division_name': 'B'},
        {'division_id': 6, 'dept_id': 3, 'division_name': 'A'},
        {'division_id': 7, 'dept_id': 3, 'division_name': 'B'},
    ]
    
    # Semesters
    mock_semesters = [
        {'semester_id': 1, 'semester_no': 1, 'academic_year': '2024-2025'},
        {'semester_id': 2, 'semester_no': 2, 'academic_year': '2024-2025'},
        {'semester_id': 3, 'semester_no': 3, 'academic_year': '2024-2025'},
        {'semester_id': 4, 'semester_no': 4, 'academic_year': '2024-2025'},
    ]
    
    # Users
    mock_users = {
        'superadmin': {
            'user_id': 1,
            'college_id': 1,
            'name': 'Super Admin',
            'email': 'admin@attendance.system',
            'mobile': '9999999999',
            'role_id': 1,
            'is_approved': True,
            'created_at': datetime(2020, 1, 1)
        },
        'college_admin': {
            'user_id': 2,
            'college_id': 1,
            'name': 'Ms. Neha Singh',
            'email': 'neha.singh@college.edu',
            'mobile': '9876543213',
            'role_id': 1,
            'is_approved': True,
            'created_at': datetime(2021, 1, 20)
        },
        'hod': {
            'user_id': 3,
            'college_id': 1,
            'name': 'Prof. Amit Patel',
            'email': 'amit.patel@college.edu',
            'mobile': '9876543212',
            'role_id': 2,
            'is_approved': True,
            'created_at': datetime(2020, 3, 5)
        },
        'faculty': {
            'user_id': 4,
            'college_id': 1,
            'name': 'Dr. Priya Sharma',
            'email': 'priya.sharma@college.edu',
            'mobile': '9876543211',
            'role_id': 3,
            'is_approved': True,
            'created_at': datetime(2022, 6, 10)
        },
        'student': {
            'user_id': 5,
            'college_id': 1,
            'name': 'Raj Kumar',
            'email': 'raj.kumar@college.edu',
            'mobile': '9876543210',
            'role_id': 4,
            'is_approved': True,
            'created_at': datetime(2023, 8, 15)
        },
        'parent': {
            'user_id': 6,
            'college_id': 1,
            'name': 'Shyam Kumar',
            'email': 'shyam.kumar@email.com',
            'mobile': '9876543214',
            'role_id': 5,
            'is_approved': True,
            'created_at': datetime(2023, 9, 1)
        }
    }
    
    # Faculty Members
    mock_faculty = [
        {
            'faculty_id': 1,
            'user_id': 3,  # Prof. Amit (HOD)
            'dept_id': 1,
            'short_name': 'AP'
        },
        {
            'faculty_id': 2,
            'user_id': 4,  # Dr. Priya
            'dept_id': 1,
            'short_name': 'PS'
        }
    ]
    
    # Students
    mock_students = [
        {
            'student_id': 1,
            'user_id': 5,  # Raj Kumar
            'dept_id': 1,
            'division_id': 1,
            'enrollment_no': 'EN2023001',
            'roll_no': 101,
            'mentor_id': 2,
            'semester_id': 3
        }
    ]
    
    # Parents
    mock_parents = [
        {
            'user_id': 6,  # Shyam Kumar
            'student_id': 1
        }
    ]
    
    # Subjects
    mock_subjects = [
        {
            'subject_id': 1,
            'dept_id': 1,
            'subject_name': 'Data Structures',
            'subject_code': 'CS301',
            'semester_id': 3
        },
        {
            'subject_id': 2,
            'dept_id': 1,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'semester_id': 3
        }
    ]
    
    return {
        'roles': mock_roles,
        'college': mock_college,
        'departments': mock_departments,
        'divisions': mock_divisions,
        'semesters': mock_semesters,
        'users': mock_users,
        'faculty': mock_faculty,
        'students': mock_students,
        'parents': mock_parents,
        'subjects': mock_subjects,
    }


# Statistics based on mock data
def get_mock_statistics():
    """Get system statistics"""
    return {
        'faculty_stats': {
            'total_lectures': 120,
            'completed_lectures': 95,
            'pending_lectures': 25,
            'avg_attendance': 82.5
        },
        'department_stats': {
            'total_students': 150,
            'total_faculty': 12,
            'total_divisions': 3,
            'avg_attendance': 81.25
        },
        'college_stats': {
            'total_departments': 3,
            'total_faculty': 25,
            'total_students': 500,
            'total_users': 600,
            'avg_attendance': 81.25
        },
        'system_stats': {
            'total_colleges': 1,
            'total_departments': 3,
            'total_users': 600,
            'total_students': 500,
            'total_faculty': 25,
            'pending_approvals': 5,
            'active_sessions': 12
        }
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
