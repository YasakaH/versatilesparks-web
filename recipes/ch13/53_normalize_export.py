"""
Recipe 53 (V2): Normalize and Export Trusted Data

Strip currency symbols, normalize dates, canonicalize booleans.
Export to CSV, JSON, or Parquet from validated storage.
"""
import json, csv, re
from pathlib import Path


def normalize_price(raw: str) -> float:
    cleaned = re.sub(r"[₹€£$, ]", "", raw)
    cleaned = re.sub(r"(?:INR|USD|EUR|Rs\.?)", "", cleaned, flags=re.I)
    return float(cleaned)


def normalize_boolean(raw: str) -> bool:
    return raw.strip().lower() in ("yes", "available", "in stock", "true")


def export_csv(records: list, path: str = "export.csv"):
    if not records:
        return
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=records[0].keys())
        w.writeheader()
        w.writerows(records)


def export_json(records: list, path: str = "export.json"):
    Path(path).write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")


async def main():
    records = [{"sku": "LAPTOP-001", "price": normalize_price("₹89,999"), "in_stock": normalize_boolean("Available")}]
    export_csv(records)
    export_json(records)
    print(f"Exported {len(records)} records")


if __name__ == "__main__":
    asyncio.run(main())
