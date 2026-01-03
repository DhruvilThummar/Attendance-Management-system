"""Basic smoke test."""
from attendance_system.app import create_app


def test_app_factory():
    app = create_app({"TESTING": True, "SECRET_KEY": "test"})
    assert app.config["TESTING"] is True
