import os

BONUS = "."

# ============================================================
# 1. Pattern Relationships appendix
# ============================================================

path = os.path.join(BONUS, "automation-pattern-catalog.md")
content = open(path, encoding="utf-8").read()

relationships_appendix = """

---

## Appendix — Pattern Relationships

### Dependency Map

Every pattern either depends on or enhances another. Understanding these relationships helps you compose patterns into architectures.

```text
Polling
    │
    ├── depends on → Retry with Backoff (transient failures)
    │
    └── evolves to → Event Observer (real-time needs)
    
Queue
    │
    ├── depends on → Idempotent Consumer (safe retry)
    ├── depends on → Dead Letter Queue (failed items)
    │
    └── evolves to → Fan-out/Fan-in (multi-worker)

Worker Pool
    │
    ├── depends on → Queue (work distribution)
    ├── depends on → Semaphore (bounded concurrency)
    │
    └── enhances → Producer-Consumer (bounded workers)

Circuit Breaker
    │
    ├── depends on → Retry with Backoff (base retry)
    │
    └── enhances → Supervisor (prevents crash loops)

Checkpoint/Resume
    │
    ├── depends on → Idempotent Consumer (safe resume)
    │
    └── evolves to → Checkpoint with Saga (full recovery)

Supervisor
    │
    ├── depends on → Retry with Backoff (worker restart)
    ├── depends on → Checkpoint/Resume (state preservation)
    │
    └── enhances → Worker Pool (pool health)

Saga
    │
    ├── depends on → Checkpoint/Resume (mid-run state)
    │
    └── enhances → Pipeline (transactional stages)

Pipeline
    │
    ├── depends on → Queue (stage buffering)
    ├── depends on → Dead Letter Queue (failed records)
    │
    └── evolves to → Saga (cross-stage rollback)
```

### Pattern Families

| Family | Patterns | Common Goal |
|--------|----------|-------------|
| **Execution** | Polling, Queue, Worker Pool, Producer-Consumer | How work gets done |
| **Resilience** | Retry, Circuit Breaker, Checkpoint, Saga | How failures are handled |
| **Monitoring** | Supervisor, Event Observer, Dead Letter Queue | How the system is observed |
| **Data** | Pipeline, Idempotent Consumer, Fan-out/Fan-in | How data flows through the system |
| **Advanced** | Checkpoint with Saga | Maximum reliability |

### Complexity Heat Map

| Pattern | Implementation | Operational Cost | Scalability |
|---------|---------------|------------------|-------------|
| Polling | Low | Low | Medium |
| Queue | High | Medium | High |
| Worker Pool | Medium | Medium | High |
| Producer-Consumer | High | Low | High |
| Circuit Breaker | High | Medium | High |
| Retry with Backoff | Low | Low | Medium |
| Checkpoint/Resume | Medium | Low | High |
| Idempotent Consumer | Low | Low | High |
| Fan-out/Fan-in | Medium | Medium | Very High |
| Supervisor | Low | Low | Medium |
| Saga | Very High | Very High | High |
| Event Observer | High | Medium | High |
| Pipeline | Low | Low | High |
| Dead Letter Queue | Low | Medium | Medium |
| Checkpoint with Saga | Very High | Very High | Very High |
"""

if "## Appendix — Pattern Relationships" not in content:
    # Insert before Key Principles
    kp_marker = "## Key Principles"
    idx = content.find(kp_marker)
    if idx != -1:
        content = content[:idx] + relationships_appendix + "\n\n" + content[idx:]
        open(path, "w", encoding="utf-8").write(content)
        print("Pattern Relationships appendix added")

# ============================================================
# 2. Reader Roadmap for Production Reference Library
# ============================================================

path = os.path.join(BONUS, "Production Reference Library.md")
content = open(path, encoding="utf-8").read()

roadmap_section = """

---

## Reader Roadmap

Not sure where to start? Follow your experience level:

| If you are... | Start here | Then read |
|--------------|------------|-----------|
| **New to browser automation** | Main Book (V2 Chapters 1-5) | Architecture Guide → Pattern Catalog |
| **Have built automations** | Architecture Guide (Decisions 1-8) | Pattern Catalog → Failure Playbook |
| **Running automations in production** | Failure Playbook → War Stories | Architecture Guide → Design Review |
| **Designing a new system** | Architecture Guide (All decisions) | Pattern Catalog → Design Review |
| **Debugging a failure right now** | War Stories (symptom match) | Failure Playbook (relevant pattern) |
| **Reviewing a teammate's design** | Design Review Checklist | Architecture Guide (decisions that apply) |
| **Scaling an existing system** | Scaling Roadmap (Part VII) | Architecture Guide (next architecture) |

### Quick Start Paths

**Path: Build your first production automation (1 week)**

```
Architecture Guide → Choose Decision 1-4 → Pattern Catalog → Polling + Retry
→ Failure Playbook → Patterns 1, 3, 4, 6 → Design Review → Deploy
```

**Path: Debug a failing automation (1 day)**

```
Failure Playbook → Symptom → Pattern → Recovery Fix → Verify
→ War Stories → Similar incident → Lesson
```

**Path: Scale from 1 to 10 automations (1 month)**

```
Architecture Guide → Decision 12 → Architecture B → Pattern Catalog
→ Queue → Worker Pool → Supervisor → Design Review → Deploy
```

### When to Read Each Document

```
First time?                          → Main Book
Choosing an approach?                 → Architecture Guide → Pattern Catalog
Something is broken?                  → Failure Playbook
Need to verify a design?              → Design Review Checklist
Want to learn from real failures?     → War Stories
Building a team or training someone?  → Entire Reference Library
```
"""

if "## Reader Roadmap" not in content:
    # Insert before the table of "When to Read Each Guide"
    marker = "### How the Guides Map to Maturity Levels"
    idx = content.find(marker)
    if idx != -1:
        content = content[:idx] + roadmap_section + "\n\n" + content[idx:]
        open(path, "w", encoding="utf-8").write(content)
        print("Reader Roadmap added to PRL")

# ============================================================
# 3. Final cleanup: remove temp scripts
# ============================================================

print("Pattern Relationships + Roadmap complete")
