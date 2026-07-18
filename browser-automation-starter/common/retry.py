"""Async retry with configurable backoff."""

import asyncio
from common.logging import logger


async def retry(fn, *args, exceptions=(TimeoutError,), max_retries=3, delay=2, **kwargs):
    """Retry a function on specific exceptions."""
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return await fn(*args, **kwargs)
        except exceptions as e:
            logger.warning(f"Attempt {attempt}/{max_retries} failed: {e}")
            last_error = e
            if attempt < max_retries:
                await asyncio.sleep(delay)
    logger.error(f"All {max_retries} attempts failed")
    raise last_error
