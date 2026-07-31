# Platform Architecture — Frozen

This document declares the platform architecture frozen as of 2026-07-29. No new layers should be added without a governance review.

---

## The Stack

```
Research Domains (Stable)     ← Frozen, rarely change
      │
      ▼
Technology Profiles (Volatile) ← Active, added/removed as tools evolve
      │
      ▼
Canonical Concepts            ← Frozen, permanent intellectual property
      │
      ▼
HPF Knowledge Objects          ← Active, improved via benchmark evidence
      │
      ▼
HPF Reasoning Engine           ← Active, improved via benchmark evidence
      │
      ▼
Validation (Benchmark)         ← Active, runs on every significant change
      │
      ▼
Publications                   ← Flexible, decided at publication time
      ├── Books (Perspective A/B/C)
      ├── Blog posts
      ├── Courses
      ├── Documentation
      └── AI assistant knowledge base
```

---

## Layer Responsibilities

### Research Domains

**Status**: Frozen

Evergreen domains that define the boundaries of knowledge. See THREE-BOOK-PLAN.md for the full list.

**Owns**: What questions to ask.

### Technology Profiles

**Status**: Active

Tool-specific mappings onto stable domains. A Playwright profile documents how Playwright instantiates each stable domain concept.

**Owns**: How specific tools implement domain concepts.

### Canonical Concepts

**Status**: Frozen

The permanent intellectual property. Each concept is a durable idea defined independently of any tool or implementation. Concepts have properties, relationships, and constraints.

**Location**: `canon/concepts/`

**Owns**: What is true about the domain.

### HPF Knowledge Objects

**Status**: Active

Structured knowledge files in `tools/hpf-engine/domain/knowledge/`. Each object maps to one or more canonical concepts and adds the structure needed by the HPF reasoner (metadata, tags, entity references, mode-specific sections).

**Owns**: Knowledge in machine-readable form.

### HPF Reasoning Engine

**Status**: Active

The pipeline: question analyzer → retriever → evidence builder → renderer. Improved one behavioural deficiency at a time via the M2 validation cycle.

**Location**: `tools/hpf-engine/hpf/`

**Owns**: Generating answers from knowledge objects.

### Validation (Benchmark)

**Status**: Active

The dual-judge evaluation pipeline at `tools/hpf-engine/evaluation/`. Produces evidence that drives the improvement cycle.

**Owns**: Measuring whether the platform improves.

### Publications

**Status**: Flexible

Outputs that consume HPF knowledge. Not part of the HPF governance track.

**Owns**: Communicating knowledge to humans.

---

## Governance Boundaries

| Layer | Change Authority | Review Required |
|---|---|---|
| Research domains | Governance review | Yes |
| Technology profiles | Platform team | No |
| Canonical concepts | Governance review | Yes |
| HPF knowledge objects | Benchmark evidence | No (single-change cycle) |
| HPF reasoning engine | Benchmark evidence | No (single-change cycle) |
| Validation | Benchmark evidence | No |
| Publications | Editorial decision | No |

---

## Improvement Protocol (M2)

The only allowed path for changing HPF:

```
Observe (benchmark evidence)
      ↓
Pattern identification
      ↓
Root cause analysis
      ↓
Hypothesis formation
      ↓
Single change implementation
      ↓
Validation (re-run benchmark)
      ↓
Measure
      ↓
Repeat
```

No multi-change cycles. No intuition-led modifications. Every change must trace to a documented hypothesis from the M2 evidence base.

---

## What This Architecture Enables

1. **Research produces concepts** — one-time intellectual asset creation
2. **Concepts produce knowledge objects** — structured for machine reasoning
3. **Knowledge objects produce answers** — via the reasoning engine
4. **Benchmark validates answers** — evidence-guided improvement
5. **All publications consume the same knowledge** — books, blogs, courses, assistants

---

*Frozen: 2026-07-29*
*Supersedes any earlier architectural descriptions in HPF-HANDOFF.md*
