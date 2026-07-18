"""
Recipe 56 (V2): Data Provenance & Audit Trails

Attach source_url, scraper_version, run_id, and collected_at
to every record so data can be traced back to its origin.

Uses common/data_pipeline.py attach_provenance() function.
"""
import asyncio
from common.data_pipeline import attach_provenance


async def main():
    record = attach_provenance(
        {"sku": "LAPTOP-001", "price": 89999},
        source_url="https://competitor.com/product/laptop",
        scraper_version="PRICE-MONITOR",
        run_id="2026-07-15-001",
    )
    print(f"Record with provenance: {record}")


if __name__ == "__main__":
    asyncio.run(main())
