"""Admin-specific routes."""
from __future__ import annotations

from flask import Blueprint, jsonify

from ..app import role_required

bp = Blueprint("admin", __name__)


@bp.get("/")
@role_required("Admin")
def dashboard():
    return jsonify(message="admin dashboard placeholder"), 501
