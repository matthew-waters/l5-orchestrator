"""Rescheduling step stub."""

from __future__ import annotations

import logging

from src.domain.planning.plan_snapshots import capture_plan_snapshots

logger = logging.getLogger(__name__)


def reschedule_occurrences() -> None:
    logger.info("Rescheduling step stub")
    capture_plan_snapshots()
