"""
Mock Data Service

This module provides mock data for development/testing.
When transitioning to a real database, replace these functions with actual database queries.
"""

from datetime import datetime
from models import User, Role, College, Department, Division, Faculty, Student, Parent, Subject, Semester


class MockDataService:
    """Service to provide mock data matching the database models"""
    
    @staticmethod
    def get_college():
        """Get mock college data"""
        return {
            'college_id': 1,
            'college_name': 'ABC Engineering College',
            'created_at': datetime(2020, 1, 1)
        }
    
    @staticmethod
    def get_departments():
        """Get mock departments"""
        return [
            {
                'dept_id': 1,
                'college_id': 1,
                'dept_name': 'Computer Science & Engineering',
                'hod_faculty_id': 1
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
    
    @staticmethod
    def get_divisions():
        """Get mock divisions"""
        return [
            {'division_id': 1, 'dept_id': 1, 'division_name': 'A'},
            {'division_id': 2, 'dept_id': 1, 'division_name': 'B'},
            {'division_id': 3, 'dept_id': 1, 'division_name': 'C'},
            {'division_id': 4, 'dept_id': 2, 'division_name': 'A'},
            {'division_id': 5, 'dept_id': 2, 'division_name': 'B'},
            {'division_id': 6, 'dept_id': 3, 'division_name': 'A'},
            {'division_id': 7, 'dept_id': 3, 'division_name': 'B'},
        ]
    
    @staticmethod
    def get_semesters():
        """Get mock semesters"""
        return [
            {'semester_id': 1, 'semester_no': 1, 'academic_year': '2024-2025'},
            {'semester_id': 2, 'semester_no': 2, 'academic_year': '2024-2025'},
            {'semester_id': 3, 'semester_no': 3, 'academic_year': '2024-2025'},
            {'semester_id': 4, 'semester_no': 4, 'academic_year': '2024-2025'},
        ]
    
    @staticmethod
    def get_users():
        """Get mock users"""
        return {
            'superadmin': {
                'user_id': 1,
                'college_id': 1,
                'name': 'Super Admin',
                'email': 'admin@attendance.system',
                'mobile': '9999999999',
                'role_id': 1,  # ADMIN
                'is_approved': True,
                'created_at': datetime(2020, 1, 1)
            },
            'college_admin': {
                'user_id': 2,
                'college_id': 1,
                'name': 'Ms. Neha Singh',
                'email': 'neha.singh@college.edu',
                'mobile': '9876543213',
                'role_id': 1,  # ADMIN
                'is_approved': True,
                'created_at': datetime(2021, 1, 20)
            },
            'hod': {
                'user_id': 3,
                'college_id': 1,
                'name': 'Prof. Amit Patel',
                'email': 'amit.patel@college.edu',
                'mobile': '9876543212',
                'role_id': 2,  # HOD
                'is_approved': True,
                'created_at': datetime(2020, 3, 5)
            },
            'faculty': {
                'user_id': 4,
                'college_id': 1,
                'name': 'Dr. Priya Sharma',
                'email': 'priya.sharma@college.edu',
                'mobile': '9876543211',
                'role_id': 3,  # FACULTY
                'is_approved': True,
                'created_at': datetime(2022, 6, 10)
            },
            'student': {
                'user_id': 5,
                'college_id': 1,
                'name': 'Raj Kumar',
                'email': 'raj.kumar@college.edu',
                'mobile': '9876543210',
                'role_id': 4,  # STUDENT
                'is_approved': True,
                'created_at': datetime(2023, 8, 15)
            },
            'parent': {
                'user_id': 6,
                'college_id': 1,
                'name': 'Shyam Kumar',
                'email': 'shyam.kumar@email.com',
                'mobile': '9876543214',
                'role_id': 5,  # PARENT
                'is_approved': True,
                'created_at': datetime(2023, 9, 1)
            }
        }
    
    @staticmethod
    def get_faculty():
        """Get mock faculty members"""
        return [
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
    
    @staticmethod
    def get_students():
        """Get mock students"""
        return [
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
    
    @staticmethod
    def get_parents():
        """Get mock parents"""
        return [
            {
                'user_id': 6,  # Shyam Kumar
                'student_id': 1
            }
        ]
    
    @staticmethod
    def get_subjects():
        """Get mock subjects"""
        return [
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
            },
            {
                'subject_id': 3,
                'dept_id': 1,
                'subject_name': 'Operating Systems',
                'subject_code': 'CS303',
                'semester_id': 3
            }
        ]
    
    @staticmethod
    def get_all_data():
        """Get all mock data at once"""
        return {
            'college': MockDataService.get_college(),
            'departments': MockDataService.get_departments(),
            'divisions': MockDataService.get_divisions(),
            'semesters': MockDataService.get_semesters(),
            'users': MockDataService.get_users(),
            'faculty': MockDataService.get_faculty(),
            'students': MockDataService.get_students(),
            'parents': MockDataService.get_parents(),
            'subjects': MockDataService.get_subjects(),
        }
