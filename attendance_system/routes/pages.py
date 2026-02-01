"""Attendance routes - Attendance marking and tracking."""

from __future__ import annotations

from flask import Blueprint, render_template

attendance = Blueprint("attendance", __name__)


@attendance.get("/mark-attendance")
def mark_attendance():
    """Mark attendance page."""
    return render_template("attendance.html")


@attendance.get("/student-attendance")
def student_attendance():
    """Student attendance view page."""
    return render_template("student-attendance.html")
