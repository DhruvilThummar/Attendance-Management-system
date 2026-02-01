from __future__ import annotations

from flask import jsonify

from . import api


@api.get("/health")
def health():
    return jsonify({"status": "ok"})
