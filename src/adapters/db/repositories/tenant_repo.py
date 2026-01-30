"""Tenant repository."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from src.adapters.db.models import Tenant


class TenantRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, tenant_id: int) -> Tenant | None:
        return self.session.get(Tenant, tenant_id)

    def get_by_api_key_hash(self, api_key_hash: str) -> Tenant | None:
        return (
            self.session.query(Tenant)
            .filter(Tenant.api_key_hash == api_key_hash)
            .one_or_none()
        )

    def list(self) -> Iterable[Tenant]:
        return self.session.query(Tenant).order_by(Tenant.tenant_id).all()

    def create(self, name: str, api_key_hash: str) -> Tenant:
        tenant = Tenant(name=name, api_key_hash=api_key_hash)
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        return tenant
