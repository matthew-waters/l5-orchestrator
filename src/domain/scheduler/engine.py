"""Scheduler engine for periodic tasks."""

from __future__ import annotations

import logging
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from threading import Event

from src.domain.scheduler.task import ScheduledTask

logger = logging.getLogger(__name__)


@dataclass
class SchedulerEngine:
    tasks: Iterable[ScheduledTask]
    tick_seconds: int = 30
    _last_run: dict[str, float] = field(default_factory=dict, init=False)

    def run_forever(self, stop_event: Event) -> None:
        logger.info("Scheduler starting with tick=%ss", self.tick_seconds)
        while not stop_event.is_set():
            now = time.monotonic()
            for task in self.tasks:
                last_run = self._last_run.get(task.name, 0.0)
                if now - last_run < task.interval_seconds:
                    continue

                logger.info("Running task: %s", task.name)
                try:
                    task.run()
                except Exception:  # pragma: no cover
                    logger.exception("Task failed: %s", task.name)
                finally:
                    self._last_run[task.name] = time.monotonic()

            stop_event.wait(self.tick_seconds)
        logger.info("Scheduler stopping")
