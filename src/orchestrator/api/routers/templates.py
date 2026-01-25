from fastapi import APIRouter, Depends

from orchestrator.api.deps import get_api_key
from orchestrator.api.schemas.templates import JobTemplateCreateRequest, JobTemplateResponse

router = APIRouter(tags=["templates"])


@router.post("/job-templates", response_model=JobTemplateResponse)
def create_job_template(
    payload: JobTemplateCreateRequest,
    api_key: str = Depends(get_api_key),
) -> JobTemplateResponse:
    return JobTemplateResponse(
        id="template_stub",
        name=payload.name,
        app_artifact_id=payload.app_artifact_id,
        data_uri=payload.data_uri,
        fleet_template_id=payload.fleet_template_id,
    )
