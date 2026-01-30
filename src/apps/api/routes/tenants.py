"""Tenant routes."""

from __future__ import annotations

import hashlib

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from src.adapters.db.session import get_db
from src.apps.api.schemas.tenants import TenantMe
from src.domain.tenancy.service import TenantService

router = APIRouter(tags=["auth"])


@router.get("/me", response_model=TenantMe)
def get_me(
    api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> TenantMe:
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    api_key_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
    service = TenantService(db)
    tenant = service.get_by_api_key_hash(api_key_hash)
    if tenant is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return tenant


