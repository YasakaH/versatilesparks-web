"""Browser lifecycle utilities."""

import asyncio
import nodriver as uc
from common.config import HEADLESS, CDP_PORT, logger


async def launch_browser(**kwargs):
    """Launch a Chrome browser instance."""
    options = {
        "headless": HEADLESS,
    }
    options.update(kwargs)
    if options.get("user_data_dir"):
        user_data_dir = options.pop("user_data_dir")
        browser = await uc.start(user_data_dir=user_data_dir, **options)
    else:
        browser = await uc.start(**options)
    logger.info("Browser launched")
    return browser


async def close_browser(browser):
    """Close the browser instance."""
    try:
        browser.stop()
        logger.info("Browser closed")
    except Exception:
        pass
