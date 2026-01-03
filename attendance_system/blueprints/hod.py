"""HOD routes."""
from __future__ import annotations

from flask import Blueprint, jsonify

from ..app import role_required

bp = Blueprint("hod", __name__)


@bp.get("/")
@role_required("HOD")
def dashboard():
    return jsonify(message="hod dashboard placeholder"), 501
