"""
Attendance Management System - Main Flask Application

This is the main application entry point that initializes Flask,
loads configuration, database, and registers all blueprints (routes).

The application is organized into modular route blueprints:
- routes/main.py: Home, About, Contact pages
- routes/auth.py: Login, Register
- routes/superadmin.py: Super Admin dashboard and profile
- routes/college.py: College admin routes
- routes/hod.py: Head of Department routes
- routes/faculty.py: Faculty routes
- routes/student.py: Student routes
- routes/parent.py: Parent routes
"""

from flask import Flask, g, session
from dotenv import load_dotenv
import os

from models.user import db, User


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+mysqlconnector://root:password@localhost:3306/attendance_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

# Initialize SQLAlchemy
db.init_app(app)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@app.context_processor
def inject_user():
    user = g.user
    # Provide safe fallback if user is None
    if user is None:
        user = type('User', (), {
            'user_id': None,
            'name': 'Guest',
            'email': 'guest@example.com',
            'mobile': None,
            'avatar': None,
            'is_approved': False,
            'created_at': None
        })()
    return dict(user=user)

# Create all database tables if they don't exist
with app.app_context():
    try:
        db.create_all()
        print("✓ Database tables created/verified successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        print("  Make sure MySQL is running and DATABASE_URL is correct in .env")

# ==================== REGISTER BLUEPRINTS ====================

def register_blueprints():
    """Register all route blueprints with the Flask application"""
    from routes import register_blueprints as register_all
    register_all(app)


# Register blueprints
register_blueprints()


if __name__ == "__main__":
    app.run(debug=True)
