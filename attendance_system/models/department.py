"""
Department model
"""

from .user import db


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
