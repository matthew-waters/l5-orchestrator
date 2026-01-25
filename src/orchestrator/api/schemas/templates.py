from typing import Any

from pydantic import BaseModel


class JobTemplateCreateRequest(BaseModel):
    name: str
    app_artifact_id: str
    default_args: dict[str, Any] | None = None
    data_uri: str
    fleet_template_id: str


class JobTemplateResponse(BaseModel):
    id: str
    name: str
    app_artifact_id: str
    data_uri: str
    fleet_template_id: str
