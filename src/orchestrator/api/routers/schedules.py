from datetime import timedelta

from fastapi import APIRouter, Depends

from orchestrator.api.deps import get_api_key
from orchestrator.api.schemas.schedules import (
    ScheduleCandidate,
    SchedulePreviewRequest,
    SchedulePreviewResponse,
)

router = APIRouter(tags=["schedules"])


@router.post("/schedules/preview", response_model=SchedulePreviewResponse)
def preview_schedule(
    payload: SchedulePreviewRequest,
    api_key: str = Depends(get_api_key),
) -> SchedulePreviewResponse:
    candidate = ScheduleCandidate(
        proposed_start=payload.earliest_start,
        estimated_finish_p50=payload.earliest_start + timedelta(hours=1),
        estimated_finish_p90=payload.earliest_start + timedelta(hours=2),
        scores={"carbon": 0.0, "risk": 0.0, "slack": 1.0},
    )
    return SchedulePreviewResponse(candidates=[candidate], chosen=candidate, rationale="stub")
