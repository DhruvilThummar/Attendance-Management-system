from __future__ import annotations

from flask import render_template

from . import api

@api.get("/reports")
def reports():
    return render_template("reports.html")