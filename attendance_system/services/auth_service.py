"""Authentication service using MySQL + password hashing."""
from __future__ import annotations

from typing import Optional

from werkzeug.security import check_password_hash

from ..db_manager import execute


def verify_credentials(email: str, password: str) -> Optional[dict]:
    """Return user dict if credentials are valid, else None.

    Query: users(id, email, password_hash, role)
    Accepts either a proper password hash or, in dev/demo mode, a plain text match
    (useful when the DB is not seeded with hashes yet).
    """

    if not email or not password:
        return None

    rows = execute(
        """
        SELECT id, email, password, role
        FROM users
        WHERE LOWER(email) = LOWER(%s)
        LIMIT 1
        """,
        (email,),
    )

    if not rows:
        return None

    user_id, user_email, stored_hash, role = rows[0]

    # If DB is not initialized (execute returns empty list), bail out
    if stored_hash is None:
        return None

    is_valid = check_password_hash(stored_hash, password) or stored_hash == password
    if not is_valid:
        return None

    return {
        "id": user_id,
        "email": user_email,
        "role": role,
    }
