"""AWS link model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.db.base import Base


class AwsLink(Base):
    __tablename__ = "aws_links"

    aws_link_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tenants.tenant_id"), nullable=False, index=True
    )
    role_arn: Mapped[str] = mapped_column(String(512), nullable=False)
    input_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    output_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    logs_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    stack_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    last_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="aws_links")
