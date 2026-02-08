"""
Academic Calendar model
"""

from .user import db


class AcademicCalendar(db.Model):
    """Academic calendar events (holidays, exams, etc.)"""
    
    __tablename__ = 'academic_calendar'
    
    college_id = db.Column(db.Integer, db.ForeignKey('college.college_id', ondelete='CASCADE'), primary_key=True)
    event_date = db.Column(db.Date, primary_key=True, nullable=False)
    description = db.Column(db.String(255))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id', ondelete='CASCADE'), nullable=False)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.event_type_id'))
    
    # Relationships
    college = db.relationship('College', overlaps='academic_calendars')
    department = db.relationship('Department', overlaps='academic_calendars')
    event_type = db.relationship('EventType', backref='calendar_events')
    
    def __repr__(self):
        return f'<AcademicCalendar {self.event_type} on {self.event_date}>'
