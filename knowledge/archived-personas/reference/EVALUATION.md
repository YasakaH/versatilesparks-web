> Originally from CORE/EVALUATION.md

# Evaluation Suite v1
══════════════════════

Standardized benchmarks for every personality and skill.

---

## Personality Benchmarks

Every personality must pass benchmark tasks for its domain.

### Format
```yaml
benchmark:
  personality: principal-engineer
  version: 1.0.0
  
  tasks:
    - id: arch-review-001
      name: "Monolith decomposition recommendation"
      input: "10-service monolith, team of 12 engineers, 3-year codebase"
      expected_workflow:
        - repository-analysis
        - architecture-review
        - dependency-mapping
      expected_output_types:
        - bounded_contexts
        - interface_contracts
        - migration_plan
      quality_gates:
        - loose_coupling_improved: boolean
        - interface_stability: boolean
        - migration_failure_modes: boolean
      pass_criteria:
        - "All expected workflow skills invoked"
        - "All quality gates pass"
        - "No constitution violations"
  
    - id: tech-debt-002
      name: "Technical debt assessment"
      input: "Python monolith, 500K LOC, 80% test coverage"
      expected_workflow:
        - repository-analysis
        - technical-debt-analysis
        - code-review
      quality_gates:
        - debt_categorized: boolean
        - remediation_prioritized: boolean
        - tradeoffs_documented: boolean
```

### Benchmark Categories

| Category | Tasks | Pass Criteria |
|----------|-------|---------------|
| Engineering | 10 tasks | All skills invoked, all quality gates pass |
| Architecture | 8 tasks | Clear boundaries, documented tradeoffs |
| AI | 8 tasks | Reliable outputs, cost budgets respected |
| Research | 6 tasks | Evidence hierarchy respected |
| Security | 6 tasks | Threats identified, mitigations proposed |
| Marketing | 5 tasks | Audience defined, positioning clear |

## Skill Benchmarks

Every skill must pass unit tests for its inputs/outputs.

```yaml
skill_benchmark:
  skill: architecture-review
  version: 1.0.0
  
  tests:
    - id: arch-unit-001
      name: "Two-service dependency analysis"
      input: {repos: ["service-a", "service-b"]}
      expected_output_contains: ["dependency", "interface", "coupling"]
      expected_confidence_above: 0.7
  
    - id: arch-unit-002
      name: "Empty repository"
      input: {repos: []}
      expected_error: "No repository data provided"
  
    - id: arch-unit-003
      name: "Large monolith (100K LOC)"
      input: {repos: ["monolith"], analysis_depth: "shallow"}
      expected_duration_below_ms: 30000
      expected_output_contains: ["boundaries", "recommendations"]
```

## Regression Detection

Run benchmarks weekly. Alert on:
- Personality success rate drop > 10%
- Skill failure rate increase > 5%
- Confidence score drop > 0.15
- Duration increase > 50%
- Cost increase > 50%

## New Personality Validation

Before a new personality is registered:

1. **Schema validation** — all required fields present
2. **Constitution check** — no violations
3. **Quality gate test** — all gates defined and testable
4. **Benchmark execution** — pass 3 domain-specific tasks
5. **Conflict check** — doesn't duplicate existing personality
6. **Registration** — added to capability registry
