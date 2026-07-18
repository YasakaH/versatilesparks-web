"""Centralized configuration from environment variables."""

import os

HEADLESS = os.environ.get("HEADLESS", "false").lower() == "true"
TIMEOUT = int(os.environ.get("TIMEOUT", "30"))
CDP_PORT = int(os.environ.get("CDP_PORT", "9222"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
