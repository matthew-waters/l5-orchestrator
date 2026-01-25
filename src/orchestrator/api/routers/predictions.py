from fastapi import APIRouter, Depends

from orchestrator.api.deps import get_api_key
from orchestrator.api.schemas.predictions import RuntimePredictionResponse

router = APIRouter(tags=["predictions"])


@router.get("/predictions/runtime", response_model=RuntimePredictionResponse)
def get_runtime_prediction(
    job_template_id: str,
    fleet_template_id: str,
    api_key: str = Depends(get_api_key),
) -> RuntimePredictionResponse:
    return RuntimePredictionResponse(
        available=False,
        notes="insufficient history",
    )
