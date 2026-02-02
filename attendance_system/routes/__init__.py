"""Route blueprints - Organized by domain."""

from __future__ import annotations

from flask import Blueprint

# API Blueprint for REST endpoints
api = Blueprint("api", __name__)

# Import core page blueprints
from .core import core
from .dashboard import dashboard
from .academic import academic
from .pages import attendance
from .auth_pages import auth

# Import API route modules to register routes on the api blueprint
from . import login
from . import registration
from . import reports
from . import departments
from . import attendance_api
from . import lookup
from . import notifications

# Import standalone blueprints
from .students import students_bp
from .faculty import faculty_bp
from .timetable import timetable_bp
from .profile import profile_bp
from .lectures import lectures_bp

# Export all blueprints for app.py to register
__all__ = [
    "api",           # API routes (prefix: /api)
    "auth",          # Auth pages (/login, /register)
    "core",          # Core pages (/, /about, /contact)
    "dashboard",     # Dashboard pages (/dashboard, /settings, /profile, /reports)
    "academic",      # Academic pages (/faculty, /students, /timetable, /subjects, /departments)
    "attendance",    # Attendance pages (/mark-attendance, /student-attendance)
    "students_bp",   # Student API routes
    "faculty_bp",    # Faculty API routes
    "timetable_bp",  # Timetable API routes
    "profile_bp",    # Profile API routes
    "lectures_bp"    # Lectures API routes
]
