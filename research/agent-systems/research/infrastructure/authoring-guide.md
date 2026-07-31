# Agent Systems Authoring Infrastructure

> **Status:** Frozen  
> **Date:** 2026-07-22  
> **Purpose:** Authoring standards for building consistent, maintainable Research Packages across 24+ nodes.

---

## What This Is

When you have 1 node, natural consistency works fine. When you have 24 nodes written by one person across months, natural consistency degrades. This infrastructure is the scaffolding that prevents structural drift — it replaces "remember the style guide" with "follow the template."

These are not optional guidelines. Every Reference Package MUST include these assets.

---

## Directory Layout

```text
research/
├── infrastructure/
│   ├── authoring-guide.md             # Master instructions for authors
│   ├── templates/
│   │   ├── design-invariants.md       # Template + filled example
│   │   └── node-contract.md           # Template + filled example
│   ├── evidence-citation-standard.md  # How to cite sources consistently
│   ├── diagram-standard.md            # Visual language rules
│   └── terminology-glossary.md        # Single authoritative vocabulary
│
└── packages/
    └── node-01-perception/
        ├── CONTRACT.md                # Applied contract (machine-readable YAML)
        ├── INVARIANTS.md              # Applied invariants (timeless truths)
        └── references.md              # Main reference document
```

---

## The Five Assets

### 1. Design Invariants

Timeless truths about a node that do not change when tools evolve. Unlike production patterns (which become obsolete) or current implementations (which get replaced), invariants capture what is fundamental to the node's role in the architecture.

Example for Perception:
- Every observation has a cost.
- Every observation has uncertainty.
- Higher fidelity is not always better.
- Perception quality bounds decision quality.
- Structured perception dominates when available.

Placement: Included in `references.md` after Mental Model, before Module A. Also stored in `/infrastructure/templates/design-invariants.md`.

### 2. Node Contract

Formal interface declaration borrowed from software architecture. Defines exactly what a node consumes, produces, guarantees, and does NOT guarantee. Enables neighboring nodes to reason about dependencies without reading the full reference.

Example for Perception:
```yaml
consumes: [observations]
produces: [structured_observations]
guarantees: [confidence_estimate, freshness_metadata]
does_not_guarantee: [correctness, completeness]
```

Placement: Separate file at `<package>/CONTRACT.md` for machine readability. Also referenced in Interfaces table within `references.md`.

### 3. Diagram Standard

A fixed visual language. No ad-hoc chart styles. All diagrams use the same conventions:
- Flow diagrams: top-down, labeled arrows, consistent shapes
- Dependency diagrams: node boxes with arrow direction encoding
- Decision trees: diamond decision points, rectangular outcomes
- Sequence diagrams: actor lifelines, solid arrows for sync, dashed for async

All source files live in `diagrams/` (Mermaid `.md`). Published assets in `figures/` (SVG).

### 4. Evidence Citation Standard

Uniform format for citing sources. Eliminates ambiguity about what constitutes evidence vs. opinion.

Every factual claim in Modules A–C ends with an inline tag: `[Type: ID]`

| Type | Tag Format | Acceptable Location |
|---|---|---|
| Canon | `[Canon: Node XX]` | Any |
| Primary | `[Primary: ID]` | Modules A–C |
| Engineering | `[Engineering: ID]` | Modules A–C (flagged if vendor-published) |
| Benchmark | `[Benchmark: ID]` | Modules A–C |
| Community | `[Community: ID]` | Appendix only |
| Opinion | `[Opinion: ID]` | Introduction only |

Source details live in the shared `evidence/` root, not repeated per package.

### 5. Terminology Glossary

Single authoritative definitions for terms that appear across multiple packages. Prevents subtle meaning drift.

Defined once, referenced everywhere. If a term appears in `glossary.md`, every package that uses it must apply the same definition.

---

## Version Lifecycle

Packages follow a maturity progression:

| Version Range | Meaning | Quality Gates Required |
|---|---|---|
| `0.x` | Active research. Structure is correct; content may be incomplete. | Structure only |
| `1.0` | First internally validated reference. All modules populated with cited content. | Structure + Evidence |
| `1.x` | Incremental updates (new benchmarks, removed tools, added implementations). | Structure + Evidence |
| `2.0` | Major conceptual revision (new modality, shifted architecture view). | Structure + Evidence + Canonical |
| `3.0` | Decommissioned / Deprecated. Final release locked. | All four |

The **spec_version** tracks the specification version used. The **package version** tracks the maturity of this specific package. They diverge when a package receives a major revision after spec stabilization.

---

## Review Dimensions

Each package goes through four independent reviews:

| Review | Who It Checks | Trigger |
|---|---|---|
| **Technical** | Architecture accuracy, Canon compliance, interface correctness | All versions |
| **Editorial** | Clarity, consistency, tone, formatting | Before 1.0, before 2.0 |
| **Evidence** | Claim-source alignment, evidence taxonomy adherence, no gaps | Before 1.0, before 2.0 |
| **Canonical** | Whether the package necessitates Canon changes | All versions |

These are tracked in `package.yaml`:

```yaml
review_stage: pilot         # pilot | wave1 | wave2 | scaling | active
technical_review: passed    # pending | passed | blocked
editorial_review: passed    # pending | passed | blocked
evidence_review: passed     # pending | passed | blocked
canonical_review: passed    # pending | passed | blocked
```

---

*End of Authoring Infrastructure*
