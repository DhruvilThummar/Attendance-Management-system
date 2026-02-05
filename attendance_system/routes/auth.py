"""
Authentication routes - Login, Register
"""
from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login")
def login():
    """User login page"""
    return render_template("login.html")


@auth_bp.route("/register")
def register():
    """User registration page"""
    return render_template("register.html")
