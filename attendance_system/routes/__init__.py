"""Route blueprints - Organized by domain."""

from __future__ import annotations

from flask import Blueprint

# API Blueprint for REST endpoints
api = Blueprint("api", __name__)

# Register core page blueprints
from .core import core
from .dashboard import dashboard
from .academic import academic
from .pages import attendance

# Import API route modules
from . import login
from . import registration
from . import reports
from . import departments

__all__ = ["api", "core", "dashboard", "academic", "attendance"]
