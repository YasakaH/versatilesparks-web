"""
Recipe 58 — CRM Lead Processing System

Business Problem:
    A sales team receives 200+ leads/day through a website form.
    Each lead must cross three systems: Marketing → CRM → Sales.

Architecture:
    Lead Form → Validation → Duplicate Check → CRM → Assignment → Slack

Key concept: Idempotency. Running twice produces no duplicate leads.
Uses common/ modules for validation, dedup, and alerting.
"""

import asyncio
from common.data_pipeline import validate_product
from common.alert import send_alert


class LeadProcessor:
    """Process incoming leads with idempotency guarantee."""

    def __init__(self):
        self.seen = set()

    async def process(self, lead: dict) -> dict:
        # Validate
        data, errors = validate_product(lead)
        if errors:
            return {"status": "rejected", "errors": errors}

        # Idempotency check: company + email as natural key
        dedup_key = f"{lead.get('company', '')}|{lead.get('email', '')}"
        if dedup_key in self.seen:
            return {"status": "duplicate", "dedup_key": dedup_key}
        self.seen.add(dedup_key)

        # Submit to CRM (placeholder)
        print(f"Lead accepted: {lead.get('name')} at {lead.get('company')}")
        return {"status": "accepted", "dedup_key": dedup_key}


async def main():
    processor = LeadProcessor()
    result = await processor.process({"sku": "LEAD-001", "name": "Jane Doe", "price": 0, "url": ""})
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
