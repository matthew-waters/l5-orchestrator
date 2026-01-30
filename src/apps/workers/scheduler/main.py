"""Periodic scheduler worker entrypoint."""

from __future__ import annotations

import logging
import os
import signal
from threading import Event

from dotenv import load_dotenv

from src.domain.tasks.planning.occurrence_generation import OccurrenceGenerationTask
from src.domain.tasks.planning.tasks import PlanningTask
from src.domain.scheduler.engine import SchedulerEngine


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    tick_seconds = _get_int("SCHEDULER_TICK_SECONDS", 30)
    occurrence_interval = _get_int("OCCURRENCE_GEN_INTERVAL_SECONDS", 1800)
    planning_interval = _get_int("PLANNING_INTERVAL_SECONDS", 1800)

    tasks = [
        OccurrenceGenerationTask(interval_seconds=occurrence_interval),
        PlanningTask(interval_seconds=planning_interval),
    ]

    stop_event = Event()

    def _handle_signal(_: int, __: object) -> None:
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    SchedulerEngine(tasks=tasks, tick_seconds=tick_seconds).run_forever(stop_event)


if __name__ == "__main__":
    main()
