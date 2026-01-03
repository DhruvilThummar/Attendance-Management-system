"""Authentication endpoints."""
from __future__ import annotations

from flask import Blueprint, jsonify

bp = Blueprint("auth", __name__)


@bp.get("/")
def healthcheck():
    return jsonify(status="ok")


@bp.post("/login")
def login():
    return jsonify(message="login placeholder"), 501


@bp.post("/logout")
def logout():
    return jsonify(message="logout placeholder"), 501
