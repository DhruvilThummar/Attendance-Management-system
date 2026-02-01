"""
Flask Application Factory Module
=================================

This module creates and configures the Flask application.

Key Features:
- Application factory pattern for flexibility
- Blueprint registration for organized routing
- Database connection pooling
- Error handling and logging
- Environment configuration loading

Author: Development Team
Version: 1.0

Usage:
    app = create_app()
    app.run()
"""

from __future__ import annotations

from flask import Flask, render_template
from dotenv import load_dotenv

from .config import Config
from .db_manager import init_db_pool
from .blueprints.dashboards import dashboards
from .routes import api, core, dashboard, academic, attendance


def create_app(config: dict | None = None) -> Flask:
    """
    Application Factory Function
    
    Creates and configures the Flask application instance.
    This pattern allows for flexible app creation with different
    configurations for testing, development, and production.
    
    Features:
    - Loads environment variables from .env file
    - Applies base configuration from config.py
    - Allows override configuration via parameter
    - Initializes database connection pool (non-blocking)
    - Registers all blueprints for routing
    
    Args:
        config (dict | None): Optional configuration dictionary
                             to override default configuration
    
    Returns:
        Flask: Configured Flask application instance
    
    Raises:
        Exception: If database initialization fails (logged but doesn't block)
    
    Example:
        # Create app with default configuration
        app = create_app()
        
        # Create app with testing configuration
        test_config = {'TESTING': True}
        app = create_app(test_config)
    """
    # Load environment variables from .env file
    load_dotenv()

    # Create Flask application instance
    app = Flask(__name__)
    
    # Apply base configuration from config.py
    app.config.from_object(Config())
    
    # Override with provided config if any
    if config:
        app.config.update(config)

    # Initialize database connection pool
    # Uses best-effort approach - app can run without DB if needed
    db_url = app.config.get("DATABASE_URL")
    if db_url:
        try:
            # Attempt to initialize database connection pool
            init_db_pool(db_url)
        except Exception as exc:
            # Log warning but don't block app startup
            app.logger.warning("DB not reachable (%s). Running without DB.", exc)

    # ========== BLUEPRINT REGISTRATION ==========
    # Register blueprints for organized routing
    # Blueprints allow grouping related routes together
    
    # Role-based dashboards - Dynamic dashboards for each user role
    # Routes: /dashboard/* (Faculty, HOD, Student, Parent, College, Admin)
    app.register_blueprint(dashboards)
    
    # API endpoints - RESTful API routes
    # Prefix: /api
    app.register_blueprint(api, url_prefix="/api")
    
    # Core pages - Main application pages
    # Routes: /, /about, /contact
    app.register_blueprint(core)
    
    # Dashboard pages - User dashboards
    # Routes: /dashboard, /settings, /profile, /reports
    app.register_blueprint(dashboard)
    
    # Academic management pages
    # Routes: /faculty, /students, /timetable, /subjects, /departments
    app.register_blueprint(academic)
    
    # Attendance management pages
    # Routes: /mark-attendance, /student-attendance
    app.register_blueprint(attendance)

    return app
