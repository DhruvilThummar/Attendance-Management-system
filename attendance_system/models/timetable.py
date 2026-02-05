"""
Timetable model
"""

from .user import db


class Timetable(db.Model):
    """Timetable/Class Schedule model"""
    
    __tablename__ = 'timetable'
    
    timetable_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id', ondelete='CASCADE'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id', ondelete='CASCADE'), nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey('division.division_id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(
        db.Enum('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'),
        nullable=False
    )
    lecture_no = db.Column(db.Integer, nullable=False)
    room_no = db.Column(db.String(20))
    building_block = db.Column(db.String(50))
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # Relationships
    subject = db.relationship('Subject', back_populates='timetables')
    faculty = db.relationship('Faculty', back_populates='timetables')
    division = db.relationship('Division', back_populates='timetables')
    lectures = db.relationship('Lecture', back_populates='timetable', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Timetable {self.subject.subject_code} - {self.day_of_week} Lecture {self.lecture_no}>'
