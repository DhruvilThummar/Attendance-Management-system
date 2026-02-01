"""Core page routes - Public pages and general navigation."""

from __future__ import annotations

from flask import Blueprint, render_template

core = Blueprint("core", __name__)


@core.get("/")
def home():
    """Home page."""
    return render_template("home.html")


@core.get("/about")
def about():
    """About page."""
    return render_template("about.html")


@core.get("/contact")
def contact():
    """Contact page."""
    return render_template("contact.html")
