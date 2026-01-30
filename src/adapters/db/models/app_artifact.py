"""App artifact model."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base


class AppArtifact(Base):
    __tablename__ = "app_artifacts"

    artifact_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tenants.tenant_id"), nullable=False, index=True
    )
    artifact_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    s3_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="app_artifacts")
    workloads: Mapped[List["Workload"]] = relationship(
        "Workload", back_populates="artifact"
    )
    runs: Mapped[List["Run"]] = relationship(
        "Run", back_populates="artifact"
    )
