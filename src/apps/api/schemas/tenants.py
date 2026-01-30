"""Tenant API schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TenantMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tenant_id: int
    name: str
    created_at: datetime
