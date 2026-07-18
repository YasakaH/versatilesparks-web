import asyncio

from .logging import logger


async def retry(
    func,
    *args,
    exceptions,
    max_retries=3,
    delay=1,
    **kwargs,
):
    """Retry an async operation when one of the supplied exception types occurs.

    Parameters
    ----------
    func
        Async function to call.
    exceptions
        Tuple of retryable exception classes.
    max_retries
        Maximum number of attempts.
    delay
        Initial delay (seconds). Exponential backoff is applied.
    """
    for attempt in range(1, max_retries + 1):
        try:
            return await func(*args, **kwargs)

        except exceptions as exc:
            if attempt == max_retries:
                logger.error(
                    "Operation failed after %s attempts.",
                    max_retries,
                )
                raise

            wait = delay * (2 ** (attempt - 1))

            logger.warning(
                "Retry %s/%s after %s (%ss)",
                attempt + 1,
                max_retries,
                type(exc).__name__,
                wait,
            )

            await asyncio.sleep(wait)
