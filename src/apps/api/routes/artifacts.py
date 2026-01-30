"""Artifact routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from src.apps.api.auth import get_current_tenant
from src.apps.api.schemas.artifacts import ArtifactRead
from src.domain.services.artifact_service import ArtifactService

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.post("", response_model=ArtifactRead, status_code=201)
def upload_artifact(
    file: UploadFile = File(...),
    tenant=Depends(get_current_tenant),
    service: ArtifactService = Depends(ArtifactService),
) -> ArtifactRead:
    try:
        return service.upload(tenant_id=tenant.tenant_id, file=file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
