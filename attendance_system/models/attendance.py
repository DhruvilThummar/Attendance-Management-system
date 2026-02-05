"""
Attendance and AttendanceStatus models
"""

from datetime import datetime
from .user import db


class AttendanceStatus(db.Model):
    """Attendance status lookup model (PRESENT, ABSENT)"""
    
    __tablename__ = 'attendance_status'
    
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relationships
    attendances = db.relationship('Attendance', back_populates='status')
    
    def __repr__(self):
        return f'<AttendanceStatus {self.status_name}>'


class Attendance(db.Model):
    """Student attendance record"""
    
    __tablename__ = 'attendance'
    
    attendance_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id', ondelete='CASCADE'), nullable=False, index=True)
    status_id = db.Column(db.Integer, db.ForeignKey('attendance_status.status_id'), nullable=False)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.lecture_id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    student = db.relationship('Student', back_populates='attendances')
    status = db.relationship('AttendanceStatus', back_populates='attendances')
    lecture = db.relationship('Lecture', back_populates='attendances')
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'lecture_id', name='uq_attendance_student_lecture'),
        db.Index('idx_attendance_student', 'student_id'),
    )
    
    def __repr__(self):
        return f'<Attendance Student:{self.student_id} Status:{self.status.status_name}>'
    
    def is_present(self):
        """Check if this attendance record is marked as PRESENT"""
        return self.status_id == 1
