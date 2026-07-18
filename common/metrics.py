"""
metrics.py — Automation Observability Metrics

Track success rate, runtime, and records processed per run.
Uses SQLite — zero infrastructure, works on any VPS.

Usage:
    from common.metrics import MetricsCollector

    metrics = MetricsCollector("metrics.db")
    metrics.record_run(status="success", records=150, runtime=273.4)
    rate = metrics.success_rate()  # 0.97
"""
import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Persistent automation run metrics using SQLite.

    Thread-safe for single-process async use. For multi-worker
    scenarios, switch to Postgres or use WAL mode.
    """

    def __init__(self, db_path: str = "metrics.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started TEXT NOT NULL,
                status TEXT NOT NULL,
                records INTEGER DEFAULT 0,
                runtime REAL DEFAULT 0.0
            )
        """)
        self.conn.commit()

    def record_run(self, status: str, records: int, runtime: float) -> None:
        """Record a completed automation run.

        Args:
            status: "success" or "failure"
            records: Number of records processed
            runtime: Duration in seconds
        """
        self.conn.execute(
            "INSERT INTO runs (started, status, records, runtime) VALUES (?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), status, records, runtime)
        )
        self.conn.commit()
        logger.info("Metrics: %s — %d records in %.1fs", status, records, runtime)

    def success_rate(self, last_n: int = None) -> float:
        """Calculate success rate over recent runs.

        Args:
            last_n: If set, only consider the most recent N runs.

        Returns:
            Float 0.0 to 1.0 representing success fraction.
        """
        query = """
            SELECT AVG(CASE WHEN status='success' THEN 1.0 ELSE 0.0 END)
            FROM runs
        """
        if last_n:
            query += f" ORDER BY id DESC LIMIT {last_n}"
        result = self.conn.execute(query)
        rate = result.fetchone()[0] or 0.0
        return rate

    def last_run(self) -> dict | None:
        """Get the most recent run record."""
        cursor = self.conn.execute(
            "SELECT started, status, records, runtime FROM runs ORDER BY id DESC LIMIT 1"
        )
        row = cursor.fetchone()
        if row:
            return {"started": row[0], "status": row[1], "records": row[2], "runtime": row[3]}
        return None

    def total_runs(self) -> int:
        """Total number of recorded runs."""
        cursor = self.conn.execute("SELECT COUNT(*) FROM runs")
        return cursor.fetchone()[0]

    def avg_runtime(self) -> float:
        """Average runtime in seconds across all runs."""
        cursor = self.conn.execute("SELECT AVG(runtime) FROM runs")
        return cursor.fetchone()[0] or 0.0

    def close(self):
        self.conn.close()
