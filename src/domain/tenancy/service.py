"""Tenant service layer."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from src.adapters.db.models import Tenant
from src.adapters.db.repositories.tenant_repo import TenantRepository


class TenantService:
    def __init__(self, session: Session) -> None:
        self.repo = TenantRepository(session)

    def get_by_id(self, tenant_id: int) -> Tenant | None:
        return self.repo.get_by_id(tenant_id)

    def get_by_api_key_hash(self, api_key_hash: str) -> Tenant | None:
        return self.repo.get_by_api_key_hash(api_key_hash)

    def list(self) -> Iterable[Tenant]:
        return self.repo.list()

    def create(self, name: str, api_key_hash: str) -> Tenant:
        if not name:
            raise ValueError("name is required")
        if not api_key_hash:
            raise ValueError("api_key_hash is required")
        return self.repo.create(name=name, api_key_hash=api_key_hash)
