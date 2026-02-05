"""
College model
"""

from datetime import datetime
from .user import db


class College(db.Model):
    """College model"""
    
    __tablename__ = 'college'
    
    college_id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    users = db.relationship('User', back_populates='college', cascade='all, delete-orphan')
    departments = db.relationship('Department', back_populates='college', cascade='all, delete-orphan')
    academic_calendars = db.relationship('AcademicCalendar', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<College {self.college_name}>'
