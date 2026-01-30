"""S3 client adapter."""

from __future__ import annotations

import boto3


def get_s3_client():
    return boto3.client("s3")
