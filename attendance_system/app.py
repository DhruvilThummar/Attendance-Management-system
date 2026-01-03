"""Flask application factory and RBAC decorators."""
from __future__ import annotations

from flask import Flask, abort, g, redirect, request, session, url_for

from .config import DefaultConfig
from .db_manager import init_db_pool


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(DefaultConfig())
    if config:
        app.config.update(config)

    init_db_pool(app.config.get("DATABASE_URL"))

    # Deferred import to avoid circulars
    from .blueprints import admin_bp, auth_bp, faculty_bp, hod_bp, student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(hod_bp, url_prefix="/hod")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(student_bp, url_prefix="/student")

    @app.before_request
    def load_user() -> None:  # placeholder for session-backed user load
        g.user = session.get("user")

    return app


def role_required(*roles: str):
    """Decorator enforcing that g.user has one of the required roles."""

    def decorator(fn):
        def wrapper(*args, **kwargs):
            user = getattr(g, "user", None)
            if not user or user.get("role") not in roles:
                if user:
                    abort(403)
                return redirect(url_for("auth.login", next=request.path))
            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper

    return decorator


if __name__ == "__main__":
    create_app().run(debug=True)
