"""Tenant routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.apps.api.auth import get_current_tenant
from src.apps.api.schemas.tenants import TenantMe
from src.adapters.db.models import Tenant

router = APIRouter(tags=["auth"])


@router.get("/me", response_model=TenantMe)
def get_me(tenant: Tenant = Depends(get_current_tenant)) -> TenantMe:
    return tenant


