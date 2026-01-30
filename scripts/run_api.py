"""Run the FastAPI application with Uvicorn."""

from __future__ import annotations

import os

from dotenv import load_dotenv
import uvicorn


def main() -> None:
    load_dotenv()

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() in {"1", "true", "yes", "y"}

    uvicorn.run(
        "src.apps.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
