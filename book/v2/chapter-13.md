# Data Engineering & Trusted Automation Pipelines

## Turning Browser Output into Business-Grade Data


![Chapter Illustration](Images/chapter-13.png)

## Previously

Chapter 12 gave you a reliable execution platform — Docker, scheduling, monitoring, recovery, secrets management. Your automation runs on schedule, survives crashes, and alerts you when something breaks.

Now we address the failure that no amount of scheduling can catch: the automation runs perfectly and produces bad data.


## Why This Chapter Exists

A scraped ₹89,999 becomes 0 because a selector returned "Price unavailable." An automation stores empty strings because the element had no text. A price monitor reports "in stock" because the HTML said so — even though the JavaScript state had changed.

This chapter is not about extracting more data. It is about proving that extracted data is trustworthy.

A scraped `₹89,999` becomes `0` because a selector returned "Price unavailable." A scraper stores empty strings because the element had no text. A price monitor thought the product was "in stock" because the HTML said so — even though the JavaScript state had changed.

This chapter is not about extracting more data. It is about **proving that the data you extracted is trustworthy.**


## The Cost of Getting This Wrong

| Mistake | Outcome | Cost |
|---------|---------|------|
| No validation before storage | ₹0 stored as a valid price because selector returned "N/A" | Wrong business decisions based on bad data |
| No provenance tracking | Six months later: "where did this come from?" | Cannot answer — data is unusable for audits |
| No incremental scraping | Full rescrape every cycle — 99.9% redundant | Unnecessary bandwidth, CPU, API quota |
| No structural comparison | Website redesign undetected until extraction returns zero rows | Days of missed data before discovery |
| No data lineage | Dashboard shows a number. Nobody knows if it was validated. | Data is mistrusted by default |


## The Mental Shift

### Beginner Thinking
> "I extracted the data. My job is done."

### Production Thinking
> "I extracted the data. Now I must prove it is correct, complete, and ready for downstream systems."




### Data Decay

Data changes over time — even if it is stored correctly.

```text
Day 0:  ₹89,999  (freshly extracted, validated, stored)
Day 1:  ₹89,999  (still accurate — price unchanged)
Day 7:  ₹89,999  (may have changed — no re-check)
Day 30: ₹89,999  (likely stale — competitor may have updated)
Day 90: ₹89,999  (high risk — seasonal pricing, new models)
```

Without re-validation, all data decays. The rate depends on the domain:

| Data Type | Useful Lifetime | Re-check Frequency |
|-----------|----------------|-------------------|
| Currency exchange rate | Minutes | Every run |
| Competitor prices | Hours to days | Daily |
| Product availability | Hours | Every 6 hours |
| Supplier catalog | Days to weeks | Weekly |
| Historical trends | Months to years | Never (archive) |

A production system should tag every record with its expected decay rate and flag records that exceed their useful lifetime.


## The Data Trust Pipeline

```text
Browser (via nodriver) → Extract → Raw Data → Validate → Normalize → Deduplicate → Attach Provenance → Store → Export
```

Every step either increases or decreases trust.

### The Trust Pyramid

Data trust is not binary — it is layered:

```text
            Business Decisions
        ┌──────────────────────────────┐
        │       Trusted Data           │
        │   (provenance, lineage)      │
        ├──────────────────────────────┤
        │     Normalized Data          │
        │    (comparable fields)       │
        ├──────────────────────────────┤
        │     Validated Data           │
        │  (type, range, business)     │
        ├──────────────────────────────┤
        │       Extracted Data         │
        │     (raw from browser)       │
        └──────────────────────────────┘
```

Raw extracted data has zero trust. It may be malformed, from the wrong element, or contain placeholder values. Each layer of the pyramid adds a validation that increases confidence.

### Data Lineage

Provenance answers "where did this record come from?" Lineage answers "how did it get here and who touched it?"

```text
Competitor Website
    ↓ (nodriver extraction)
Raw Price: "₹89,999"
    ↓ (validation)
Checked: type=numeric, range=100-999999
    ↓ (normalization)
Parsed: 89999.0
    ↓ (storage)
Database: prices table, row id=48291
    ↓ (export)
Dashboard: "Current Competitor Price: ₹89,999"
    ↓ (decision)
Business: "Match price at ₹89,999"
```

Each arrow is a transformation that could introduce error. Lineage tracks every step so you can answer "was this price validated?" with evidence.

- **Raw data** has zero trust — it may be malformed, missing, or wrong.
- **Validated data** has high trust — if it passes schema checks.
- **Normalized data** is comparable — currency, dates, and units are consistent.
- **Provenance-attached data** is provable — you know where it came from and when.


