"""Tenant API schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TenantCreate(BaseModel):
    name: str
    api_key_hash: str


class TenantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tenant_id: int
    name: str
    api_key_hash: str
    created_at: datetime
