"""Occurrence generation step stub."""

from __future__ import annotations

import logging

from src.adapters.db.models import Occurrence

logger = logging.getLogger(__name__)


def generate_occurrences(workload) -> list[Occurrence]:
    logger.info("Occurrence generation stub for workload_id=%s", workload.workload_id)
    return []
