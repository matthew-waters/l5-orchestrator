"""Schedule rule models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScheduleAnchor(BaseModel):
    cron: str
    timezone: str


class ScheduleDeadline(BaseModel):
    offset_seconds: int = Field(gt=0)


class ScheduleRules(BaseModel):
    anchor: ScheduleAnchor
    deadline: ScheduleDeadline
