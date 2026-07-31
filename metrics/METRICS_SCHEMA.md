# Metrics Schema (v1)

Contract between metrics collectors (`tools/publisher/metrics/`) and the raw data store (`metrics/raw/`).

## Snapshot layout

```text
metrics/raw/YYYY-MM-DD.json

{
    "date":          "2026-07-31",          # UTC date of the snapshot
    "collected_at":  "2026-07-31T09:44:20Z",# precise collection timestamp
    "sources": {
        "devto": {                          # one key per active source
            "account":  { ... },            # source-wide analytics (totals, read time)
            "articles": [ ... ]             # per-item records (articles/pages/products)
        }
    }
}
```

Source-specific item names stay natural to the source:

- Dev.to → `account` + `articles`
- Gumroad → `account` + `products`
- Search Console → `site` + `pages` (+ `queries` when added)
- GitHub → `repository` + `metrics`

## Invariants

1. **Snapshots are immutable.** A day's file is never modified after it is written.
2. **One file per UTC day.** Filename is `YYYY-MM-DD.json` in UTC.
3. **Source names are stable.** Adding a source is a new key in `sources`; renaming is a schema change.
4. **Collectors must not modify previous snapshots.** They read them, never write them.
5. **`--force` is for development only.** It exists to correct a schema change during the pilot week, not for routine collection.
6. **Every snapshot is reproducible.** All data comes from API responses at `collected_at`; no derived values stored in raw files.

## Feedback records

Each collection emits one `FeedbackRecord` per article (signal_type `metrics_snapshot`) to `knowledge/feedback/`.

The event's existence is part of this contract; only the payload evolves.

## Collectors

- `collect.py` — CLI entry (`--devto`, `--gumroad`, `--search-console`, `--github`, `--all`)
- A collector that is not configured returns `[]` and is skipped; it never fails the snapshot.
