"""
Lecture model
"""

from datetime import datetime
from .user import db


class Lecture(db.Model):
    """Lecture/Class session model"""
    
    __tablename__ = 'lecture'
    
    lecture_id = db.Column(db.Integer, primary_key=True)
    timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.timetable_id', ondelete='CASCADE'), nullable=False)
    lecture_date = db.Column(db.Date, nullable=False)
    
    # Relationships
    timetable = db.relationship('Timetable', back_populates='lectures')
    attendances = db.relationship('Attendance', back_populates='lecture', cascade='all, delete-orphan')
    proxy_lectures = db.relationship('ProxyLecture', back_populates='lecture', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('timetable_id', 'lecture_date', name='uq_lecture_timetable_date'),
    )
    
    def __repr__(self):
        return f'<Lecture {self.timetable.subject.subject_code} on {self.lecture_date}>'
    
    def get_attendance_count(self, status_id=None):
        """Get attendance count for this lecture"""
        query = Attendance.query.filter_by(lecture_id=self.lecture_id)
        if status_id:
            query = query.filter_by(status_id=status_id)
        return query.count()
