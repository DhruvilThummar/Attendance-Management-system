"""
Main routes - Home, About, Contact, Profile Test
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def home():
    """Home page"""
    return render_template("home.html")


@main_bp.route("/about")
def about():
    """About page"""
    return render_template("about.html")


@main_bp.route("/contact")
def contact():
    """Contact page"""
    return render_template("contact.html")


@main_bp.route("/profiles")
@main_bp.route("/profile-test")
def profile_test():
    """Profile test page"""
    return render_template("profile_test.html")
