"""
Proxy Lecture model
"""

from datetime import datetime
from .user import db


class ProxyLecture(db.Model):
    """Proxy lecture (substitute faculty) model"""
    
    __tablename__ = 'proxy_lecture'
    
    proxy_id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.lecture_id', ondelete='CASCADE'), nullable=False)
    original_faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    substitute_faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    lecture_date = db.Column(db.Date, nullable=False)
    lecture_no = db.Column(db.Integer, nullable=False)
    room_no = db.Column(db.String(20))
    building_block = db.Column(db.String(50))
    reason = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('proxy_status.status_id'))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    lecture = db.relationship('Lecture', back_populates='proxy_lectures')
    original_faculty = db.relationship('Faculty', foreign_keys=[original_faculty_id], back_populates='original_proxy_lectures')
    substitute_faculty = db.relationship('Faculty', foreign_keys=[substitute_faculty_id], back_populates='substitute_proxy_lectures')
    subject = db.relationship('Subject', back_populates='proxy_lectures')
    status = db.relationship('ProxyStatus', backref='proxy_lectures')
    
    def __repr__(self):
        return f'<ProxyLecture {self.original_faculty.user.name} -> {self.substitute_faculty.user.name}>'
