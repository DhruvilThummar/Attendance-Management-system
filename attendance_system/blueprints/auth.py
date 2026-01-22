"""Authentication endpoints and entry pages."""
from __future__ import annotations

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

bp = Blueprint("auth", __name__)


@bp.get("/")
def home():
    return render_template("home.html")


@bp.get("/login")
def login_form():
    return render_template("auth/login.html")


@bp.post("/login")
def login():
    # TODO: hook up auth_service.verify_credentials
    _ = (request.form.get("email"), request.form.get("password"))
    return jsonify(message="login processing placeholder"), 501


@bp.post("/logout")
def logout():
    return redirect(url_for("auth.home"))
