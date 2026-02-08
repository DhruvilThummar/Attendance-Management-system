"""
Division model
"""

from .user import db


class Division(db.Model):
    """Division/Section model (Division A, B, C etc. within a department)"""
    
    __tablename__ = 'division'
    
    division_id = db.Column(db.Integer, primary_key=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id', ondelete='CASCADE'), nullable=False)
    division_name = db.Column(db.String(50), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.semester_id', ondelete='SET NULL'))
    capacity = db.Column(db.Integer)
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id', ondelete='SET NULL'))
    
    # Relationships
    department = db.relationship('Department', back_populates='divisions')
    students = db.relationship('Student', back_populates='division')
    timetables = db.relationship('Timetable', back_populates='division', cascade='all, delete-orphan')
    semester = db.relationship('Semester', backref='divisions')
    class_teacher = db.relationship('Faculty', foreign_keys=[class_teacher_id], backref='divisions_as_class_teacher')
    
    def __repr__(self):
        return f'<Division {self.division_name}>'
