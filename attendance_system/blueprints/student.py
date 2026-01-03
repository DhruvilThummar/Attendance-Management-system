"""Student routes."""
from __future__ import annotations

from flask import Blueprint, jsonify

from ..app import role_required

bp = Blueprint("student", __name__)


@bp.get("/")
@role_required("Student")
def dashboard():
    return jsonify(message="student dashboard placeholder"), 501
