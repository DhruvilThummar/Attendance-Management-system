"""
Main routes - Home, About, Contact
"""
from flask import Blueprint, render_template, request
from services.data_helper import DataHelper

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def home():
    """Home page"""
    college = DataHelper.get_college()
    return render_template("home.html", college=college)


@main_bp.route("/about")
def about():
    """About page"""
    college = DataHelper.get_college()
    return render_template("about.html", college=college)


@main_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        # TODO: Handle contact form submission
        pass
    college = DataHelper.get_college()
    return render_template("contact.html", college=college)
