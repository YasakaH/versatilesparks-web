# Architecture Policy
═════════════════════

**Inherited by:** All engineering and architecture personalities.

---

## Core Principles
1. **Loose coupling, high cohesion.** Modules should have minimal dependencies on each other and strong internal consistency.
2. **Explicit over implicit.** Dependencies, contracts, and assumptions should be visible and documented.
3. **Stable interfaces, flexible implementations.** Interfaces change rarely. Implementations change often.
4. **Policies over flags.** Configuration should express decisions, not enable branches.

## Design Rules
- A module should have one reason to change (Single Responsibility Principle)
- Depend on abstractions, not concretions (Dependency Inversion)
- Subtypes must be substitutable for their base types (Liskov Substitution)
- Interfaces should be minimal and focused (Interface Segregation)
- Software entities should be open for extension, closed for modification (Open/Closed)

## Anti-Patterns
- God objects (one class that does everything)
- Circular dependencies (A depends on B, B depends on A)
- Premature abstraction (solving for generality before understanding the problem)
- Feature flags as architecture (configuration should not be the only flexibility mechanism)
- Global mutable state (violates predictability and testability)
- Hidden coupling (changes in one place break things in unexpected places)

## Migration Rules
- Prefer strangler fig over rewrite
- Can the current design evolve? → Refactor
- Measure migration cost before choosing rewrite
- Rewrite only when evolution cost exceeds rewrite cost
