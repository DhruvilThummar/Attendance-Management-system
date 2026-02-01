from __future__ import annotations

from flask import render_template

from . import api

@api.get("/login")
def login():
    return render_template("login.html")
