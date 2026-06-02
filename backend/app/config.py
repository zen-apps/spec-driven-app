"""Backend configuration.

Settings are read from environment variables with defaults that match
`examples/create_agent.ipynb`, so the same code runs against the notebook's GCP
project locally and inside docker-compose later (Phase 3). Nothing here is
hardcoded into the agent module.

No new dependency is introduced — this is a small, typed settings object built
from the standard library only.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Typed view of the backend's runtime configuration."""

    # Gemini model name (notebook default: gemini-3.5-flash).
    gemini_model: str
    # GCP project that hosts the Gemini model.
    gcp_project: str
    # GCP location/region for the model ("global" in the notebook).
    gcp_location: str
    # Sampling temperature for the LLM (notebook uses 1.0).
    temperature: float
    # Path to the service-account JSON. Lives in the gitignored ./credentials
    # dir and is mounted at runtime; never committed, never logged.
    google_application_credentials: str | None


def get_settings() -> Settings:
    """Build Settings from the environment, applying notebook-matching defaults."""
    return Settings(
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
        gcp_project=os.getenv("GCP_PROJECT", "zen-general-377713"),
        gcp_location=os.getenv("GCP_LOCATION", "global"),
        temperature=float(os.getenv("GEMINI_TEMPERATURE", "1.0")),
        # Standard Google SDK env var; the backend reads the file path only and
        # never echoes its contents.
        google_application_credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    )
