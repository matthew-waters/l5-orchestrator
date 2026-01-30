"""Artifact API schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ArtifactRead(BaseModel):
    artifact_id: int
    artifact_hash: str
    s3_uri: str
    created_at: datetime
