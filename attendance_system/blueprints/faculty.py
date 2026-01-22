"""Faculty routes."""
from __future__ import annotations

from flask import Blueprint, render_template

from ..app import role_required

bp = Blueprint("faculty", __name__)


@bp.get("/")
@role_required("Faculty")
def dashboard():
    return render_template("faculty/dashboard.html")
