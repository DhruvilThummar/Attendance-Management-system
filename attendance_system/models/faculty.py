"""
Faculty model
"""

from .user import db


class Faculty(db.Model):
    """Faculty/Teacher model"""
    
    __tablename__ = 'faculty'
    
    faculty_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id', ondelete='CASCADE'), nullable=False)
    short_name = db.Column(db.String(50))
    
    # Relationships
    user = db.relationship('User', back_populates='faculty')
    department = db.relationship('Department', foreign_keys=[dept_id], back_populates='faculty_members')
    timetables = db.relationship('Timetable', back_populates='faculty', cascade='all, delete-orphan')
    students_mentored = db.relationship('Student', foreign_keys='Student.mentor_id', back_populates='mentor')
    original_proxy_lectures = db.relationship(
        'ProxyLecture',
        foreign_keys='ProxyLecture.original_faculty_id',
        back_populates='original_faculty'
    )
    substitute_proxy_lectures = db.relationship(
        'ProxyLecture',
        foreign_keys='ProxyLecture.substitute_faculty_id',
        back_populates='substitute_faculty'
    )
    
    def __repr__(self):
        return f'<Faculty {self.user.name} - {self.short_name}>'
