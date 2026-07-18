"""
network_queue.py — CDP Handler with asyncio.Queue

Production pattern for handling high-volume CDP network events
without blocking the event loop or dropping events silently.

Architecture:
  Chrome → CDP Event → asyncio.Queue → Worker → Storage

The handler is intentionally lightweight (just queues data).
The worker processes events sequentially, protecting the
event loop from overload during high-traffic page loads.

Usage:
    from common.network_queue import NetworkMonitor

    monitor = NetworkMonitor(max_queue_size=5000)
    await monitor.setup()
    # browser.add_handler(uc.cdp.network.RequestWillBeSent,
    #                     monitor.request_handler)
    # ... run automation ...
    await monitor.cleanup()
"""
import asyncio
import logging

logger = logging.getLogger(__name__)


class NetworkMonitor:
    """Observe network traffic without freezing the event loop.

    Queues CDP events in an asyncio.Queue and processes them
    in a background worker. Drops oldest events when overloaded
    to prevent unbounded memory growth.
    """

    def __init__(self, max_queue_size: int = 5000):
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.worker_task: asyncio.Task | None = None
        self.running = False
        self._dropped_count = 0

    async def setup(self):
        """Start the background worker task."""
        self.running = True
        self.worker_task = asyncio.create_task(self._worker())
        logger.info("NetworkMonitor worker started (queue=%d)", self.queue.maxsize)

    async def request_handler(self, event):
        """CDP event callback — must complete instantly.

        Called by nodriver's add_handler for each RequestWillBeSent event.
        Only queues the data; does no I/O or heavy processing.
        """
        data = {
            "url": event.request.url,
            "method": event.request.method,
            "type": event.type if hasattr(event, 'type') else "unknown",
        }

        # Drop oldest event if queue is full (protect memory)
        if self.queue.full():
            try:
                self.queue.get_nowait()
                self._dropped_count += 1
            except asyncio.QueueEmpty:
                pass

        await self.queue.put(data)

    async def _worker(self):
        """Background loop: process queued events sequentially."""
        while self.running:
            try:
                event = await self.queue.get()
                await self._process(event)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Worker error: %s", e)

    async def _process(self, event: dict):
        """Process a single network event. Override in subclass."""
        logger.info("Request: %s %s", event["method"], event["url"][:120])

    @property
    def dropped_count(self) -> int:
        """Number of events dropped due to queue overload."""
        return self._dropped_count

    @property
    def queue_size(self) -> int:
        """Current number of events waiting to be processed."""
        return self.queue.qsize()

    async def cleanup(self):
        """Graceful shutdown: stop worker and drain queue."""
        self.running = False
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
        logger.info(
            "NetworkMonitor stopped (dropped=%d, remaining=%d)",
            self._dropped_count,
            self.queue.qsize(),
        )
