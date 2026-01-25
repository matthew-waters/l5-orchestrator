from pydantic import BaseModel

from orchestrator.api.schemas.common import Metadata


class ArtifactUploadResponse(BaseModel):
    artifact_id: str
    s3_uri: str
    sha256: str
    version: str | None = None
    metadata: Metadata | None = None
