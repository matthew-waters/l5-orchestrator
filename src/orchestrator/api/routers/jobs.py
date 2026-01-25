from fastapi import APIRouter, Depends

from orchestrator.api.deps import get_api_key
from orchestrator.api.schemas.common import JobState
from orchestrator.api.schemas.jobs import JobRequestCreate, JobRequestResponse

router = APIRouter(tags=["jobs"])


@router.post("/jobs", response_model=JobRequestResponse)
def create_job_request(
    payload: JobRequestCreate,
    api_key: str = Depends(get_api_key),
) -> JobRequestResponse:
    return JobRequestResponse(job_id="job_stub", state=JobState.planned)


@router.post("/jobs/{job_id}/cancel", response_model=JobRequestResponse)
def cancel_job(job_id: str, api_key: str = Depends(get_api_key)) -> JobRequestResponse:
    return JobRequestResponse(job_id=job_id, state=JobState.cancelled)
