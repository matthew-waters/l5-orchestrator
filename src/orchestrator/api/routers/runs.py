from fastapi import APIRouter, Depends

from orchestrator.api.deps import get_api_key
from orchestrator.api.schemas.common import RunStatus
from orchestrator.api.schemas.runs import RunResponse

router = APIRouter(tags=["runs"])


@router.get("/runs/{run_id}", response_model=RunResponse)
def get_run(run_id: str, api_key: str = Depends(get_api_key)) -> RunResponse:
    return RunResponse(id=run_id, job_request_id="job_stub", status=RunStatus.running)


@router.post("/runs/{run_id}/cancel", response_model=RunResponse)
def cancel_run(run_id: str, api_key: str = Depends(get_api_key)) -> RunResponse:
    return RunResponse(id=run_id, job_request_id="job_stub", status=RunStatus.cancelled)
