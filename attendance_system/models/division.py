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
    
    # Relationships
    department = db.relationship('Department', back_populates='divisions')
    students = db.relationship('Student', back_populates='division')
    timetables = db.relationship('Timetable', back_populates='division', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Division {self.division_name}>'
