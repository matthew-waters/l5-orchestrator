from datetime import datetime
from typing import Any

from pydantic import BaseModel

from orchestrator.api.schemas.common import JobState, JobType, RiskMode


class JobRequestCreate(BaseModel):
    job_template_id: str
    type: JobType
    intended_time: datetime | None = None
    earliest_start: datetime | None = None
    latest_finish: datetime | None = None
    risk_mode: RiskMode = RiskMode.neutral
    weights: dict[str, Any] | None = None


class JobRequestResponse(BaseModel):
    job_id: str
    state: JobState
