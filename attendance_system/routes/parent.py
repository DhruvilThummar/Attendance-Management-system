"""
Parent routes - Dashboard and Profile
"""
from flask import Blueprint, render_template
from services.data_helper import DataHelper

parent_bp = Blueprint('parent', __name__, url_prefix='/parent')


@parent_bp.route("/dashboard")
def pdashboard():
    """Parent Dashboard"""
    parents = DataHelper.get_parents()
    return render_template("parent/pbase.html", 
                          title="Parent Dashboard",
                          parents=parents)


@parent_bp.route("")
def parent_redirect():
    """Redirect to parent dashboard"""
    return pdashboard()


@parent_bp.route("/profile")
def parent_profile():
    """Parent Profile"""
    parents = DataHelper.get_parents()
    college = DataHelper.get_college()
    return render_template("parent/profile.html",
                          title="Parent Profile",
                          parents=parents,
                          college=college)
