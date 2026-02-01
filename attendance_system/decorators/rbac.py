"""
Role-Based Access Control (RBAC) Decorators
===========================================

This module provides decorators for enforcing role-based access control
throughout the application. Each decorator checks user roles and permissions.

Decorators:
- login_required: Require user to be authenticated
- role_required: Require specific role(s)
- admin_only: Admin access only
- faculty_only: Faculty access only
- student_only: Student access only
- hod_only: HOD access only
- parent_only: Parent access only
- college_only: College admin access only

Usage:
    @login_required
    @role_required('FACULTY')
    def mark_attendance():
        pass

Author: Development Team
Version: 1.0
"""

from functools import wraps
from flask import session, redirect, url_for, jsonify, request
from typing import Union, List

# Role constants
ADMIN = "ADMIN"
HOD = "HOD"
FACULTY = "FACULTY"
STUDENT = "STUDENT"
PARENT = "PARENT"
COLLEGE = "COLLEGE"


def login_required(f):
    """
    Decorator: Require user to be authenticated
    
    Checks if user is logged in (in session).
    Redirects to login if not authenticated.
    
    Usage:
        @login_required
        def protected_view():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is in session
        if 'user_id' not in session:
            # If API request (JSON), return 401
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'error': 'Unauthorized'}), 401
            # Otherwise redirect to login
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def role_required(*roles: str):
    """
    Decorator: Require specific role(s)
    
    Checks if user has one of the specified roles.
    Multiple roles can be checked (OR condition).
    
    Args:
        *roles: One or more role strings (ADMIN, FACULTY, STUDENT, etc.)
    
    Usage:
        @role_required('FACULTY', 'HOD')
        def faculty_or_hod_view():
            pass
    
    Returns:
        Decorator function that enforces role check
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            if 'user_id' not in session:
                if request.headers.get('Content-Type') == 'application/json':
                    return jsonify({'error': 'Unauthorized'}), 401
                return redirect(url_for('auth.login'))
            
            # Get user role from session
            user_role = session.get('role')
            
            # Check if user has required role
            if user_role not in roles:
                # If API request, return 403
                if request.headers.get('Content-Type') == 'application/json':
                    return jsonify({'error': 'Forbidden: Access Denied'}), 403
                # Otherwise redirect to dashboard
                return redirect(url_for('get_dashboard'))
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def admin_only(f):
    """
    Decorator: Admin access only
    
    Only users with ADMIN role can access.
    
    Usage:
        @admin_only
        def admin_view():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') != ADMIN:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def faculty_only(f):
    """
    Decorator: Faculty access only
    
    Only users with FACULTY role can access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') != FACULTY:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def student_only(f):
    """
    Decorator: Student access only
    
    Only users with STUDENT role can access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') != STUDENT:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def hod_only(f):
    """
    Decorator: HOD access only
    
    Only users with HOD role can access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') != HOD:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def parent_only(f):
    """
    Decorator: Parent access only
    
    Only users with PARENT role can access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') != PARENT:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def college_only(f):
    """
    Decorator: College admin access only
    
    Only users with COLLEGE role can access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') != COLLEGE:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def hod_or_admin(f):
    """
    Decorator: HOD or Admin access
    
    Users with HOD or ADMIN role can access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') not in [HOD, ADMIN]:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def faculty_or_hod(f):
    """
    Decorator: Faculty or HOD access
    
    Users with FACULTY or HOD role can access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if session.get('role') not in [FACULTY, HOD]:
            return redirect(url_for('get_dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function
