from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from orchestrator.models.base import Base, TimestampMixin


class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")
    api_key_hash: Mapped[str] = mapped_column(String, nullable=False)


class ClientAwsConfig(Base, TimestampMixin):
    __tablename__ = "client_aws_configs"

    client_id: Mapped[str] = mapped_column(String, primary_key=True)
    role_arn: Mapped[str] = mapped_column(Text, nullable=False)
    external_id: Mapped[str | None] = mapped_column(String, nullable=True)
    region_default: Mapped[str | None] = mapped_column(String, nullable=True)
    session_name_template: Mapped[str | None] = mapped_column(String, nullable=True)
