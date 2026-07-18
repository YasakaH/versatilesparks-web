# Production Reference Library

## Browser Automation Engineering — Five-Volume Reference Set

---

### When to Read Each Guide

| Guide | Read This When... |
|-------|------------------|
| **Architecture Field Guide** | Designing a new automation system or deciding how to scale an existing one. |
| **Failure Playbook** | An automation is failing in production or you are designing recovery strategies. |
| **Pattern Catalog** | You know what you want to automate but aren't sure which architectural pattern to choose. |
| **Design Review Checklist** | You are about to write a new automation or reviewing an existing one. |
| **War Stories** | You want to learn from other people's production incidents without experiencing them yourself. |

---

### Automation Engineering Maturity Model

Use this model to assess your current level and plan your growth path.

| Level | Name | Monitoring | Recovery | Testing | Deployment | Workers | Profiles | Scaling |
|-------|------|-----------|----------|---------|------------|---------|----------|---------|
| 1 | **Script** | None (manual check) | None | Manual | Laptop | 1 | 1 | None |
| 2 | **Reliable Script** | Log files | Manual restart | Basic unit tests | Virtualenv | 1 | 1 | Manual |
| 3 | **Production Automation** | Exit code + Slack | Auto-restart on crash | Integration tests | Docker | 1-3 | Per-worker | Vertical |
| 4 | **Automation Service** | Data volume + runtime | Recovery manager | Regression suite | CI/CD | Pool (3-10) | Isolated | Horizontal |
| 5 | **Automation Platform** | SLA dashboards | Circuit breakers + DLQ | Performance + chaos | Automated rollback | Auto-scaling | Managed | Auto-scaling |
| 6 | **Automation Fleet** | Cost per run + anomaly | Self-healing fleet | Full QA | GitOps | 100+ | Fleet-managed | Multi-region |

**Which level are you?** Find your current state in the left column. The target for most commercial automations is Level 3-4. Level 5-6 is for platforms that ARE the business.

---



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


### How the Guides Map to Maturity Levels

| Guide | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 | Level 6 |
|-------|---------|---------|---------|---------|---------|---------|
| Architecture Field Guide | Decision 1-4 | Decision 5-7 | Decision 8-10 | Architecture B-C | Architecture D | Scaling Stage 5-6 |
| Failure Playbook | Pattern 1-2 | Pattern 3-5 | Pattern 6-8 | Pattern 9-12 | Pattern 13-15 | Recovery Tree |
| Pattern Catalog | Polling, Retry | Queue, Checkpoint | Worker Pool, Circuit Breaker | Saga, Fan-out/fan-in | Supervisor, DLQ | Event Observer |
| Design Review Checklist | Pre-Flight | Full Review | Production Readiness | Post-Implementation | Enterprise | Fleet |
| War Stories | 1-5 | 6-10 | 11-15 | 16-18 | 19-20 | — |

---

### Quick Reference — Decision Index

**Architecture Field Guide**

| I need to decide... | Go to |
|-------------------|-------|
| One browser or many? | Decision 1 |
| Tabs or separate processes? | Decision 2 |
| SQLite or PostgreSQL? | Decision 3 |
| Cron or scheduler? | Decision 4 |
| Docker or bare metal? | Decision 5 |
| Retry, recover, or restart? | Decision 6 |
| Profile per worker or shared? | Decision 7 |
| Browser profile or stateless? | Decision 8 |
| Browser automation or API? | Decision 9 |
| Build custom or buy a tool? | Decision 10 |
| Poll or event-driven? | Decision 11 |
| Queue or direct execution? | Decision 12 |
| Screenshot, HTML, or structured data? | Decision 13 |

**Pattern Catalog**

| I need to solve... | Go to |
|-------------------|-------|
| Periodic data collection | Polling |
| Decouple producer from consumer | Queue |
| Limit concurrent execution | Worker Pool |
| Parallel work aggregation | Fan-out/Fan-in |
| Protect failing systems | Circuit Breaker |
| Handle transient failures | Retry with Backoff |
| Resume after mid-run crash | Checkpoint/Resume |
| Make retry safe | Idempotent Consumer |
| Keep workers running | Supervisor |
| Roll back on failure | Saga |
| Observe browser events | Event Observer |
| Multi-stage data processing | Pipeline |
| Preserve failed items | Dead Letter Queue |
| Full recovery capability | Checkpoint with Saga |

**Failure Playbook**

| Symptom | Likeliest Pattern |
|---------|------------------|
| Chrome won't start | Pattern 1 |
| Profile locked | Pattern 2 |
| Session expired mid-run | Pattern 3 |
| Selector returns nothing | Pattern 4 |
| Page loads forever | Pattern 5 |
| CDP connection lost | Pattern 6 |
| All records fail validation | Pattern 7 |
| HTTP 429 / 403 | Pattern 8 |
| Container OOM (exit 137) | Pattern 9 |
| Quarantine file growing | Pattern 10 |
| 0 records extracted | Pattern 11 |
| Duplicate records | Pattern 12 |
| Blank page | Pattern 13 |
| Login suddenly fails | Pattern 14 |
| Profile corruption | Pattern 15 |

---

### Library Navigation Map

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION REFERENCE LIBRARY                     │
│                                                                     │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────────┐      │
│  │ Architecture  │──▶│    Pattern    │──▶│  Failure Playbook │      │
│  │  Field Guide  │   │    Catalog    │   │                   │      │
│  └───────┬───────┘   └───────┬───────┘   └────────┬──────────┘      │
│          │                   │                     │                │
│          │        ┌──────────┴──────────┐          │                │
│          │        │                     │          │                │
│          ▼        ▼                     ▼          ▼                │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    War Stories                               │   │
│  │         (Real incidents where every pattern broke)           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                         │                                          │
│                         ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Design Review Checklist                         │   │
│  │        (Apply everything before deploying)                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Quick Start

1. **Start here** if you are new: Read the Architecture Field Guide Part I (decisions)
2. **Choose a pattern** from the Pattern Catalog
3. **Check failure modes** in the Failure Playbook
4. **Validate your design** with the Design Review Checklist
5. **Learn from real incidents** in the War Stories
