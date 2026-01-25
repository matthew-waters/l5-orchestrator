from fastapi import APIRouter, Depends

from orchestrator.api.deps import get_api_key
from orchestrator.api.schemas.clients import (
    ClientAwsConfigRequest,
    ClientAwsConfigResponse,
    ClientCreateRequest,
    ClientCreateResponse,
)

router = APIRouter(tags=["clients"])


@router.post("/clients", response_model=ClientCreateResponse)
def create_client(payload: ClientCreateRequest) -> ClientCreateResponse:
    return ClientCreateResponse(id="client_stub", api_key="replace_me", status="active")


@router.put("/clients/{client_id}/aws", response_model=ClientAwsConfigResponse)
def upsert_client_aws_config(
    client_id: str,
    payload: ClientAwsConfigRequest,
    api_key: str = Depends(get_api_key),
) -> ClientAwsConfigResponse:
    return ClientAwsConfigResponse(
        client_id=client_id,
        role_arn=payload.role_arn,
        external_id=payload.external_id,
        region_default=payload.region_default,
        session_name_template=payload.session_name_template,
    )
