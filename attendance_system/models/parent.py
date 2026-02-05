"""
Parent model
"""

from .user import db


class Parent(db.Model):
    """Parent/Guardian model"""
    
    __tablename__ = 'parent'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='parent')
    student = db.relationship('Student', back_populates='parents')
    
    def __repr__(self):
        return f'<Parent {self.user.name} of Student {self.student.enrollment_no}>'
