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
    _pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, dsn)
    logger.info("DB pool initialized")


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
        raise RuntimeError("Database pool not initialized")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or [])
            if cur.description:
                rows = cur.fetchall()
            else:
                rows = []
            conn.commit()
            return rows
