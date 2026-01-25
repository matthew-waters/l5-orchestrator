from datetime import datetime
from typing import Any

from pydantic import BaseModel

from orchestrator.api.schemas.common import RiskMode


class SchedulePreviewRequest(BaseModel):
    job_template_id: str
    fleet_template_id: str
    earliest_start: datetime
    latest_finish: datetime
    risk_mode: RiskMode = RiskMode.neutral
    weights: dict[str, Any] | None = None


class ScheduleCandidate(BaseModel):
    proposed_start: datetime
    estimated_finish_p50: datetime
    estimated_finish_p90: datetime
    scores: dict[str, float]


class SchedulePreviewResponse(BaseModel):
    candidates: list[ScheduleCandidate]
    chosen: ScheduleCandidate | None = None
    rationale: str | None = None
