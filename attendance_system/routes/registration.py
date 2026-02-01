from __future__ import annotations

from flask import render_template

from . import api

@api.get("/registration")
def registration():
    return render_template("registration.html")