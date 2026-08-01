# Integration Contract — HPF ↔ Publishing

**Design document. Not an implementation spec.**

This file is the constitution between the two repositories: HPF (knowledge) and
the publishing system (presentation). It defines the boundary, the two
exchange contracts, ownership, versioning expectations, and evolution rules.
No code implements this yet; implementation begins after the **First Revenue**
milestone (see D-024) is reached.

Status: **formalize, don't redesign** — most of this machinery already exists
in `tools/publisher/consume_handoff.py` but was never recognized as a contract.

---

## The boundary rule

> **HPF owns knowledge. Publishing owns presentation. Neither repository may
> directly depend on the other's internal structure. All integration occurs
> exclusively through versioned exchange contracts (Knowledge Package → Publishing,
> Feedback Package → HPF).**

HPF may change 100 internal files; publishing changes zero. Publishing may
reorganize everything; HPF changes zero. Changes happen at the contract
boundary, not inside either codebase.

## Exactly two contracts

Today the boundary is leaking through four informal artifacts:

| Artifact | Status |
|---|---|
| Knowledge package (`concepts`/`briefs`/`problems`) | ✅ primary, exists |
| `knowledge/concept-map.json` | ❌ secondary — retire, move into package |
| `articles/json/manifest.json` | ❌ derived artifact — never a contract |
| `knowledge/feedback/*.json` outbox | ⚠️ exists but informal |

The end state: **exactly two contracts cross the boundary.** Anything else is
drift.

### Contract 1 — Knowledge Package (HPF → Publishing)

Everything HPF exports, in one versioned artifact:

- `contract: { knowledge_package: <n> }` — explicit declaration
- `producer: { name, version }` + `schema_version` + `compatibility` (semver range; mismatch → explicit `Unsupported contract. Need adapter.` failure, never a silent degrade)
- `generated_at` provenance
- **`capabilities` — mandatory** (e.g. `briefs: true`, `diagrams: false`, `quizzes: false`). Publishing may ignore it today; the day HPF grows a capability, the package advertises it — no schema migration.
- **`mappings` — generalized concept map** (replaces `concept-map.json`): `mappings: { concepts, problems, articles, patterns }`. Today only concepts exist; future ID families extend the dict, not the schema.
- `concepts`, `briefs`, `problems`

Artifact lifecycle:

```
handoff/schema/knowledge-package.schema.json   <- committed (schema is code-adjacent, shared)
handoff/latest.json                            <- gitignored (generated content = build artifact)
handoff/archive/knowledge-package-<date>-v<n>.json  <- gitignored (immutable history)
```

The archive answers "what knowledge generated Article #17?".

### Contract 2 — Feedback Package (Publishing → HPF)

Publishing exports **signals, not conclusions** — HPF interprets them.
Publishing stays dumb.

```
signals: [
  { type: views, article, platform, count, period },
  { type: search_query, article, query, impressions, ctr },
  { type: cta_click, article, platform, count },
  { type: sale, article, ref, amount, count },
  { type: comment, article, platform, excerpt },
  { type: discussion, source, topic, url }
]
```

- Aggregate of the existing `metrics/` collectors + the feedback outbox
- Weekly cadence, one file per period (e.g. `knowledge/feedback/feedback-package-2026-W32.json`)
- Existing outbox records (`processed: false`) fold into this; pickup is HPF-side

## Ownership matrix

| Owns | HPF | Publishing |
|---|---|---|
| Research | ✅ | ❌ |
| Canonical concepts | ✅ | ❌ |
| Patterns | ✅ | ❌ |
| Article briefs | ✅ | ❌ |
| Knowledge package | ✅ | ❌ |
| Website | ❌ | ✅ |
| Articles | ❌ | ✅ |
| Derivatives | ❌ | ✅ |
| Distribution | ❌ | ✅ |
| Metrics collection | ❌ | ✅ |
| Feedback package | ❌ | ✅ |

> If both columns are ever ✅ for the same responsibility, the architecture has drifted.

## Versioning expectations

- Contract version bumps are breaking changes; add fields to `schema_version`
  minors, never silently drop fields
- `compatibility` ranges ride along so old packages keep working where practical
- Both repos test against the same schema but **never share test files**:
  HPF keeps `tests/export_contract.py`, publishing keeps `tests/import_contract.py`

## Evolution rules

1. Extend the Knowledge Package, never the publishing system's internals.
2. New HPF capabilities arrive as `capabilities` flags; publishing routes or ignores.
3. No new secondary contracts. A third artifact = revisit this document.
4. The feedback loop runs only when real traffic exists — see principle below.

## Principle (from D-024 discussion)

> Building the feedback loop before there's traffic is building infrastructure
> on zero data.

This is exactly what the engineering freeze protects against. Until First
Revenue (10 articles / 10 pattern docs / 50 derivatives / 100+ visitors /
first funnel-attributable sale), the only allowed contract work is this
document and its maintenance.

## Known follow-ups (post-First-Revenue)

- Formalize the envelope in `consume_handoff.py` (extend, don't rewrite)
- Move `concept-map.json` into package `mappings`; retire the file
- Aggregate feedback into weekly `signals[]` packages
- Add `handoff/` ignore rules + `handoff/schema/` to the publishing repo
- Publish this document (or a pointer) into the HPF repo as well
