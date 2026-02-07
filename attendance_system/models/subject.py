"""
Subject and Semester models
"""

from .user import db


class Semester(db.Model):
    """Semester model"""
    
    __tablename__ = 'semester'
    
    semester_id = db.Column(db.Integer, primary_key=True)
    semester_no = db.Column(db.Integer, nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)  # Format: 2024-2025
    
    # Relationships
    students = db.relationship('Student', back_populates='semester')
    subjects = db.relationship('Subject', back_populates='semester', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('semester_no', 'academic_year', name='uq_semester_year'),
    )
    
    def __repr__(self):
        return f'<Semester {self.semester_no} - {self.academic_year}>'


class Subject(db.Model):
    """Subject/Course model"""
    
    __tablename__ = 'subject'
    
    subject_id = db.Column(db.Integer, primary_key=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id', ondelete='CASCADE'), nullable=False)
    subject_name = db.Column(db.String(120), nullable=False)
    subject_code = db.Column(db.String(20), unique=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.semester_id', ondelete='CASCADE'), nullable=False)
    credits = db.Column(db.Integer)
    
    # Relationships
    department = db.relationship('Department', back_populates='subjects')
    semester = db.relationship('Semester', back_populates='subjects')
    timetables = db.relationship('Timetable', back_populates='subject', cascade='all, delete-orphan')
    proxy_lectures = db.relationship('ProxyLecture', back_populates='subject')
    
    def __repr__(self):
        return f'<Subject {self.subject_code} - {self.subject_name}>'
