"""
Super Admin routes - Dashboard and Profile
"""
from flask import Blueprint, render_template
from datetime import datetime

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')

# Import mock data from app
def get_mock_data():
    from app import mock_users, mock_system_stats
    return mock_users, mock_system_stats


@superadmin_bp.route("/dashboard")
def dashboard():
    """Super Admin Dashboard"""
    return render_template("superadmin/subase.html", title="Super Admin Dashboard")


@superadmin_bp.route("")
def sdashboard():
    """Alias for super admin dashboard"""
    return render_template("superadmin/subase.html", title="Super Admin Dashboard")


@superadmin_bp.route("/profile")
def superadmin_profile():
    """Super Admin Profile"""
    mock_users, mock_system_stats = get_mock_data()
    return render_template("superadmin/profile.html",
                         title="Super Admin Profile",
                         user=mock_users['superadmin'],
                         system_stats=mock_system_stats)
