"""Authentication endpoints and entry pages."""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from ..services import auth_service

bp = Blueprint("auth", __name__)


@bp.get("/")
def home():
    return render_template("home.html")


@bp.get("/login")
def login_form():
    next_path = request.args.get("next")
    return render_template("auth/login.html", next_path=next_path)


@bp.get("/about")
def about():
    return render_template("about.html")


@bp.post("/login")
def login():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    next_path = request.form.get("next") or request.args.get("next")

    if not email or not password:
        return (
            render_template(
                "auth/login.html",
                error="Email and password are required.",
                next_path=next_path,
            ),
            400,
        )

    user = auth_service.verify_credentials(email, password)
    if not user:
        return (
            render_template(
                "auth/login.html",
                error="Invalid email or password.",
                next_path=next_path,
            ),
            401,
        )

    session["user"] = user

    # Redirect priority: provided next_path -> role dashboard -> home
    if next_path and next_path.startswith("/"):
        return redirect(next_path)

    role_target = {
        "Admin": "admin.dashboard",
        "HOD": "hod.dashboard",
        "Faculty": "faculty.dashboard",
        "Student": "student.dashboard",
    }.get(user.get("role"))

    if role_target:
        return redirect(url_for(role_target))

    return redirect(url_for("auth.home"))


@bp.post("/logout")
def logout():
    session.pop("user", None)
    session.clear()
    return redirect(url_for("auth.home"))
