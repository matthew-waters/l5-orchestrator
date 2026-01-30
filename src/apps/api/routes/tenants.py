"""Tenant routes."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.adapters.db.session import get_db
from src.apps.api.schemas.tenants import TenantCreate, TenantRead
from src.domain.tenancy.service import TenantService

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("", response_model=List[TenantRead])
def list_tenants(db: Session = Depends(get_db)) -> List[TenantRead]:
    service = TenantService(db)
    return list(service.list())


@router.get("/{tenant_id}", response_model=TenantRead)
def get_tenant(tenant_id: int, db: Session = Depends(get_db)) -> TenantRead:
    service = TenantService(db)
    tenant = service.get_by_id(tenant_id)
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return tenant


@router.get("/by-key/{api_key_hash}", response_model=TenantRead)
def get_tenant_by_key(
    api_key_hash: str, db: Session = Depends(get_db)
) -> TenantRead:
    service = TenantService(db)
    tenant = service.get_by_api_key_hash(api_key_hash)
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return tenant


@router.post("", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
def create_tenant(
    payload: TenantCreate, db: Session = Depends(get_db)
) -> TenantRead:
    service = TenantService(db)
    return service.create(name=payload.name, api_key_hash=payload.api_key_hash)
