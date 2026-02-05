"""
Database initialization and configuration
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()
        
        # Create default roles if they don't exist
        from .models import Role
        
        default_roles = [
            ('ADMIN', 1),
            ('HOD', 2),
            ('FACULTY', 3),
            ('STUDENT', 4),
            ('PARENT', 5),
        ]
        
        for role_name, role_id in default_roles:
            role = Role.query.get(role_id)
            if not role:
                role = Role(role_id=role_id, role_name=role_name)
                db.session.add(role)
        
        # Create default attendance statuses
        from .models import AttendanceStatus
        
        statuses = [
            ('PRESENT', 1),
            ('ABSENT', 2),
        ]
        
        for status_name, status_id in statuses:
            status = AttendanceStatus.query.get(status_id)
            if not status:
                status = AttendanceStatus(status_id=status_id, status_name=status_name)
                db.session.add(status)
        
        db.session.commit()


def reset_db(app):
    """Drop all tables and recreate them (use with caution!)"""
    with app.app_context():
        db.drop_all()
        init_db(app)
