"""
Authentication and Authorization Decorators
Provides route protection for login requirements and role-based access control
"""

from functools import wraps
from flask import session, redirect, url_for, abort
from models.user import User, db


def login_required(f):
    """Decorator that requires user to be logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'role' not in session:
            return redirect(url_for('auth.login'))
        
        # Verify user still exists in database
        user = User.query.get(session['user_id'])
        if not user or not user.is_approved:
            # Clear invalid session
            session.clear()
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """Decorator that requires specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or 'role' not in session:
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role')
            
            # Check if user's role is in allowed roles
            if user_role not in allowed_roles:
                # User is logged in but doesn't have correct role
                abort(403)  # Forbidden
            
            # Verify user still exists and is approved
            user = User.query.get(session['user_id'])
            if not user or not user.is_approved:
                session.clear()
                return redirect(url_for('auth.login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def superadmin_required(f):
    """Decorator requiring SUPERADMIN role"""
    return role_required('SUPERADMIN')(f)


def college_admin_required(f):
    """Decorator requiring ADMIN (College Admin) role"""
    return role_required('ADMIN')(f)


def hod_required(f):
    """Decorator requiring HOD role"""
    return role_required('HOD')(f)


def faculty_required(f):
    """Decorator requiring FACULTY role"""
    return role_required('FACULTY')(f)


def student_required(f):
    """Decorator requiring STUDENT role"""
    return role_required('STUDENT')(f)


def parent_required(f):
    """Decorator requiring PARENT role"""
    return role_required('PARENT')(f)


def admin_or_hod_required(f):
    """Decorator requiring ADMIN or HOD roles"""
    return role_required('ADMIN', 'HOD')(f)


def admin_or_faculty_required(f):
    """Decorator requiring ADMIN or FACULTY roles"""
    return role_required('ADMIN', 'FACULTY')(f)
