"""
Database Query Helper

This module provides helper functions for routes to query data.
Currently uses mock data, can be easily switched to real database queries.
"""

from services.mock_data import MockDataService


class DataHelper:
    """Helper class to get data - works with both mock and real database"""
    
    @staticmethod
    def get_user(user_type='student'):
        """Get user by type"""
        users = MockDataService.get_users()
        return users.get(user_type)
    
    @staticmethod
    def get_college():
        """Get college data"""
        return MockDataService.get_college()
    
    @staticmethod
    def get_departments():
        """Get all departments"""
        return MockDataService.get_departments()
    
    @staticmethod
    def get_department(dept_id):
        """Get specific department"""
        departments = MockDataService.get_departments()
        return next((d for d in departments if d['dept_id'] == dept_id), None)
    
    @staticmethod
    def get_divisions(dept_id=None):
        """Get divisions, optionally filtered by department"""
        divisions = MockDataService.get_divisions()
        if dept_id:
            return [d for d in divisions if d['dept_id'] == dept_id]
        return divisions
    
    @staticmethod
    def get_division(division_id):
        """Get specific division"""
        divisions = MockDataService.get_divisions()
        return next((d for d in divisions if d['division_id'] == division_id), None)
    
    @staticmethod
    def get_faculty(dept_id=None):
        """Get faculty members, optionally filtered by department"""
        faculty = MockDataService.get_faculty()
        if dept_id:
            return [f for f in faculty if f['dept_id'] == dept_id]
        return faculty
    
    @staticmethod
    def get_students(division_id=None, dept_id=None):
        """Get students with optional filters"""
        students = MockDataService.get_students()
        
        if division_id:
            students = [s for s in students if s['division_id'] == division_id]
        if dept_id:
            students = [s for s in students if s['dept_id'] == dept_id]
        
        return students
    
    @staticmethod
    def get_student(student_id):
        """Get specific student"""
        students = MockDataService.get_students()
        return next((s for s in students if s['student_id'] == student_id), None)
    
    @staticmethod
    def get_subjects(dept_id=None, semester_id=None):
        """Get subjects with optional filters"""
        subjects = MockDataService.get_subjects()
        
        if dept_id:
            subjects = [s for s in subjects if s['dept_id'] == dept_id]
        if semester_id:
            subjects = [s for s in subjects if s['semester_id'] == semester_id]
        
        return subjects
    
    @staticmethod
    def get_semesters():
        """Get all semesters"""
        return MockDataService.get_semesters()


# Transition helper comments for database migration
MIGRATION_NOTES = """
To migrate from mock data to real database:

1. In routes, replace:
   from services.mock_data import MockDataService
   mock_data = MockDataService.get_data()
   
   With:
   from models import User, Student, Faculty, etc.
   user = User.query.get(user_id)

2. Replace DataHelper calls:
   department = DataHelper.get_department(1)
   
   With:
   from models import Department
   department = Department.query.get(1)

3. Update any mock data filtering to use SQLAlchemy queries:
   students = DataHelper.get_students(div_id=1)
   
   With:
   students = Student.query.filter_by(division_id=1).all()

4. Test each route after migration to ensure data is correctly retrieved.
"""
