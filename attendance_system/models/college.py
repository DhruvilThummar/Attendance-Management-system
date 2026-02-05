"""
College, Department, and Division models
"""

from datetime import datetime
from .user import db


class College(db.Model):
    """College model"""
    
    __tablename__ = 'college'
    
    college_id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    users = db.relationship('User', back_populates='college', cascade='all, delete-orphan')
    departments = db.relationship('Department', back_populates='college', cascade='all, delete-orphan')
    academic_calendars = db.relationship('AcademicCalendar', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<College {self.college_name}>'


class Department(db.Model):
    """Department model"""
    
    __tablename__ = 'department'
    
    dept_id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.college_id', ondelete='CASCADE'), nullable=False)
    dept_name = db.Column(db.String(100), nullable=False)
    hod_faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id', ondelete='SET NULL'), unique=True)
    
    # Relationships
    college = db.relationship('College', back_populates='departments')
    hod_faculty = db.relationship('Faculty', foreign_keys=[hod_faculty_id])
    divisions = db.relationship('Division', back_populates='department', cascade='all, delete-orphan')
    faculty_members = db.relationship('Faculty', foreign_keys='Faculty.dept_id', back_populates='department')
    students = db.relationship('Student', back_populates='department')
    subjects = db.relationship('Subject', back_populates='department', cascade='all, delete-orphan')
    academic_calendars = db.relationship('AcademicCalendar', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Department {self.dept_name}>'


class Division(db.Model):
    """Division/Section model (Division A, B, C etc. within a department)"""
    
    __tablename__ = 'division'
    
    division_id = db.Column(db.Integer, primary_key=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id', ondelete='CASCADE'), nullable=False)
    division_name = db.Column(db.String(50), nullable=False)
    
    # Relationships
    department = db.relationship('Department', back_populates='divisions')
    students = db.relationship('Student', back_populates='division')
    timetables = db.relationship('Timetable', back_populates='division', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Division {self.division_name}>'
