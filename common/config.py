"""Global defaults used throughout the cookbook.

Change these values to customize browser behavior across all recipes.
Individual recipes may override them when needed.
"""
from __future__ import annotations
from pathlib import Path

# Browser
HEADLESS: bool = False
USER_DATA_DIR: Path | None = None
BROWSER_LANGUAGE: str = "en-US"
WINDOW_SIZE: tuple[int, int] = (1280, 800)

# Files
DOWNLOAD_DIR: Path = Path("downloads")

# Waiting
DEFAULT_TIMEOUT: int = 30
