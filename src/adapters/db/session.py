"""SQLAlchemy session helpers."""

from __future__ import annotations

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.adapters.db.engine import create_mysql_engine


def build_database_url() -> str:
    load_dotenv()

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT") or "3306"
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    missing = [key for key, value in [
        ("DB_HOST", host),
        ("DB_NAME", name),
        ("DB_USER", user),
        ("DB_PASSWORD", password),
    ] if not value]
    if missing:
        raise RuntimeError(f"Missing DB env vars: {', '.join(missing)}")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


def create_engine_from_env() -> Engine:
    return create_mysql_engine(build_database_url())


SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    engine = create_engine_from_env()
    SessionLocal.configure(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
