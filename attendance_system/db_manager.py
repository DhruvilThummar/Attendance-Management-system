"""MySQL database helpers (mysql-connector-python).

The project uses a DATABASE_URL of the form:
  mysql://user:password@host:port/dbname

This module intentionally keeps a small surface area:
- create_connection(): open a new connection
- execute()/fetch_one()/fetch_all(): run queries with %s placeholders
- run_sql_script(): execute schema.sql (multi-statement)

Note: For simplicity this uses a short-lived connection per call.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import urlparse

import os
import mysql.connector


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


def _parse_database_url(database_url: str) -> DbConfig:
    parsed = urlparse(database_url)
    if parsed.scheme not in {"mysql"}:
        raise ValueError("DATABASE_URL must start with mysql://")

    database = (parsed.path or "").lstrip("/")
    if not database:
        raise ValueError("DATABASE_URL must include a database name")

    return DbConfig(
        host=parsed.hostname or "localhost",
        port=parsed.port or 3306,
        user=parsed.username or "root",
        password=parsed.password or "",
        database=database,
    )


def create_connection(dsn: str | None = None):
    database_url = dsn or os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    cfg = _parse_database_url(database_url)
    return mysql.connector.connect(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
        database=cfg.database,
    )


@contextmanager
def get_cursor(dsn: str | None = None):
    conn = create_connection(dsn)
    cur = conn.cursor()
    try:
        yield conn, cur
        conn.commit()
    finally:
        try:
            cur.close()
        finally:
            conn.close()


def execute(query: str, params: Iterable[Any] | None = None, dsn: str | None = None) -> None:
    with get_cursor(dsn) as (_, cur):
        cur.execute(query, tuple(params) if params else None)


def fetch_all(query: str, params: Iterable[Any] | None = None, dsn: str | None = None) -> list[tuple[Any, ...]]:
    with get_cursor(dsn) as (_, cur):
        cur.execute(query, tuple(params) if params else None)
        return list(cur.fetchall())


def fetch_one(query: str, params: Iterable[Any] | None = None, dsn: str | None = None) -> tuple[Any, ...] | None:
    rows = fetch_all(query, params=params, dsn=dsn)
    return rows[0] if rows else None


def init_db_pool(dsn: str = "") -> None:
    """Legacy-compatible connectivity check."""

    conn = create_connection(dsn or None)
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        _ = cur.fetchone()
    finally:
        try:
            cur.close()
        finally:
            conn.close()


def run_sql_script(sql_text: str, dsn: str | None = None) -> None:
    """Run a SQL script containing multiple statements."""

    with get_cursor(dsn) as (_, cur):
        # mysql-connector supports multi-statement execution via multi=True
        for _ in cur.execute(sql_text, multi=True):
            pass


def run_sql_file(path: str, dsn: str | None = None) -> None:
    with open(path, "r", encoding="utf-8") as f:
        run_sql_script(f.read(), dsn=dsn)
