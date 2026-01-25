from pydantic import BaseModel


class ClientCreateRequest(BaseModel):
    name: str


class ClientCreateResponse(BaseModel):
    id: str
    api_key: str
    status: str


class ClientAwsConfigRequest(BaseModel):
    role_arn: str
    external_id: str | None = None
    region_default: str | None = None
    session_name_template: str | None = None


class ClientAwsConfigResponse(BaseModel):
    client_id: str
    role_arn: str
    external_id: str | None = None
    region_default: str | None = None
    session_name_template: str | None = None
