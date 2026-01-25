from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from orchestrator.models.base import Base, TimestampMixin


class AppArtifact(Base, TimestampMixin):
    __tablename__ = "app_artifacts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    client_id: Mapped[str] = mapped_column(String, nullable=False)
    s3_uri: Mapped[str] = mapped_column(Text, nullable=False)
    sha256: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str | None] = mapped_column(String, nullable=True)
    metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
