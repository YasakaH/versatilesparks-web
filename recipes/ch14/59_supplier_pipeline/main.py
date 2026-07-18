"""
Recipe 59 — Supplier Intelligence Pipeline

Business Problem:
    Monitor 25 supplier portals for stock levels, pricing, ETA, and promotions.
    Each supplier has a different website and authentication scheme.

Architecture:
    Queue → Worker Pool (2-3 max) → Extraction → Validation → Provenance → Storage → Exports

Uses common/ modules for browser, retry, logging, recovery, and data pipeline.
Scaling note: increase workers only after measuring CPU/memory stability.
"""

import asyncio
from common.browser import launch_browser
from common.data_pipeline import validate_product, attach_provenance
from common.logging import logger


MAX_WORKERS = 3


class SupplierPipeline:
    """Manage concurrent supplier extraction with worker isolation."""

    def __init__(self, suppliers: list):
        self.suppliers = suppliers
        self.results = []

    async def extract_supplier(self, supplier: dict) -> dict:
        browser = await launch_browser()
        try:
            page = await browser.get(supplier["url"])
            raw = {"sku": supplier["id"], "name": supplier.get("name", ""), "price": 0.0, "url": supplier["url"]}
            data, errors = validate_product(raw)
            if errors:
                return {"supplier": supplier["id"], "status": "quarantined", "errors": errors}
            attach_provenance(data, source_url=supplier["url"], scraper_version="SUPPLIER-PIPELINE", run_id="")
            return {"supplier": supplier["id"], "status": "success", "data": data}
        finally:
            await browser.stop()

    async def run(self):
        sem = asyncio.Semaphore(MAX_WORKERS)
        async def bounded(supplier):
            async with sem:
                return await self.extract_supplier(supplier)
        self.results = await asyncio.gather(*[bounded(s) for s in self.suppliers])
        logger.info("Pipeline: %d suppliers → %d success", len(self.suppliers), sum(1 for r in self.results if r["status"] == "success"))
        return self.results


async def main():
    pipeline = SupplierPipeline([{"id": "SUP-001", "name": "Acme Corp", "url": "https://supplier.example.com"}])
    results = await pipeline.run()
    print(f"Processed {len(results)} suppliers")


if __name__ == "__main__":
    asyncio.run(main())
