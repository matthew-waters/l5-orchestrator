"""Simple DB connection check using env vars."""

from __future__ import annotations

import os
import sys

from sqlalchemy import text
from dotenv import load_dotenv

from src.adapters.db.engine import create_mysql_engine


def _get_env(name: str, required: bool = True) -> str | None:
    value = os.getenv(name)
    if required and not value:
        print(f"Missing required env var: {name}", file=sys.stderr)
        return None
    return value


def main() -> int:
    load_dotenv()
    host = _get_env("DB_HOST")
    port = os.getenv("DB_PORT") or "3306"
    name = _get_env("DB_NAME")
    user = _get_env("DB_USER")
    password = _get_env("DB_PASSWORD")

    if not all([host, name, user, password]):
        print("Set DB_HOST, DB_NAME, DB_USER, DB_PASSWORD.", file=sys.stderr)
        return 1

    database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"
    engine = create_mysql_engine(database_url)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("DB connection OK")
        return 0
    except Exception as exc:  # pragma: no cover
        print(f"DB connection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
