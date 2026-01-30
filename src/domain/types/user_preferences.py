"""User preference models."""

from __future__ import annotations

from pydantic import BaseModel


class UserPreferences(BaseModel):
    risk_mode: str
