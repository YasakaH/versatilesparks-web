"""
data_pipeline.py — Data Validation, Quarantine, and Alerting

Production pattern for trustworthy data ingestion:

  Scrape → Validate → Store (if valid)
                   → Quarantine (if invalid) → Alert (if >10% fail)

Never do: Scrape → Save → Discover bad data later.

Usage:
    from common.data_pipeline import validate_product, process_products

    valid = process_products(scraped_records)
    # valid now contains only validated products
    # invalid records are quarantined to quarantine.json
"""
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

try:
    from pydantic import BaseModel, Field, ValidationError

    class Product(BaseModel):
        """Validated product schema for scraped data."""
        sku: str
        name: str = Field(min_length=1)
        price: float = Field(gt=0)
        url: str

    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    ValidationError = type("ValidationError", (Exception,), {})

    class Product:  # type: ignore
        """Simple dataclass fallback when pydantic is not installed."""
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

        def model_dump(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


def attach_provenance(record: dict, *, source_url: str = "", scraper_version: str = "", run_id: str = "") -> dict:
    """Attach provenance metadata to a scraped record.

    Args:
        record: The scraped record dict.
        source_url: The page URL the data was collected from.
        scraper_version: Stable recipe ID (e.g. 'PRICE-MONITOR').
        run_id: Unique run identifier.

    Returns:
        Record dict with provenance fields added.
    """
    record["provenance"] = {
        "source_url": source_url,
        "scraper_version": scraper_version or record.get("provenance", {}).get("scraper_version", ""),
        "run_id": run_id,
        "collected_at": datetime.utcnow().isoformat(),
    }
    return record


def validate_product(raw: dict) -> tuple:
    """Validate a scraped product record.

    Args:
        raw: Dict with sku, name, price, url keys.

    Returns:
        Tuple of (validated_dict_or_None, list_of_errors).
        If validation passes, errors list is empty.
    """
    if not HAS_PYDANTIC:
        # Simple validation fallback
        errors = []
        if not raw.get("sku"):
            errors.append({"loc": ("sku",), "msg": "sku is required"})
        try:
            price = float(raw.get("price", 0))
            if price <= 0:
                errors.append({"loc": ("price",), "msg": "price must be positive"})
        except (TypeError, ValueError):
            errors.append({"loc": ("price",), "msg": "price must be numeric"})
        if errors:
            return None, errors
        return raw, []

    try:
        product = Product(**raw)
        return product.model_dump(), []
    except ValidationError as e:
        return None, e.errors()


def quarantine_record(raw: dict, errors: list, file: str = "quarantine.json") -> None:
    """Save an invalid record to the quarantine file for manual review.

    Args:
        raw: The original scraped record that failed validation.
        errors: List of validation error dicts.
        file: Path to quarantine JSON lines file.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "record": raw,
        "errors": errors,
    }
    with open(file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    logger.warning("Quarantined record: %s", raw.get("sku", raw.get("url", "unknown")))


def send_alert(failure_rate: float, threshold: float = 0.10) -> None:
    """Alert when validation failure rate exceeds threshold.

    Args:
        failure_rate: Fraction of records that failed (0.0 to 1.0).
        threshold: Alert when failure_rate exceeds this value (default 10%).
    """
    if failure_rate > threshold:
        msg = f"VALIDATION ALERT: {failure_rate:.2%} of records failed validation (threshold: {threshold:.0%})"
        logger.error(msg)
        print(f"\n*** {msg} ***\n")
    else:
        logger.info("Validation pass rate: %.2f%%", (1 - failure_rate) * 100)


def process_products(records: list) -> list:
    """Validate a batch of scraped products with quarantine + alerting.

    Args:
        records: List of raw product dicts.

    Returns:
        List of validated product dicts (invalid ones are quarantined).
    """
    valid = []
    failed = []

    for record in records:
        data, errors = validate_product(record)
        if errors:
            quarantine_record(record, errors)
            failed.append(record)
        else:
            valid.append(data)

    if records:
        send_alert(len(failed) / len(records))

    logger.info(
        "Pipeline: %d total → %d valid → %d quarantined",
        len(records), len(valid), len(failed)
    )
    return valid
