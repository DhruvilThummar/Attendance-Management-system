"""Authentication service stub."""
from __future__ import annotations

from typing import Optional

from ..db_manager import execute


def verify_credentials(email: str, password: str) -> Optional[dict]:
    # TODO: hash password and compare with stored hash
    _ = execute  # placeholder to avoid lint complaints
    return None
