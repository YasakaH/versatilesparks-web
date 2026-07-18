"""
idempotency.py — Production Idempotency Patterns

Prevent duplicate processing when the same automation runs
twice. Core pattern for reliable production systems.

Architecture:
  Incoming event → Generate deterministic key → Already processed?
  → Yes: Stop (return duplicate status)
  → No: Process → Store key → Return result

Usage:
    from common.idempotency import idempotent, IdempotencyStore

    @idempotent(lambda product: f"price:{product['sku']}")
    async def process_product(product):
        # ... processing logic ...

    # Or use the store directly:
    store = IdempotencyStore("my_app.db")
    if not store.exists("job:2026-07-15"):
        await run_job()
        store.save("job:2026-07-15")
"""
from functools import wraps
from datetime import datetime
import sqlite3


class IdempotencyStore:
    """Persistent store for processed operation keys.

    Uses SQLite so state survives process restarts.
    Thread-safe: uses check_same_thread=False for async workers.
    """

    def __init__(self, db_path: str = "idempotency.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS processed_events (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def exists(self, key: str) -> bool:
        """Check if an operation key has already been processed."""
        cursor = self.conn.execute(
            "SELECT id FROM processed_events WHERE id = ?",
            (key,)
        )
        return cursor.fetchone() is not None

    def save(self, key: str) -> None:
        """Record an operation key as processed."""
        self.conn.execute(
            "INSERT OR IGNORE INTO processed_events VALUES (?, ?)",
            (key, datetime.utcnow().isoformat())
        )
        self.conn.commit()

    def count(self) -> int:
        """Return total processed events (useful for monitoring)."""
        cursor = self.conn.execute("SELECT COUNT(*) FROM processed_events")
        return cursor.fetchone()[0]


# Global default store — importable by all recipes
default_store = IdempotencyStore()


def idempotent(key_builder):
    """Decorator that prevents duplicate async function execution.

    Args:
        key_builder: Callable that receives the same args/kwargs
                     as the decorated function and returns a
                     unique string key for the operation.

    Returns:
        Decorated async function that returns
        {"status": "duplicate", "key": ...} if already processed,
        or the original function's result otherwise.

    Example:
        @idempotent(lambda sku, **kw: f"price:{sku}")
        async def process_product(sku, name, price):
            # runs once per unique sku
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = key_builder(*args, **kwargs)
            if default_store.exists(key):
                print(f"Skipping duplicate: {key}")
                return {"status": "duplicate", "key": key}
            result = await func(*args, **kwargs)
            default_store.save(key)
            return result
        return wrapper
    return decorator


# ---- UPSERT Pattern ----

def upsert_product(conn, product: dict) -> None:
    """Insert or update a product record using SKU as natural key.

    Args:
        conn: sqlite3.Connection
        product: dict with sku, name, price keys

    This is the production pattern for price monitoring —
    running twice updates the record rather than duplicating it.
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        INSERT INTO products (sku, name, price)
        VALUES (?, ?, ?)
        ON CONFLICT(sku)
        DO UPDATE SET
            name = excluded.name,
            price = excluded.price,
            updated_at = CURRENT_TIMESTAMP
    """, (product["sku"], product["name"], product["price"]))
    conn.commit()


# ---- Lead Workflow Natural Key ----

def lead_dedup_key(lead: dict) -> str:
    """Generate a deterministic deduplication key for a lead.

    Uses company + email as the natural key, normalized to
    lowercase with whitespace stripped. This prevents duplicate
    lead creation when a workflow retries.

    Args:
        lead: dict with 'company' and 'email' keys

    Returns:
        Normalized key string: "company:email"
    """
    company = lead.get("company", "").strip().lower()
    email = lead.get("email", "").strip().lower()
    return f"{company}:{email}"
