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

# Export all blueprints for app.py to register
__all__ = [
    "api",           # API routes (prefix: /api)
    "auth",          # Auth pages (/login, /register)
    "core",          # Core pages (/, /about, /contact)
    "dashboard",     # Dashboard pages (/dashboard, /settings, /profile, /reports)
    "academic",      # Academic pages (/faculty, /students, /timetable, /subjects, /departments)
    "attendance"     # Attendance pages (/mark-attendance, /student-attendance)
]
