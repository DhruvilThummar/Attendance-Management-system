"""
Academic Calendar model
"""

from .user import db


class AcademicCalendar(db.Model):
    """Academic calendar events (holidays, exams, etc.)"""
    
    __tablename__ = 'academic_calendar'
    
    college_id = db.Column(db.Integer, db.ForeignKey('college.college_id', ondelete='CASCADE'), primary_key=True)
    event_date = db.Column(db.Date, primary_key=True, nullable=False)
    event_type = db.Column(
        db.Enum('REGULAR', 'EXAM', 'HOLIDAY'),
        primary_key=True,
        nullable=False
    )
    description = db.Column(db.String(255))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), primary_key=True, nullable=False)
    
    # Relationships
    college = db.relationship('College')
    department = db.relationship('Department')
    
    def __repr__(self):
        return f'<AcademicCalendar {self.event_type} on {self.event_date}>'
