"""Artifact repository."""

from __future__ import annotations

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
