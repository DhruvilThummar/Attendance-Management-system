"""
Super Admin routes - Dashboard and Administration
"""
from flask import Blueprint, render_template, request, jsonify
from services.data_helper import DataHelper

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')


@superadmin_bp.route("/dashboard")
def sudashboard():
    """Super Admin Dashboard"""
    colleges = DataHelper.get_college()
    users = DataHelper.get_users()
    departments = DataHelper.get_departments()
    return render_template("superadmin/sudashboard.html",
                          title="Super Admin Dashboard",
                          colleges=colleges,
                          users=users,
                          departments=departments)


@superadmin_bp.route("")
def superadmin_redirect():
    """Redirect to super admin dashboard"""
    return sudashboard()


@superadmin_bp.route("/profile")
def superadmin_profile():
    """Super Admin Profile"""
    users = DataHelper.get_users()
    return render_template("superadmin/profile.html",
                          title="Super Admin Profile",
                          users=users)


@superadmin_bp.route("/manage-colleges")
def manage_colleges():
    """Manage colleges"""
    colleges = DataHelper.get_college()
    return render_template("superadmin/manage_colleges.html",
                          title="Manage Colleges",
                          colleges=colleges)


@superadmin_bp.route("/manage-users")
def manage_users():
    """Manage users"""
    users = DataHelper.get_users()
    return render_template("superadmin/manage_users.html",
                          title="Manage Users",
                          users=users)
