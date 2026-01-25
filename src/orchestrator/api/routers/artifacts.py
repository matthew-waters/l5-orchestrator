from fastapi import APIRouter, Depends, File, UploadFile

from orchestrator.api.deps import get_api_key
from orchestrator.api.schemas.artifacts import ArtifactUploadResponse

router = APIRouter(tags=["artifacts"])


@router.post("/artifacts/upload", response_model=ArtifactUploadResponse)
def upload_artifact(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
) -> ArtifactUploadResponse:
    return ArtifactUploadResponse(
        artifact_id="artifact_stub",
        s3_uri="s3://orchestrator-artifacts/stub.zip",
        sha256="stub",
        version=None,
        metadata=None,
    )
