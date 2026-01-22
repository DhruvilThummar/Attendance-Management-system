"""HOD routes."""
from __future__ import annotations

from flask import Blueprint, render_template

from ..app import role_required

bp = Blueprint("hod", __name__)


@bp.get("/")
@role_required("HOD")
def dashboard():
    return render_template("hod/dashboard.html")
