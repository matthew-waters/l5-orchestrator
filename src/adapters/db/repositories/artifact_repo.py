"""Artifact repository."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from src.adapters.db.models import AppArtifact


class ArtifactRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, artifact: AppArtifact) -> AppArtifact:
        self.session.add(artifact)
        self.session.commit()
        self.session.refresh(artifact)
        return artifact

    def list_by_tenant(self, tenant_id: int) -> Iterable[AppArtifact]:
        return (
            self.session.query(AppArtifact)
            .filter(AppArtifact.tenant_id == tenant_id)
            .order_by(AppArtifact.artifact_id)
            .all()
        )
