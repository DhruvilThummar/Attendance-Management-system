"""Authentication page routes."""

from __future__ import annotations

from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.get("/login")
def login_page():
    """Login page."""
    return render_template("login.html")


@auth.get("/register")
def register_page():
    """Registration page."""
    return render_template("register.html")