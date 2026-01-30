"""Create a tenant and one-time API key."""

from __future__ import annotations

import argparse
import hashlib
import secrets

from sqlalchemy.orm import Session

from src.adapters.db.session import SessionLocal, create_engine_from_env
from src.domain.tenancy.service import TenantService


def _create_session() -> Session:
    engine = create_engine_from_env()
    SessionLocal.configure(bind=engine)
    return SessionLocal()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a tenant entry.")
    parser.add_argument("name", help="Tenant name")
    args = parser.parse_args()

    api_key = secrets.token_hex(32)
    api_key_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    session = _create_session()
    try:
        service = TenantService(session)
        tenant = service.create(name=args.name, api_key_hash=api_key_hash)
    finally:
        session.close()

    print(f"Tenant created: tenant_id={tenant.tenant_id}")
    print("API key (store securely, shown once):")
    print(api_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
