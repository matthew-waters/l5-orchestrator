class StsClient:
    def assume_role(self, role_arn: str, external_id: str | None, duration_seconds: int):
        raise NotImplementedError
