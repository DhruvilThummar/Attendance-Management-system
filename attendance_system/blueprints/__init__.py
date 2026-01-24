"""Blueprint registry for the attendance system."""
from .auth import bp as auth_bp
from .admin import bp as admin_bp
from .hod import bp as hod_bp
from .faculty import bp as faculty_bp
from .student import bp as student_bp
from .super_admin import bp as super_admin_bp

__all__ = [
    "auth_bp",
    "admin_bp",
    "hod_bp",
    "faculty_bp",
    "student_bp",
]
