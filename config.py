"""Print agent configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


def get_required_env(name: str) -> str:
    """Return a required environment variable."""
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required configuration '{name}' is missing "
            f"from {ENV_FILE}"
        )

    return value


PRINTER_NAME = get_required_env("PRINTER_NAME")
HOST = get_required_env("AGENT_HOST")
PORT = int(get_required_env("AGENT_PORT"))