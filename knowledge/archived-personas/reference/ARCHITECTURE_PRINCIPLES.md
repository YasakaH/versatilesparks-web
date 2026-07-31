> Originally from CORE/ARCHITECTURE_PRINCIPLES.md

# ARCHITECTURE_PRINCIPLES.md

## Purpose

Define the architectural principles every Hermes agent applies when designing, evaluating, or modifying systems. These are universal — they apply regardless of domain, language, or framework.

## Principles

### 1. Deep Modules over Shallow Modules
Prefer modules that hide complexity behind simple interfaces. A deep module does one thing well and has a simple API relative to the complexity it manages.

### 2. Composition over Inheritance
Favor assembling behavior from small, interchangeable parts over deep class hierarchies. Composition is easier to test, change, and reason about.

### 3. Loose Coupling, High Cohesion
Modules should have minimal dependencies on each other (loose coupling) and strong internal relatedness (high cohesion).

### 4. Explicit over Implicit
Make dependencies, side effects, and data flow visible. Magic (automatic behavior) is convenient but makes systems unpredictable.

### 5. Policies over Flags
Replace boolean flags with explicit policy objects. A flag like `enabled: true` becomes a policy like `rate_limit: { max: 100, window: 60s }`.

### 6. Immutable State Where Possible
Prefer immutable data structures. When state must change, make the transition explicit and atomic.

### 7. Idempotency
Design operations so they can be safely retried. The same input should always produce the same outcome.

### 8. Fail Fast, Fail Clearly
Validate inputs early. When something goes wrong, produce a clear error message — not a cryptic exception or silent no-op.

### 9. Observability First
Every component should expose: what it's doing, how long it took, what errors occurred, and what it depends on. Log events, not just errors.

### 10. You Aren't Gonna Need It (YAGNI)
Build what you need now, not what you might need later. Premature abstraction is the root of most over-engineering.

### 11. Keep It Simple, Stupid (KISS)
The simplest solution that satisfies requirements is usually the best. Complexity should be justified by necessity, not cleverness.

### 12. Don't Repeat Yourself (DRY)
Every piece of knowledge should have a single, unambiguous representation. But prefer duplication over the wrong abstraction.

## Domain-Specific Extensions

| Domain | Additional Principles |
|--------|----------------------|
| Frontend | Progressive enhancement, accessibility first, mobile-first |
| Backend | Stateless when possible, database-as-boundary, API-first |
| Data | Immutable data lake, schema-on-read, idempotent pipelines |
| Security | Least privilege, defense in depth, zero trust |
| AI/ML | Reproducible experiments, data versioning, model governance |
