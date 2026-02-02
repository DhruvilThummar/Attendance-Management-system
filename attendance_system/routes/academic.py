"""Academic management routes - Faculty, Students, Timetable, Subjects."""

from __future__ import annotations

from flask import Blueprint, render_template

academic = Blueprint("academic", __name__)


@academic.get("/faculty")
def faculties():
    """Faculty management page."""
    return render_template("faculty.html")


@academic.get("/students")
def students():
    """Students management page."""
    return render_template("students.html")


@academic.get("/timetable")
def timetable():
    """Timetable management page."""
    return render_template("timetable.html")


@academic.get("/subjects")
def subjects():
    """Subjects management page."""
    return render_template("subjects.html")


@academic.get("/divisions")
def divisions():
    """Divisions management page."""
    return render_template("divisions.html")


@academic.get("/departments")
def departments():
    """Departments management page."""
    return render_template("departments.html")
