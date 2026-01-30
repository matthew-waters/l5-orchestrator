"""Always-on executor worker entrypoint."""

from __future__ import annotations

import logging
import os
import signal
from threading import Event

from dotenv import load_dotenv


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    poll_seconds = _get_int("EXECUTOR_POLL_SECONDS", 15)
    stop_event = Event()

    def _handle_signal(_: int, __: object) -> None:
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    logging.info("Executor worker starting with poll=%ss", poll_seconds)
    while not stop_event.is_set():
        logging.info("Executor poll stub")
        stop_event.wait(poll_seconds)
    logging.info("Executor worker stopping")


if __name__ == "__main__":
    main()
