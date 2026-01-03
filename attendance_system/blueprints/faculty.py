"""Faculty routes."""
from __future__ import annotations

from flask import Blueprint, jsonify

from ..app import role_required

bp = Blueprint("faculty", __name__)


@bp.get("/")
@role_required("Faculty")
def dashboard():
    return jsonify(message="faculty dashboard placeholder"), 501
