"""
Recipe 52 (V2): Validate Scraped Records Before Storage

Uses common/data_pipeline.py to validate, quarantine, and alert
on bad data. The four validation layers: structure, type, business
rule, and context.
"""
import asyncio
from common.data_pipeline import validate_product, process_products


async def main():
    sample = [
        {"sku": "LAPTOP-001", "name": "Gaming Laptop", "price": 89999, "url": "https://example.com/1"},
        {"sku": "PHONE-002", "name": "", "price": 49999, "url": "https://example.com/2"},
        {"sku": "TAB-003", "name": "Tablet", "price": -1, "url": "https://example.com/3"},
    ]
    valid = process_products(sample)
    print(f"Valid: {len(valid)} / {len(sample)}")


if __name__ == "__main__":
    asyncio.run(main())
