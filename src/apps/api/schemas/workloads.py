"""Workload API schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorkloadCreate(BaseModel):
    name: str
    description: str | None = None
    tags_json: list[str] | None = None
    artifact_id: int
    fleet_template_id: int
    schedule_rules_json: dict[str, Any]
    user_preferences_json: dict[str, Any]
    manual_runtime_seconds: int | None = None


class WorkloadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workload_id: int
    tenant_id: int
    name: str
    description: str | None
    tags_json: list[str] | None = None
    artifact_id: int
    fleet_template_id: int
    schedule_rules_json: dict[str, Any]
    user_preferences_json: dict[str, Any]
    manual_runtime_seconds: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class WorkloadList(BaseModel):
    items: list[WorkloadRead] = Field(default_factory=list)
