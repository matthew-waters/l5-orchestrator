class S3Client:
    def upload_bytes(self, bucket: str, key: str, payload: bytes):
        raise NotImplementedError
