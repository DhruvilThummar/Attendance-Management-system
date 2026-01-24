"""Flask application factory and RBAC decorators."""
from __future__ import annotations

from flask import Flask, abort, g, redirect, request, session, url_for, render_template
from dotenv import load_dotenv

from .config import DefaultConfig
from .db_manager import init_db_pool


def create_app(config: dict | None = None) -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(DefaultConfig())
    if config:
        app.config.update(config)

    db_url = app.config.get("DATABASE_URL")
    if db_url:
        try:
            init_db_pool(db_url)
        except Exception as e:
            # Log warning but allow app to start for frontend development
            import logging
            logging.warning(f"Failed to connect to database: {e}. Running in demo mode.")

    # Deferred import to avoid circulars
    from .blueprints import admin_bp, auth_bp, faculty_bp, hod_bp, student_bp, super_admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(super_admin_bp, url_prefix="/super_admin")
    app.register_blueprint(hod_bp, url_prefix="/hod")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(student_bp, url_prefix="/student")

    @app.before_request
    def load_user() -> None:  # placeholder for session-backed user load
        g.user = session.get("user")

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    return app


def role_required(*roles: str):
    """Decorator enforcing that g.user has one of the required roles."""

    def decorator(fn):
        def wrapper(*args, **kwargs):
            user = getattr(g, "user", None)
            
            # 1. Check if user is logged in
            if not user:
                print(f"⚠️ Unauthorized access attempt to {request.path} (No User)")
                return redirect(url_for("auth.login_form", next=request.path))
            
            # 2. Check if user has required role
            user_role = user.get("role")
            if user_role not in roles:
                print(f"⛔ Forbidden access attempt to {request.path} by {user.get('email')} (Role: {user_role}). Required: {roles}")
                abort(403)
                
            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper

    return decorator


if __name__ == "__main__":
    create_app().run(debug=True)
