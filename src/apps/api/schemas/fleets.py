"""Fleet API schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FleetCreate(BaseModel):
    name: str
    description: str | None = None
    config_json: dict[str, Any]


class FleetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fleet_template_id: int
    name: str
    description: str | None
    config_json: dict[str, Any]
    created_at: datetime


class FleetList(BaseModel):
    items: list[FleetRead] = Field(default_factory=list)
