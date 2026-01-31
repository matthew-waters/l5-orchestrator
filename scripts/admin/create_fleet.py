"""Create a fleet entry."""

from __future__ import annotations

import argparse
import json

from sqlalchemy.orm import Session

from src.adapters.db.models import Fleet
from src.adapters.db.repositories.fleet_repo import FleetRepository
from src.adapters.db.session import SessionLocal, create_engine_from_env


def _create_session() -> Session:
    engine = create_engine_from_env()
    SessionLocal.configure(bind=engine)
    return SessionLocal()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a fleet entry.")
    parser.add_argument("name", help="Fleet name")
    parser.add_argument("config_json", help="Fleet config JSON string")
    parser.add_argument("--description", default=None, help="Optional description")
    args = parser.parse_args()

    try:
        config = json.loads(args.config_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid config_json: {exc}") from exc

    session = _create_session()
    try:
        repo = FleetRepository(session)
        fleet = repo.create(
            Fleet(
                name=args.name,
                description=args.description,
                config_json=config,
            )
        )
    finally:
        session.close()

    print(f"Fleet created: fleet_template_id={fleet.fleet_template_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
