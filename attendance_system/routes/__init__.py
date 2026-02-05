"""
Routes package for Attendance Management System
"""

from flask import Blueprint

# Import all blueprints
from .main import main_bp
from .auth import auth_bp
from .superadmin import superadmin_bp
from .college import college_bp
from .hod import hod_bp
from .faculty import faculty_bp
from .student import student_bp
from .parent import parent_bp

# List of all blueprints to register
blueprints = [
    main_bp,
    auth_bp,
    superadmin_bp,
    college_bp,
    hod_bp,
    faculty_bp,
    student_bp,
    parent_bp
]

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
