from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from orchestrator.models.base import Base, TimestampMixin


class JobTemplate(Base, TimestampMixin):
    __tablename__ = "job_templates"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    client_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    app_artifact_id: Mapped[str] = mapped_column(String, nullable=False)
    default_args: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    data_uri: Mapped[str] = mapped_column(Text, nullable=False)
    fleet_template_id: Mapped[str] = mapped_column(String, nullable=False)
