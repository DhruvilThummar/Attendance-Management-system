"""Flask application factory."""

from __future__ import annotations

from flask import Flask, render_template
from dotenv import load_dotenv

from .config import Config
from .db_manager import init_db_pool
from .routes import api, core, dashboard, academic, attendance


def create_app(config: dict | None = None) -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config())
    if config:
        app.config.update(config)

    # Best-effort DB connectivity check; app can still run without DB.
    db_url = app.config.get("DATABASE_URL")
    if db_url:
        try:
            init_db_pool(db_url)
        except Exception as exc:
            app.logger.warning("DB not reachable (%s). Running without DB.", exc)

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(core)  # Core pages (/, /about, /contact)
    app.register_blueprint(dashboard)  # Dashboard (/dashboard, /settings, /profile, /reports)
    app.register_blueprint(academic)  # Academic (/faculty, /students, /timetable, /subjects, /departments)
    app.register_blueprint(attendance)  # Attendance (/mark-attendance, /student-attendance)

    return app
