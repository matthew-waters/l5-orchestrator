from datetime import datetime

from pydantic import BaseModel

from orchestrator.api.schemas.common import RunStatus


class RunResponse(BaseModel):
    id: str
    job_request_id: str
    status: RunStatus
    started_at: datetime | None = None
    ended_at: datetime | None = None
    logs_uri: str | None = None
