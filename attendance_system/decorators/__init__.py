"""RBAC decorators - Role-Based Access Control."""

from functools import wraps
from typing import Callable

from flask import session, jsonify, redirect, url_for, request

from ..exceptions import AuthenticationError, AuthorizationError


def require_auth(f: Callable) -> Callable:
    """Decorator to require authentication."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("core.login"))
        return f(*args, **kwargs)

    return decorated_function


def require_role(*allowed_roles) -> Callable:
    """Decorator to require specific roles.
    
    Usage:
        @require_role("ADMIN", "HOD")
        def admin_route():
            pass
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"error": "Unauthorized"}), 401
                return redirect(url_for("core.login"))

            user_role = session.get("role", "")
            if user_role not in allowed_roles:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"error": "Forbidden"}), 403
                return (
                    jsonify({"error": "Access Denied"}),
                    403,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_approval(f: Callable) -> Callable:
    """Decorator to require user approval."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("core.login"))

        is_approved = session.get("is_approved", False)
        if not is_approved:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return (
                    jsonify({"error": "Account not approved"}),
                    403,
                )
            return (
                jsonify({"error": "Your account is not approved yet"}),
                403,
            )

        return f(*args, **kwargs)

    return decorated_function


def admin_only(f: Callable) -> Callable:
    """Decorator to restrict to admin only."""
    return require_role("ADMIN")(f)


def faculty_access(f: Callable) -> Callable:
    """Decorator to allow faculty and admin."""
    return require_role("ADMIN", "FACULTY", "HOD")(f)


def student_access(f: Callable) -> Callable:
    """Decorator to allow student access."""
    return require_role("ADMIN", "STUDENT")(f)
