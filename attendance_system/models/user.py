"""
User and Role models
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from utils.simple_hash import simple_hash, verify_simple_hash


db = SQLAlchemy()


class Role(db.Model):
    """Role model for user roles (ADMIN, HOD, FACULTY, STUDENT, PARENT)"""
    
    __tablename__ = 'role'
    
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    users = db.relationship('User', back_populates='role', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Role {self.role_name}>'


class User(db.Model):
    """User model for all system users"""
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.college_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(15))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    
    # Relationships
    college = db.relationship('College', back_populates='users')
    role = db.relationship('Role', back_populates='users')
    faculty = db.relationship('Faculty', uselist=False, back_populates='user')
    student = db.relationship('Student', uselist=False, back_populates='user')
    parent = db.relationship('Parent', uselist=False, back_populates='user')
    
    def __repr__(self):
        return f'<User {self.email} - {self.name}>'
    
    def set_password(self, password):
        """Hash and set password using simple custom hashing"""
        self.password_hash = simple_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash using simple verification"""
        return verify_simple_hash(password, self.password_hash)
    
    def get_role_name(self):
        """Get the role name for this user"""
        return self.role.role_name if self.role else None
