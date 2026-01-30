"""Artifact service."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

from src.adapters.db.models import AppArtifact
from src.adapters.db.repositories.artifact_repo import ArtifactRepository
from src.adapters.db.session import get_db
from src.adapters.s3.client import get_s3_client


@dataclass
class ArtifactUploadResult:
    artifact_id: int
    artifact_hash: str
    s3_uri: str
    created_at: datetime


class ArtifactService:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.repo = ArtifactRepository(session)
        self.s3 = get_s3_client()

    def list(self, tenant_id: int) -> Iterable[AppArtifact]:
        return self.repo.list_by_tenant(tenant_id)

    def upload(
        self,
        *,
        tenant_id: int,
        file: UploadFile,
    ) -> ArtifactUploadResult:
        data = file.file.read()
        artifact_hash = hashlib.sha256(data).hexdigest()

        self._validate_artifact_stub(data)

        bucket = os.getenv("ARTIFACTS_BUCKET")
        if not bucket:
            raise ValueError("ARTIFACTS_BUCKET is not configured")

        key = f"tenants/{tenant_id}/artifacts/{artifact_hash}/app.zip"
        self.s3.put_object(Bucket=bucket, Key=key, Body=data)
        s3_uri = f"s3://{bucket}/{key}"

        artifact = AppArtifact(
            tenant_id=tenant_id,
            artifact_hash=artifact_hash,
            s3_uri=s3_uri,
        )
        artifact = self.repo.create(artifact)
        return ArtifactUploadResult(
            artifact_id=artifact.artifact_id,
            artifact_hash=artifact_hash,
            s3_uri=s3_uri,
            created_at=artifact.created_at,
        )

    def _validate_artifact_stub(self, _data: bytes) -> None:
        return
