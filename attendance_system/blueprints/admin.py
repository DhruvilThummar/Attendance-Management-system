"""Admin-specific routes."""
from __future__ import annotations

from flask import Blueprint, render_template

from ..app import role_required

bp = Blueprint("admin", __name__)


@bp.get("/")
@role_required("Admin")
def dashboard():
    return render_template("admin/dashboard.html")
