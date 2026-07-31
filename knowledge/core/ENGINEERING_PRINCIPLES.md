# ENGINEERING_PRINCIPLES.md

## Purpose

Engineering habits and heuristics that every Hermes engineer persona internalizes. These guide how code is written, reviewed, and maintained — day to day.

## Core Principles

### Prefer Deletion over Addition
The best line of code is the one you delete. Before adding new code, ask: can I remove or simplify existing code instead?

### Prefer Configuration over Hard-Coding
Anything that varies between environments, users, or time should be configurable — not hard-coded.

### Prefer Policy over Branching
Replace `if/else` on roles/environments with policy objects. Policies are testable, combinable, and auditable.

### Prefer Interfaces over Implementations
Depend on abstractions, not concrete implementations. This makes testing and swapping implementations trivial.

### Avoid Premature Abstraction
Duplicate once — it's fine. Duplicate twice — refactor. Duplicate three times — it's a pattern. Do not abstract on first occurrence.

### Measure Before Optimizing
Never optimize without profiling. Your intuition about bottlenecks is usually wrong.

### Optimize Bottlenecks, Not Everything
Find the slowest part of the system and optimize that. Optimizing non-bottlenecks is wasted effort.

### Minimize Coupling
Every dependency is a liability. If you can reduce coupling without sacrificing correctness, do it.

### Maximize Cohesion
Related behavior should live together. Unrelated behavior should not. If a module does two unrelated things, split it.

### Prefer Explicit over Magic
Implicit behavior (automatic routing, global state, monkey patching) creates systems that are hard to debug. Explicit code is boring but safe.

## Coding Standards

- **Error handling**: Never ignore errors. If you can't handle it, propagate it with context.
- **Logging**: Log entry, exit, and errors. Use structured logging, not strings.
- **Testing**: Write tests alongside code. Test behavior, not implementation.
- **Documentation**: Document why, not what. The code already says what it does.
- **Naming**: Names should reveal intent. If you need a comment to explain what a variable means, rename it.
- **Functions**: Small, single-purpose, with clear names. If a function does two things, split it.
- **State**: Minimize mutable state. Prefer pure functions that take input and return output.

## Review Checklist

When reviewing code, check in this order:

1. Does it solve the right problem?
2. Is it correct?
3. Is it safe?
4. Is it maintainable?
5. Is it performant enough?
6. Is it tested?
7. Is it well-named and well-structured?
8. Is it documented appropriately?
