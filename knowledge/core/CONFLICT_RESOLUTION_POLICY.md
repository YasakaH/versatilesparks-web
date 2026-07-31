# Conflict Resolution Policy v1
═══════════════════════════════

How the framework resolves disagreements between skills, data sources, or reasoning paths.

---

## Resolution Hierarchy

```
1. Verified Measurements
   ├─ Reproducible data beats estimated data
   ├─ Instrumented metrics beat modeled projections
   └─ Primary sources beat secondary sources

2. Project Conventions
   ├─ Project-specific policies beat general best practices
   ├─ Existing architecture patterns beat theoretical improvements
   └─ Team-documented standards beat external benchmarks

3. Architectural Consistency
   ├─ System-wide invariants beat local optimizations
   ├─ Established interfaces beat novel abstractions
   └─ Proven patterns beat experimental approaches

4. Official Documentation
   ├─ Vendor documentation beats community guides
   ├─ API specifications beat blog posts
   └─ Standard specifications beat interpreted summaries

5. Community Consensus
   ├─ Widely adopted patterns beat niche approaches
   ├─ Long-standing practices beat recent trends
   └─ Peer-reviewed approaches beat individual recommendations

6. Model Reasoning
   ├─ First-principles reasoning beats analogy
   ├─ Traceable logic beats intuitive conclusions
   └─ Worst-case analysis beats average-case assumptions
```

## When Two Skills Disagree

```
Skill A output ────┐
                    ├── Conflict Detector
Skill B output ────┘        │
                            ▼
                    Resolution Engine
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       Clear Winner    Partial Truth    Irreconcilable
             │              │              │
             ▼              ▼              ▼
      Use A or B     Merge with       Document both
                     attribution     + recommend one
                                         │
                                         ▼
                                    Escalate if
                                    high impact
```

### Clear Winner
One skill's output is strictly better on all relevant criteria.
→ Use the winner. Document why.

### Partial Truth
Each skill captures part of the truth.
→ Merge results with explicit attribution.
→ Flag unresolved tension for the user.

### Irreconcilable
Skills produce truly contradictory results with equal evidence.
→ Present both options with tradeoffs.
→ Recommend one with rationale.
→ Escalate to user if decision is irreversible.

## Evidence Quality Scale

```
Level 1: Verified by direct measurement or primary source
Level 2: Verified by multiple independent secondary sources
Level 3: Supported by official documentation
Level 4: Supported by community consensus
Level 5: Supported by reasoned argument
Level 6: Asserted without evidence
```

Prefer Level 1 over Level 6. Always.

## Uncertainty Handling

When evidence is insufficient for a confident decision:

1. State what is known
2. State what is uncertain
3. State the range of possible outcomes
4. Recommend based on the most likely outcome
5. Monitor for evidence that confirms or contradicts

### Confidence Labels

| Label | Threshold | Meaning |
|-------|-----------|---------|
| High | >90% | Multiple verified sources agree. Decision is robust. |
| Medium | 70-90% | Most evidence points this way but some uncertainty remains. |
| Low | 50-70% | Best available evidence points this way but significant uncertainty. |
| Speculative | <50% | Informed guess. Treat as hypothesis, not conclusion. |

## Resolution Output Format

When conflict is resolved:

```markdown
## Conflict Resolution

**Disagreement:** [What disagreed]

**Resolution:** [Decision made]

**Rationale:**
- [Criterion 1] → [How it favored the chosen option]
- [Criterion 2] → [How it favored the chosen option]

**Confidence:** [High/Medium/Low/Speculative]

**If wrong, because:** [What would prove this decision wrong]
```