## Production Incident

A retailer built a daily price monitoring system. The scraper ran every morning. One day a selector changed. Instead of `₹89,999`, the scraper stored: `"Price unavailable"`. The parser converted it to `0`. No exception. No timeout. The automation worked.

Marketing launched a "Beat Any Competitor Price" campaign.

They lost thousands of dollars.

The software never crashed. The data failed.


## Data Contract

Before any record reaches your database, it must satisfy a contract. Every downstream system — dashboards, reports, alerts, analytics — depends on this contract being enforced at ingestion time. In nodriver-based automation, this contract is enforced by `common/data_pipeline.py`:

```text
Browser Output (nodriver extraction)

    ↓

Data Contract

Every stored record MUST include:

  ✓ Required fields (sku, name, price, url)
  ✓ Correct types (price is numeric, not text)
  ✓ Valid ranges (price > 0, name not empty)
  ✓ Provenance (source URL, scraper version, collected at)
  ✓ Environment snapshot reference (Recipe 39)
  ✓ Run ID

    ↓

Database
```

This contract is not a suggestion. It is an architectural constraint. Records that violate the contract are quarantined — never stored.


## Recipe 52 — Validate Scraped Records Before Storage

**Stable ID:** DATA-VALIDATION
**File:** `recipes/ch13/52_validate.py`
**Prerequisites:** PRODUCTION-SCAFFOLD

### Problem

Your scraper extracted a record. It looks correct. But is every field valid?

### Why Validation Exists

Without validation, bad data spreads invisibly:

```text
Browser → Database → Dashboard → Business Decision (wrong)
```

### The Four Validation Layers

| Layer | What It Checks | Example |
|-------|---------------|---------|
| Structure | Required fields exist | sku, name, price, url |
| Type | Field is correct type | price is numeric |
| Business Rule | Value is realistic | price > 0, discount <= 90% |
| Context | Value is plausible | ₹5 today vs ₹75,000 yesterday — flag it |

### Production Pattern

```python
from common.data_pipeline import validate_product, quarantine_record

record = {"sku": "LAPTOP-001", "name": "", "price": "N/A"}
data, errors = validate_product(record)
if errors:
    quarantine_record(record, errors)
```

### The Quarantine Pattern

Never throw bad records away. Quarantine them for manual review:

```text
Raw Record → Validator → Accepted → Store
                       → Quarantine → Manual Review
```

### Production Rule

> Validation must happen before storage. Never after.


## Recipe 53 — Normalize and Export Trusted Data

**Stable ID:** DATA-NORMALIZATION
**File:** `recipes/ch13/53_normalize_export.py`

### Problem

Three websites report the same product. Three different formats:

```
₹89,999    | 89,999 INR    | Rs.89999
```

Your database should store one value, not three.

### Normalization Layers

| Layer | Operation |
|-------|-----------|
| Currency | Strip symbols, convert to base currency |
| Whitespace | Strip leading/trailing, collapse multiples |
| Unicode | Normalize to NFC |
| Dates | Convert to ISO 8601 |
| Booleans | "Yes" / "Available" / "In Stock" → `true` |

### Export Format Selection

| Format | Best For | Caveat |
|--------|----------|--------|
| CSV | Analysts, Excel | UTF-8 BOM required for Excel |
| JSON | APIs, developers | Larger file size |
| Parquet | Data pipelines | Requires PyArrow |

### Production Rule

> Store canonical values, not presentation values. Export is a delivery format — the database is the source of truth.


## Recipe 54 — Incremental Scraping & Change Detection

**Stable ID:** INCREMENTAL-SCRAPING
**File:** `recipes/ch13/54_incremental_scraping.py`

### Problem

Full rescrapes waste resources. If 10 of 10,000 products change daily, a full scrape is 99.9% redundant.

### Concept

```text
Extract → Normalize → Hash → Seen Before?
  YES → Skip
  NO  → Store
```

### The Dynamic Content Problem

Hashing the entire HTML fails because timestamps, nonces, and ads change every load. Strip them first:

```python
import re

def stable_hash(content: str) -> str:
    content = re.sub(r'data-time="\d+"', '', content)
    content = re.sub(r'nonce="[^"]+"', '', content)
    return hashlib.sha256(content.encode()).hexdigest()
```

### Failure Modes

| Failure | Cause | Fix |
|---------|-------|-----|
| Everything looks "new" | Dynamic timestamps in content | Strip before hashing |
| Nothing ever "changes" | Content hash too broad | Hash meaningful fields only |


## Recipe 55 — Structural Page Comparison

**Stable ID:** STRUCTURAL-COMPARISON
**File:** `recipes/ch13/55_structural_compare.py`

