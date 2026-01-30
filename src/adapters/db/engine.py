"""SQLAlchemy engine helpers."""

from __future__ import annotations

from sqlalchemy import Engine, create_engine


def create_mysql_engine(database_url: str) -> Engine:
    """Create a SQLAlchemy engine for MySQL."""
    return create_engine(database_url, pool_pre_ping=True)
