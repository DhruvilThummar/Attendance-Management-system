"""Notifications and search stubs for frontend navigation."""

from __future__ import annotations

from flask import request, jsonify

from . import api


@api.route("/notifications/recent", methods=["GET"])
def recent_notifications():
    """Return recent notifications (empty stub)."""
    return jsonify({"unread": 0, "notifications": []})


@api.route("/notifications/<int:notification_id>/read", methods=["POST"])
def mark_notification_read(notification_id: int):
    """Mark a notification as read (no-op stub)."""
    return jsonify({"success": True, "notification_id": notification_id})


@api.route("/search", methods=["GET"])
def search():
    """Search endpoint stub."""
    query = request.args.get("q", "")
    return jsonify({"query": query, "results": []})