### Problem

Pixels change for reasons that have nothing to do with your data (ads, banners, clocks). But the DOM structure changing may indicate the website redesign that breaks your automation.

### Concept

Compare DOM structure, not screenshots. `common/visual_diff.py` implements tag-structure comparison:

```python
from common.visual_diff import compare_regions

diff = compare_regions(yesterday_html, today_html, selectors=[".product-table"])
if diff["rows"] == "125 → 0":
    alert(f"Product table disappeared — possible extraction failure")
```

### What to Monitor

| Region | Signal |
|--------|--------|
| Product table rows | Extraction still working? |
| Search result count | Data still available? |
| Form fields | Page structure changed? |

### Production Rule

> Structural comparison detects failures before validation does. A table with 125 rows that drops to 0 rows is a structural failure, not a validation error.


## Recipe 56 — Data Provenance & Audit Trails

**Stable ID:** DATA-PROVENANCE
**File:** `recipes/ch13/56_provenance.py`

### Problem

Six months later, a customer asks: "Where did this price come from?" Can you answer?

### Every Record Needs Provenance

```json
{
  "price": 89999,
  "provenance": {
    "source_url": "https://competitor.com/product/laptop",
    "scraper_version": "PRICE-MONITOR",
    "run_id": "2026-07-15-001",
    "collected_at": "2026-07-15T06:00:00Z"
  }
}
```

### Implementation

Use `common/data_pipeline.py`:

```python
from common.data_pipeline import attach_provenance

record = attach_provenance(
    {"sku": "LAPTOP-001", "price": 89999},
    source_url="https://...",
    scraper_version="PRICE-MONITOR",
    run_id="2026-07-15-001"
)
```

Every provenance record should also reference the **Environment Snapshot** (Recipe 39, `ENVIRONMENT-SNAPSHOT`) so data can be traced back to the exact execution environment.

### Production Rule

> A number without provenance is just a number. A number with provenance is evidence.


## Data Quality Dashboard

Instead of a single score, measure your pipeline's operational health each run:

```text
Today's Run
─────────────────────────────
Accepted Records    12,481
Rejected                 32
Quarantined              11
Duplicates               41
Validation Success   99.74%
Structural Drift         0
Export Status        Success
```

Track these metrics over time. A sudden increase in quarantined records means a website changed or a selector broke.


## Common Data Engineering Mistakes

- [✗] Saving raw HTML as truth
- [✗] Trusting every extracted value without validation
- [✗] Hashing entire pages (timestamps break dedup)
- [✗] Deleting invalid records instead of quarantining
- [✗] Ignoring provenance — "where did this come from?"
- [✗] Exporting directly from the browser instead of validated storage


## Chapter Summary

The browser collects data. The automation system is responsible for proving that the data can be trusted.

This is not a technical afterthought. It is a core engineering responsibility. A scraper that silently stores bad data is worse than one that crashes — a crash is obvious, bad data is discovered only after someone makes a wrong decision based on it.

The patterns in this chapter — validation, quarantine, normalization, incremental collection, structural comparison, provenance — are what separate amateur data scraping from professional data engineering.



## Engineering Review

### Things You Now Understand
- Extracted data is not trustworthy until validated, normalized, and provenanced
- The Data Contract defines what every record must satisfy before storage
- Validation must happen before storage — never after
- Validation has 4 layers: structure, type, business rule, context
- Data decay means all data has a useful lifetime — tag records with expected decay rate
- Provenance answers "where did this come from?" Lineage answers "how did it get here?"

### Common Mistakes
- [✗] Not validating data type — strings stored where numbers are expected
- [✗] Assuming all records have the same structure — merged cells produce jagged arrays
- [✗] Hashing entire pages for dedup — timestamps and nonces change every load
- [✗] Deleting invalid records instead of quarantining — loses evidence of failure patterns
- [✗] Storing raw HTML as the source of truth — expensive and not a stable diff target

### Senior Takeaways
- The Trust Pyramid shows data trust is layered — each layer adds confidence
- Data lineage tracks every transformation so you can answer "was this price validated?" with evidence
- Confidence scores make data quality visible to operators and downstream consumers

### Architecture Questions
1. Your validation pipeline rejects 5% of records. Is this normal variation or a systematic problem? What threshold determines the difference?
2. A website changes its price format from ₹89,999 to 89999.0. Does your validation catch this, or does it silently succeed?
3. Six months after deployment, a client asks "where did this specific price come from?" What data do you need to have stored to answer this?

**Next: Chapter 14 — Production Case Studies**

Where everything from Chapters 9 through 13 comes together as complete, deployable systems that solve real business problems.
