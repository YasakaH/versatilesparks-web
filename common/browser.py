"""browser.py — Launch and close a nodriver browser consistently."""
from __future__ import annotations

from pathlib import Path

import nodriver as uc

from .config import HEADLESS, USER_DATA_DIR
from .logging import logger


async def launch_browser(
    *,
    headless: bool | None = None,
    user_data_dir: str | Path | None = None,
):
    """Launch a nodriver browser using the cookbook defaults.

    Parameters
    ----------
    headless:
        Override the default HEADLESS setting.
    user_data_dir:
        Override the default browser profile directory.

    Returns
    -------
    Browser
        Running nodriver browser instance.

    Raises
    ------
    RuntimeError
        If the browser could not be started.
    """
    headless = HEADLESS if headless is None else headless
    user_data_dir = USER_DATA_DIR if user_data_dir is None else Path(user_data_dir)

    logger.debug("Starting browser")

    try:
        browser = await uc.start(
            headless=headless,
            user_data_dir=user_data_dir,
        )
    except Exception as exc:
        raise RuntimeError(
            "Failed to start Chrome. Verify Chrome/Chromium is installed, "
            "supported, and that nodriver is installed correctly."
        ) from exc

    logger.debug("Browser started")
    return browser


async def close_browser(browser):
    """Close a running browser instance."""
    if browser is None:
        return

    logger.debug("Closing browser")
    browser.stop()
