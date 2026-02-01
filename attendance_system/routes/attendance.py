from __future__ import annotations

from flask import render_template

from . import api

@api.get("/attendance")
def attendance():
    return render_template("attendance.html")