"""
Recipe 60 — Automation Operations Platform

Business Problem:
    An agency manages automation for 12 clients. Each automation
    has different schedules, profiles, and output requirements.
    Previously each ran on a separate server — unsustainable.

Architecture:
    Scheduler → Job Registry → Worker Pool → Browser Pool → Recovery → Metrics → Alerts

Single Python orchestration application. Not a distributed system.
Uses common/ modules for browser, recovery, metrics, alerting, and data pipeline.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from common.recovery import RecoveryManager, FailureType
from common.logging import logger


@dataclass
class Job:
    """A registered automation job within the platform."""
    name: str
    schedule: str  # cron expression or interval
    target_url: str
    profile_dir: str = ""
    enabled: bool = True
    last_run: str = ""
    success_count: int = 0
    failure_count: int = 0


@dataclass
class PlatformMetrics:
    """Aggregate platform health metrics."""
    total_jobs: int = 0
    running: int = 0
    idle: int = 0
    healthy_profiles: int = 0
    corrupted_profiles: int = 0


class AutomationPlatform:
    """Single-process automation operations platform.

    Registers jobs, dispatches workers, handles recovery,
    and collects metrics — all in one Python application.
    """

    def __init__(self):
        self.jobs: dict[str, Job] = {}
        self.recovery = RecoveryManager()
        self.metrics = PlatformMetrics()

    def register_job(self, name: str, target_url: str, schedule: str = "daily", profile_dir: str = ""):
        self.jobs[name] = Job(name=name, target_url=target_url, schedule=schedule, profile_dir=profile_dir)
        self.metrics.total_jobs = len(self.jobs)
        logger.info("Registered job: %s → %s", name, target_url)

    async def dispatch(self, job: Job):
        """Dispatch a single job with recovery coverage."""
        logger.info("Dispatching: %s", job.name)
        try:
            # Placeholder — see production implementation
            job.last_run = datetime.utcnow().isoformat()
            job.success_count += 1
            logger.info("Job complete: %s", job.name)
        except Exception as e:
            job.failure_count += 1
            decision = await self.recovery.handle(FailureType.UNKNOWN)
            if decision == "stop":
                logger.error("Job failed, manual intervention: %s", job.name)

    async def run(self):
        """Run the platform loop — dispatch all enabled jobs."""
        for job in self.jobs.values():
            if job.enabled:
                await self.dispatch(job)
        self.metrics.running = sum(1 for j in self.jobs.values() if j.enabled)
        self.metrics.idle = self.metrics.total_jobs - self.metrics.running
        return self.metrics


async def main():
    platform = AutomationPlatform()
    platform.register_job("Price Monitor", "https://competitor.com/products")
    platform.register_job("CRM Sync", "https://crm.example.com/leads")
    metrics = await platform.run()
    print(f"Platform ran: {metrics.running} jobs, {metrics.idle} idle")


if __name__ == "__main__":
    asyncio.run(main())
