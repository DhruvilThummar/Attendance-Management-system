"""Dashboard routes - User dashboards and overview pages."""

from __future__ import annotations

from flask import Blueprint, render_template

dashboard = Blueprint("dashboard", __name__)


@dashboard.get("/dashboard")
def dashboard_home():
    """Main dashboard page."""
    return render_template("dashboard.html")


@dashboard.get("/settings")
def settings():
    """Settings page."""
    return render_template("settings.html")


@dashboard.get("/profile")
def profile():
    """User profile page."""
    return render_template("profile.html")


@dashboard.get("/reports")
def reports():
    """Reports page."""
    return render_template("reports.html")
