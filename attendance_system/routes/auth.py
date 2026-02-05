"""
Authentication routes - Login, Register, Logout
"""
from flask import Blueprint, render_template, request, redirect, url_for, session
from services.data_helper import DataHelper

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # TODO: Validate credentials against database
        session['user_id'] = username
        return redirect(url_for('college.cdashboard'))
    return render_template("login.html")


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        # TODO: Create new user in database
        return redirect(url_for('auth.login'))
    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('auth.login'))
