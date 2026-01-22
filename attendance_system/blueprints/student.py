"""Student routes."""
from __future__ import annotations

from flask import Blueprint, render_template

from ..app import role_required

bp = Blueprint("student", __name__)


@bp.get("/")
@role_required("Student")
def dashboard():
    return render_template("student/dashboard.html")
