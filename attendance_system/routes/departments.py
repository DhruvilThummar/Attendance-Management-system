from __future__ import annotations

from flask import render_template

from . import api

@api.get("/departments")
def departments():
    return render_template("departments.html")