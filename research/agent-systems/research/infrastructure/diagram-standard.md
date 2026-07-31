# Agent Systems Diagram Standard v1.0

> **Status:** Frozen  
> **Date:** 2026-07-22  
> **Purpose:** Standard visual language for all diagrams across the Research Package system.

---

## Core Rules

1. All diagrams use **Mermaid** syntax for source files (`diagrams/` directory).
2. Published outputs are **SVG** in `figures/` directory.
3. Every diagram has a **caption** in the referencing `references.md` section that explains what it shows and why it matters.
4. No ad-hoc chart styles. These five diagram types cover all documented needs:

| Type | Use When | File Convention |
|---|---|---|
| **Flow Diagram** | Showing data/information flow between components | `flow-*.mermaid` |
| **Dependency Diagram** | Showing which nodes depend on which | `deps-*.mermaid` |
| **Decision Tree** | Showing modality selection or other branching logic | `decision-*.mermaid` |
| **Sequence Diagram** | Showing temporal ordering of interactions between nodes | `seq-*.mermaid` |
| **Architecture Diagram** | Showing structural layout of a system or layer | `arch-*.mermaid` |

---

## Color Palette

| Color | Hex | Use |
|---|---|---|
| **Teal** | `#3F6E8C` | Primary nodes, core pipeline |
| **Muted Green** | `#6B9080` | Supporting/guardrail nodes |
| **Warm Gray** | `#2E3440` | Text, borders, background |
| **Light Warm** | `#F5F3EE` | Background fills |
| **Highlight** | `#E5DED2` | Emphasized elements in diagrams |

---

## Flow Diagrams

For showing perception pipeline, execution flow, data transformation.

```mermaid
flowchart TD
    A[Raw Environment] --> B[Signal<br/>Acquisition]
    B --> C{Modality<br/>Selection}
    C -->|Vision| D[Screenshot<br/>1,600+ tokens]
    C -->|AXTree| E[Accessibility Tree<br/>200-400 tokens]
    C -->|WebMCP| F[Typed Tool Call<br/>20-100 tokens]
    D --> G[Confidence<br/>Assessment]
    E --> G
    F --> G
    G --> H[Structured Observation<br/>+ Confidence Score]
```

Style rules:
- Round rectangles for processes, diamonds for decisions, square brackets for I/O
- Bold labels for major transitions
- Keep descriptions on single lines; use `<br/>` for multi-line labels
- Arrows must have labels when the branch has meaning

---

## Dependency Diagrams

For showing node-to-node relationships within the architecture.

```mermaid
graph LR
    A[Node 01: Perception] --> B[Node 02: Decision Engine]
    B --> C[Node 03: Planning]
    C --> D[Node 04: Scheduling]
    D --> E[Node 05: Execution]
    E --> F[Node 06: Verification]
    F --> G[Node 07: Recovery]
    G --> H[Node 08: Learning]
    H -->|feedback| B
    B -->|feeds| C
```

Style rules:
- Use explicit arrow labels (`-->|label|`) for meaningful relationships
- Solid lines for primary dependencies, dashed for optional/conditional
- Direction flows left-to-right by default

---

## Decision Trees

For showing selection logic (e.g., modality selection, model routing).

```mermaid
flowchart TD
    A[Task Received] --> B{WebMCP<br/>available?}
    B -->|Yes| C[Use WebMCP<br/>20-100 tokens]
    B -->|No| D{Visual task?<br/>canvas/images/layout}
    D -->|Yes| E[Use Vision<br/>1,600+ tokens]
    D -->|No| F{A11Y-compliant site?}
    F -->|Yes| G[Use AXTree<br/>200-400 tokens]
    F -->|No| H[Use Hybrid<br/>500-1,500 tokens]
```

Style rules:
- Decisions are diamonds with labeled branches
- Outcomes are rectangles
- One level of nesting maximum (deep trees use flowcharts with subgraphs instead)

---

## Sequence Diagrams

For showing temporal interactions between nodes during an agent step.

```mermaid
sequenceDiagram
    participant Surface as Execution Surface
    participant P as Perception (01)
    participant DM as Decision Engine (02)
    
    Surface->>P: Raw signals
    P->>P: Modality Selection
    P->>P: Signal Transformation
    P->>DM: Structured Observation + Confidence
    Note over P,DM: Observation includes: token_count, timestamp, modality, confidence
```

Style rules:
- Use short participant names (node number abbreviation)
- Self-messages show internal processing
- Notes explain what's implicit in the arrow labels

---

## Architecture Diagrams

For showing system structure, layers, or physical deployment.

```mermaid
graph TB
    subgraph Tier0["Tier 0 — Atomic Loop"]
        P[Perception] --> DE[Decision Engine]
        DE --> PL[Planning]
        PL --> SE[Scheduling]
        SE --> EX[Execution]
        EX --> VE[Verification]
        VE --> RE[Recovery]
        RE --> LE[Learning]
        LE -->|feedback| DE
    end
    
    subgraph Tier1["Tier 1 — Containers"]
        WM[Working Memory]
        LTM[Long-term Memory]
        ES[Environment State]
    end
    
    subgraph Tier2["Tier 2 — Guardrails"]
        SEC[Security]
        GOV[Governance]
    end
    
    subgraph Tier4["Tier 4 — Execution Surfaces"]
        BS[Browser 17]
        DS[Desktop 18]
        TS[Terminal 19]
        AS[API 20]
        MS[Mobile 21]
        IS[IoT 22]
    end
    
    Tier0 --> Tier1
    Tier0 --> Tier2
    Tier0 --> Tier4
```

Style rules:
- Use subgraphs for tiers/layers
- One diagram per package unless cross-tier complexity demands multiple
- Avoid nested subgraphs deeper than one level

---

## General Rules

1. **One diagram per conceptual idea.** Don't cram multiple concepts into one diagram.
2. **Maximum 15 elements per diagram.** If you need more, split into focused diagrams.
3. **Every diagram must be compilable with `mermaid-cli`.** Test rendering before publishing.
4. **File naming:** `diagrams/<type>-<topic>.mermaid` → `figures/<type>-<topic>.svg`
5. **Captions in references.md:** Every diagram reference includes a one-line explanation of what the reader should notice.

---

*End of Diagram Standard v1.0*
