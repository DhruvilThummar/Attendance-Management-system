"""Database connection helpers using psycopg2."""
from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any, Iterable

import psycopg2
import psycopg2.pool

logger = logging.getLogger(__name__)

_pool: psycopg2.pool.SimpleConnectionPool | None = None


def init_db_pool(dsn: str, minconn: int = 1, maxconn: int = 5) -> None:
    global _pool
    if _pool:
        return
    try:
        _pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, dsn)
        # Quick connectivity check so we fail fast with a clear error
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        logger.info("DB pool initialized")
    except Exception as exc:  # surface the real reason (bad URL, bad creds, SSL, etc.)
        logger.error("Failed to initialize DB pool: %s", exc)
        _pool = None
        raise


def close_pool() -> None:
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None


@contextmanager
def get_conn():
    if not _pool:
        raise RuntimeError("Database pool not initialized")
    conn = _pool.getconn()
    try:
        yield conn
    finally:
        _pool.putconn(conn)


def execute(query: str, params: Iterable[Any] | None = None) -> list[tuple[Any, ...]]:
    if not _pool:
        logger.warning("Database pool not initialized; returning empty result")
        return []
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or [])
            if cur.description:
                rows = cur.fetchall()
            else:
                rows = []
            conn.commit()
            return rows
