# Browser Automation Architecture Field Guide

> **Read This If...**
> You are designing a new automation system or deciding how to scale an existing one. This guide helps you choose between competing architectures, understand tradeoffs, and avoid common design mistakes.

---

## Decision Matrices, Reference Architectures, and Scaling Roadmaps

### How to Use This Guide

This guide is organized as a reference. When designing a new automation system or debugging an existing one:

1. Find the decision matrix for the question you are answering
2. Read the Engineering Principle, then check the Decision table
3. Review the Example and Common Mistake
4. Use the Production Rule as your design constraint

---> **Quick Take**
> If you're short on time:
> - [Y] Use one profile per worker. Never share.
> - [Y] Start with SQLite. Migrate to PostgreSQL only when needed.
> - [Y] Classify failures before choosing retry strategy.
> - [Y] Monitor data volume, not just exit codes.
> - [Y] Docker > bare metal for any deployed automation.
> 
> Estimated reading: 12 minutes
> 



## PART I — DECISION MATRICES

Each matrix follows the same structure:

```
Engineering Principle → Decision Table → Example → Common Mistake → Production Rule
```

---

### Decision 1 — Single Browser vs Multiple Browsers

**Engineering Principle:** Isolation costs memory but prevents cascading failures. One browser per identity is the default. Sharing a browser across identities is an optimization — never a starting point.

**Complexity:** ■□□□□□ | **Operations:** ■□□□□□ | **Scalability:** ■■□□□□


| Factor | Single Browser | Multiple Browsers |
|--------|---------------|-------------------|
| Memory | ~500MB | ~500MB per browser |
| Isolation | Tabs share cookies, storage | Completely isolated |
| Concurrency | Sequential | Parallel |
| Profile management | One profile | One per browser |
| Complexity | Simple | Lock files, coordination |

**Example:** Scraping a single marketplace catalog with one account → single browser. Scraping the same marketplace with 3 different accounts → 3 browsers, 3 profiles.

**Common Mistake:** Sharing one browser across 10 accounts in 10 tabs. When one account logs out, the cookie is invalid for all 10.

**Production Rule:** Use a single browser for multi-page extraction from one site. Use multiple browsers when you need account isolation or parallel extraction from different sites.

---

### Decision 2 — Tabs vs Browser Processes

**Engineering Principle:** Tabs share a process and crash domain. Browser processes are fully isolated. Choose isolation level based on crash tolerance, not convenience.

**Complexity:** ■■□□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■□□□


| Factor | Multiple Tabs | Multiple Processes |
|--------|--------------|-------------------|
| Memory | Shared, lower overhead | Isolated, higher overhead |
| Crash isolation | One tab crash can crash the process | Process crash does not affect others |
| Profile sharing | Same cookies/session | Completely separate |
| Coordination | Same event loop | Need IPC or queue |
| Startup cost | One launch, N tabs | N launches |

**Example:** Price comparison on one marketplace → tabs (faster, lower memory). Automating two client CRMs → separate processes (client isolation).

**Common Mistake:** Using tabs for different accounts. A logout in one tab invalidates the session cookie for all tabs.

**Production Rule:** Use tabs for parallel work at the same domain. Use separate processes for different identities.

---

### Decision 3 — SQLite vs PostgreSQL

**Engineering Principle:** Storage choice is driven by concurrency requirements. Single-writer workloads do not benefit from client-server databases.

**Complexity:** ■■□□□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■■□□


| Factor | SQLite | PostgreSQL |
|--------|--------|------------|
| Setup | File-based, zero config | Server install, connection string |
| Concurrency | Single writer, multiple readers | Multiple concurrent writers |
| Performance | Fast for single worker | Fast for many workers |
| Scale limit | ~100 concurrent readers | Thousands of connections |
| Operational cost | Low — no server | Medium — requires maintenance |

**Example:** Price monitor with one worker → SQLite. Agency platform with 5 concurrent workers writing results → PostgreSQL.

**Common Mistake:** Deploying PostgreSQL on day one for a single-worker automation. Adds server maintenance for zero concurrency benefit.

**Production Rule:** Start with SQLite. Migrate to PostgreSQL when you have multiple writers or the database outgrows ~10GB.

---

### Decision 4 — Cron vs Dedicated Scheduler

**Engineering Principle:** Scheduling is coordination, not time. A scheduler that overlaps jobs is worse than no scheduler at all.

**Complexity:** ■□□□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■□□□


| Factor | Cron | Dedicated Scheduler |
|--------|------|---------------------|
| Setup | One line in crontab | Requires configuration |
| Precision | Minute-level | Second-level |
| Locking | Not built-in | Job locking, concurrency control |
| History | No built-in logging | Run history, failure tracking |
| Recovery | No retry after downtime | Catch-up after missed runs |

**Example:** A single daily report → cron is sufficient. 10 jobs with inter-job dependencies → scheduler with run history.

**Common Mistake:** Using cron without a lock file. The cron fires again before the previous run finishes, producing duplicate records.

**Production Rule:** Use cron with `filelock` for single-job automations. Use a dedicated scheduler when you need run history, dependency management, or catch-up after downtime.

---

### Decision 5 — Docker vs Bare Metal

**Engineering Principle:** Reproducibility is more valuable than convenience. Docker guarantees the same environment in development and production.

**Complexity:** ■■■□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■■■□


| Factor | Docker | Bare Metal |
|--------|--------|------------|
| Reproducibility | Exact same environment | Depends on OS and packages |
| Chrome version | Pinned in Dockerfile | Shared system Chrome |
| Deployment | `docker pull && docker run` | `git pull && pip install` |
| Resource limits | Built-in (CPU, memory) | Manual |
| Profile persistence | Volume mount | Direct filesystem |

**Example:** Client deployment → Docker (they get the exact same Chrome, Python, and dependencies). Personal script → virtualenv is fine.

**Common Mistake:** Running `pip install` on the server without pinning versions. Next month's dependency update breaks the automation silently.

**Production Rule:** Use Docker for any automation deployed to a server. Use bare metal only for local development.

---

### Decision 6 — Retry vs Recover vs Restart

**Engineering Principle:** The response to failure must match the failure class. The wrong response is worse than no response.

**Complexity:** ■■□□□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■■□□


| Failure Type | Strategy | When to Use |
|-------------|----------|-------------|
| Network timeout | Retry | Transient — will likely succeed |
| Browser crash | Restart | Full state loss — start fresh |
| Session expired | Recover (re-login) | Partial state loss — resume |
| Selector missing | Stop and alert | Permanent — never succeed on retry |
| All records fail validation | Stop and alert | Systematic — retry produces same result |

**Example:** Timeout → retry with backoff (90% succeed on second try). Selector missing → never retry, always alert a human.

**Common Mistake:** Retrying a login failure 5 times. The account gets locked. The failure was permanent (wrong password), not transient.

**Production Rule:** Classify every failure before choosing a strategy. Transient → retry. State-loss → restart. Permanent → escalate.

---

### Decision 7 — Profile per Worker vs Shared Profile

**Engineering Principle:** Storage is cheap. Debugging is expensive. One profile per worker eliminates an entire class of production bugs.

**Complexity:** ■□□□□□ | **Operations:** ■□□□□□ | **Scalability:** ■■■■□□


| Factor | Profile per Worker | Shared Profile |
|--------|-------------------|----------------|
| Isolation | Complete | None — state leaks between workers |
| Concurrency | Unlimited | One writer at a time |
| Disk usage | ~50MB per worker | ~50MB total |
| Session management | Independent | Shared — one logout logs out all |
| Schema complexity | Simple | Lock management, corruption recovery |

**Example:** 10 workers → 10 profiles at 500MB total. One corrupted profile → one worker affected, not all 10.

**Common Mistake:** Sharing one profile across 5 workers to "save disk space." When one worker's login fails, all 5 fail because the corrupted cookie affects the shared profile.

**Production Rule:** Always use one profile per worker. Shared profiles are never worth the disk savings.

---

### Decision 8 — Browser Profiles vs Stateless Sessions

**Engineering Principle:** Profiles persist complete browser state (cookies, storage, extensions). Sessions persist only authentication. Choose based on how much state the target application depends on.

**Complexity:** ■■□□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■□□□


| Factor | Browser Profile | Stateless Session (Cookies) |
|--------|----------------|----------------------------|
| State persisted | Everything (cookies, IndexedDB, cache, extensions) | Only authentication cookies |
| Startup time | Slower (load profile) | Faster (inject cookies) |
| Portability | Chrome-version-sensitive | Portable across Chrome versions |
| Corruption risk | Higher (profile can corrupt) | Lower (cookie file is smaller) |
| Recovery | Delete profile, re-authenticate | Clear cookies, re-authenticate |

**Example:** A banking portal that uses IndexedDB for session state → full profile required. A REST API that authenticates with a JWT cookie → stateless session is sufficient.

**Common Mistake:** Using a full browser profile when a cookie file would suffice. Profile corruption causes random failures that are harder to diagnose than cookie expiry.

**Production Rule:** Use a full browser profile only when the application stores state outside cookies. Use cookie-only persistence for everything else — it is faster, more portable, and less prone to corruption.

---

### Decision 9 — Browser Automation vs API Integration

**Engineering Principle:** A browser is the most expensive way to get data. Use it only when APIs are unavailable or insufficient.

**Complexity:** ■□□□□□ | **Operations:** ■□□□□□ | **Scalability:** ■■■■□□


| Situation | Best Choice | Reason |
|-----------|-------------|--------|
| Public REST API | API call | One HTTP request vs a full browser |
| Authenticated dashboard | Browser | No API available |
| Heavy JS SPA | Browser with CDP | API calls embedded in page |
| Login + file download | Browser | Download triggered by browser events |
| Simple data feed | API or fetch from page | No browser needed |
| CAPTCHA-protected page | Manual workflow | Neither approach works reliably |

**Example:** A supplier has a public product API → use `requests.get()`. A supplier only has a JavaScript-rendered dashboard → use nodriver with CDP network monitoring.

**Common Mistake:** Writing a full browser automation for a site that has a documented API. The browser automation will be slower, more fragile, and harder to maintain than a simple API call.

**Production Rule:** Before writing any automation, check for an API. If one exists, use it. Reserve browser automation for sites that require it.

---

### Decision 10 — Build vs Buy (Automation Tooling)

**Engineering Principle:** Your time is expensive. If a tool exists that solves 80% of your problem, use it. Build only when the remaining 20% is critical to your business.

**Complexity:** ■□□□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■■■□


| Situation | Choose | Reason |
|-----------|--------|--------|
| Simple form filling | n8n / Zapier | No-code, hosted, 5-minute setup |
| API integration | n8n / Make | 500+ connectors, scheduling built-in |
| Complex browser automation | nodriver / Playwright | Full control, CDP access, custom logic |
| Cross-browser testing | Playwright | Mature testing ecosystem |
| Enterprise compliance | Selenium Grid | Legacy enterprise requirement |
| Internal RPA | nodriver | Lightweight, Python-native |

**Example:** A marketing team needs to pull data from 3 SaaS dashboards → n8n (1 hour setup vs 3 days coding). A pricing team needs to scrape 50 competitor product pages with anti-bot circumvention → nodriver (requires full browser control).

**Common Mistake:** Building a custom automation framework when Zapier/n8n would work. The build cost is 10x the tool cost for simple workflows.

**Production Rule:** Use tools for standard integrations. Build only when the workflow requires browser-level control, custom CDP event handling, or proprietary anti-bot strategies.

---

### Decision 11 — Polling vs Event-Driven Extraction

**Engineering Principle:** Polling is reliable and simple. Event-driven is fast and efficient. Choose reliability over speed when data completeness is critical.

**Complexity:** ■■■□□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■■□□


| Factor | Polling | Event-Driven (CDP) |
|--------|---------|-------------------|
| Latency | Seconds to minutes | Milliseconds |
| Reliability | Simple, predictable | Complex, race conditions |
| Resource usage | High (full page load) | Low (observe network) |
| Data completeness | Full page state every time | May get partial state |
| Implementation | `asyncio.sleep` + `browser.get()` | CDP event subscription |

**Example:** Daily competitor price check → polling (reliable, simple). Real-time stock ticker → CDP network monitoring (low latency).

**Common Mistake:** Using CDP events for a daily batch extraction. The event handler complexity adds no value when polling once per day works reliably.

**Production Rule:** Use polling for periodic data collection. Use event-driven CDP when you need sub-second latency or are monitoring live streams.

---

### Decision 12 — Queue vs Direct Execution

**Engineering Principle:** A queue decouples work production from consumption. Add a queue only when the producer and consumer operate at different speeds or when crash resilience is required.

**Complexity:** ■■■■□□ | **Operations:** ■■■■□□ | **Scalability:** ■■■■■□


| Factor | Direct Execution | Async Queue |
|--------|-----------------|-------------|
| Latency | Immediate | Buffered |
| Backpressure | None (blocks caller) | Built-in (bounded queue) |
| Crash resilience | Work lost on crash | Work preserved in queue |
| Complexity | None | Queue management |
| Throughput | Single-threaded | Configurable parallelism |

**Example:** Single-worker, single-target → direct execution (simpler). 10 workers, 50 jobs, need crash resilience → Redis queue.

**Common Mistake:** Adding Redis on day one for a single-worker automation. The queue adds operational complexity and latency for zero benefit.

**Production Rule:** Use direct execution for single-worker automations. Add a queue when you have multiple workers or need crash resilience.

---

### Decision 13 — Screenshot vs HTML Dump vs Structured Data

**Engineering Principle:** Evidence is not validation. Choose the evidence format based on what question it answers, not how impressive it looks.

**Complexity:** ■□□□□□ | **Operations:** ■□□□□□ | **Scalability:** ■□□□□□


| Evidence Type | Size | Best For |
|--------------|------|----------|
| Screenshot | 200-500KB | Visual layout debugging, proving page loaded |
| HTML dump | 50-200KB | Checking element existence, structural comparison |
| Structured data | 1-10KB/record | Validation, storage, downstream consumption |

**Example:** After a failure → capture all three (screenshot + HTML + console). In normal operation → store only structured data.

**Common Mistake:** Replacing data validation with screenshots. A screenshot shows the page rendered; it does not prove the price is ₹89,999.

**Production Rule:** Store structured data as the primary output. Save screenshots only on failure. Use HTML dumps for structural comparison between runs.

---

## PART II — ARCHITECTURE SMELLS

Recognizing a bad architecture early saves weeks of rework. These patterns are not always wrong, but they should trigger an immediate review.

### Smell 1 — One Profile Used by 8 Workers

```
profiles/
  shared/          ← 8 workers read/write here
```

**Why it hurts:** Profile corruption affects all 8 workers simultaneously. One logout logs out everyone. Session errors appear random and are impossible to reproduce.

**Fix:** One profile per worker.

### Smell 2 — Chrome Restarted Before Every Page

```python
for url in urls:
    browser = await launch_browser()  ← Every. Single. Page.
    page = await browser.get(url)
    await close_browser(browser)
```

**Why it hurts:** Chrome takes 3-5 seconds to start. Scraping 100 pages adds 5 minutes of startup overhead. Profiles cannot persist state.

**Fix:** Launch once, navigate through all pages, close once.

### Smell 3 — One Database per Automation

```
automations/
  price_monitor/
    data.db
  supplier_check/
    data.db
  reporting/
    data.db
```

**Why it hurts:** Cannot query across automations. Each database needs its own backup, monitoring, and cleanup script. Reporting across targets requires manual data merging.

**Fix:** One database with per-target schemas or a shared PostgreSQL instance.

### Smell 4 — Microservices for Two Automation Jobs

```
services/
  price-extractor/    ← runs on its own container
  price-validator/    ← separate container
  price-storer/       ← separate container
  price-alerter/      ← separate container
```

**Why it hurts:** Splitting a single-threaded batch job into 4 services adds network calls, serialization overhead, deployment coordination, and distributed debugging complexity. The system does less work than the monolith version.

**Fix:** One process with internal modules. Split only when scale requires independent deployment.

### Smell 5 — Same Credentials in 8 Different Places

```
price_monitor.py:        LOGIN = "admin@example.com"
supplier_check.py:       LOGIN = "admin@example.com"
reporting.py:             LOGIN = "admin@example.com"
```

**Why it hurts:** Changing credentials requires updating 8 files. One will be missed. The automation fails silently for that one target.

**Fix:** One `.env` file read by `common/config.py`.

### Smell 6 — No Idempotency Key

```python
async def process_lead(lead):
    await crm.create(lead)  ← Running twice creates 2 leads
```

**Why it hurts:** Any retry, manual re-run, or cron misfire produces duplicates. The database accumulates phantom records.

**Fix:** Natural key dedup — `company + email` as the identity.

### Smell 7 — Retrying Everything the Same Way

```python
@retry(max_attempts=5)
async def do_anything():
    ...  # Login, extract, download — all retried 5 times
```

**Why it hurts:** Selector failures retried 5 times (always fail). Login retried 5 times (account lockout). Only network timeouts benefit from retry.

**Fix:** Classify failures. Retry only transient ones.

---

## PART III — COST TABLE

| Architecture | Browsers | RAM | CPU | Storage | Best For |
|-------------|----------|-----|-----|---------|----------|
| Price Monitor | 1 | ~600MB | Low | 500MB | Single site, one worker |
| Reporting | 2 | ~1.5GB | Medium | 2GB | One site, concurrent reporting |
| Worker Pool (3) | 3 | ~3GB | High | 10GB | N suppliers, N profiles |
| Platform (5 jobs) | 5 | ~6GB | High | PostgreSQL | Multi-client, multi-target |
| Fleet (20+ jobs) | 20+ | ~16GB | Very High | Centralized + shards | 100+ automations |

### Estimated Costs

| Resource | Unit Cost |
|----------|-----------|
| Chrome process | ~300-500MB RAM |
| Browser profile | ~50MB disk (first run) |
| Per-run artifact | ~5MB (screenshot + HTML + logs) |
| Daily output (1000 products) | ~1MB structured data |
| VPS (4GB RAM) | ~$15-25/month |
| VPS (16GB RAM) | ~$60-100/month |

### Sizing Guide

```text
1 browser  + 1 profile   → 4GB VPS
3 browsers + 3 profiles  → 8GB VPS
5 browsers + 5 profiles  → 16GB VPS
10+ browsers             → 32GB VPS or multiple servers
```

---

## PART IV — CHOOSING COMPLEXITY

```text
Complexity
    ▲
    │                      ╱ Distributed Fleet
    │                    ╱
    │                  ╱
    │                ╱    Platform
    │              ╱
    │            ╱
    │          ╱ Production Automation
    │        ╱
    │      ╱
    │    ╱ Simple Script
    │  ╱
    │╱
    └──────────────────────────────────▶ Business Value
```

The curve is not linear. Each jump in complexity adds disproportionate operational cost.

| Level | Complexity | When to Stop |
|-------|-----------|-------------|
| Simple Script | Low | Automation runs only for you |
| Production Automation | Medium | Automation runs for a client |
| Platform | High | Automation runs a business process |
| Distributed Fleet | Very High | Automation IS the business |

The right level is the simplest one that covers your failure cost. If a client pays $500/month for an automation, do not build a $5,000/month platform to deliver it.

---

## PART V — ARCHITECTURE EVOLUTION

Four perspectives. Each answers a different question.

### Infrastructure (Chapter 12)

```text
Laptop → Docker → VPS → Cluster
```

**Question:** Where does the code run?

### Software Architecture (This Guide)

```text
Script → Automation → Worker Pool → Platform → Fleet
```

**Question:** How is the software structured?

### Operational Maturity (Part VII)

```text
1 job → 10 jobs → 100 jobs → 1000 jobs
```

**Question:** How many targets can we manage?

---



## Architecture Lifecycle

Every architecture follows the same lifecycle. Knowing where you are in it helps you plan:

```
Choose → Deploy → Observe → Scale → Replace
```

| Phase | Question | Activity |
|-------|----------|----------|
| **Choose** | What pattern fits? | Decision matrix (Part I) |
| **Deploy** | How do I run it? | Reference architectures (Part VI) |
| **Observe** | Is it working? | Monitoring, data volume, alerts |
| **Scale** | When do I upgrade? | Evolution triggers (Part VI) |
| **Replace** | When do I retire it? | Architecture killers (Part VI) |

**Choose:** An architecture is not permanent. Revisit the decision matrices every 6-12 months as your requirements evolve.

**Replace:** An architecture is ready for retirement when it triggers multiple Architecture Killers, requires more than 2 workarounds, or the team has lost confidence in it.


## PART VI — REFERENCE ARCHITECTURES

Each architecture includes the full design framework.

---

### Architecture A — Single-Website Price Monitor

**Engineering Principle:** The simplest architecture that meets requirements is the most maintainable.

**Failure Cost:** Low. Miss one run — the next run catches up. No data permanently lost.

```
Cron → Worker (nodriver) → Validation → SQLite → Slack Alert
```

| Decision | Choice | Why |
|----------|--------|-----|
| Storage | SQLite | Single writer |
| Execution | Cron | One job, minute precision fine |
| Browser count | 1 | One target, one account |

**Evolution Trigger:** When you add a second website. Two cron jobs running independently quickly become unmanageable.

**Architecture Killers:**
- [X] Needs sub-second latency (polling interval is minutes)
- [!] More than 3 websites (each needs its own job)
- [!] SLA > 99.9% (no redundancy, no failover)

**Example:** A single competitor price tracker, checked every 6 hours.

**Common Mistake:** Adding PostgreSQL and a web dashboard on day one for a script that runs once per day.

**Production Rule:** Start with the simplest architecture. Add complexity only when the requirements demand it.

---

### Architecture B — Multi-Supplier Intelligence Pipeline

**Engineering Principle:** Profile isolation is non-negotiable when each target has different authentication.

**Failure Cost:** Medium. One supplier's data loss costs that supplier's reports. Other suppliers unaffected.

```
Scheduler → Queue → Worker Pool (3 max) → Validation → PostgreSQL → Exports
```

| Decision | Choice | Why |
|----------|--------|-----|
| Storage | PostgreSQL | Multiple concurrent writers |
| Profiles | 1 per supplier | Authentication isolation |
| Workers | 2-3 max | 4GB VPS constraint |

**Evolution Trigger:** When worker count hits the VPS memory limit. Time to scale horizontally or upgrade the server.

**Architecture Killers:**
- [X] Single VPS under 4GB RAM (Chrome needs memory)
- [!] Synchronous processing required (queue adds async complexity)
- [!] Suppliers with sub-second SLA needs

**Example:** 25 suppliers, each with different portals and login methods.

**Common Mistake:** Running 25 concurrent Chrome processes on a 4GB VPS. Each Chrome needs ~500MB. Three is the safe limit.

**Production Rule:** Cap concurrent workers at a number your server can sustain. Scale horizontally, not vertically.

---

### Architecture C — Client Reporting Platform

**Engineering Principle:** A job registry separates configuration from code. Adding a new client should not require a code deployment.

```
Job Registry (YAML) → Scheduler → Worker Pool → Recovery → PostgreSQL → Alerts
```

| Decision | Choice | Why |
|----------|--------|-----|
| Job config | YAML | New client = new config file |
| Profiles | 1 per client | Each client has different credentials |
| Recovery | `common/recovery.py` | Each client's automation must survive independently |

**Example:** An agency managing automation for 12 clients.

**Common Mistake:** Putting client-specific URLs and credentials in the Python code. Adding a client requires a PR, review, and deployment.

**Production Rule:** Configuration that changes per client belongs in config files, not in Python code.

---

### Architecture D — Full Operations Platform

**Engineering Principle:** The operations platform is a single Python application until scale forces distribution. Premature microservices are the most common architecture mistake.

```
Job Registry → Scheduler → Queue → Worker Pool → Browser Pool → Recovery → Validation → PostgreSQL → Dashboard → Alerts
```

| Decision | Choice | Why |
|----------|--------|-----|
| Architecture | Single process | 10+ automations handled by one process |
| Storage | PostgreSQL | Dashboard queries run alongside writes |
| Recovery | Per-failure-type | Platform-level failures affect all jobs |
| Dashboard | Optional | Start with Slack alerts, add dashboard later |

**Example:** Managing 10+ automations across multiple clients.

**Common Mistake:** Splitting into microservices before the platform manages 50+ jobs. The coordination overhead exceeds the benefit.

**Production Rule:** A single process with asyncio queues handles most automation platforms. Split only when the team or workload outgrows a single deployment.

---

## PART VII — SCALING ROADMAP

### Stage 1: 1-2 Jobs (Laptop)

```
Python + nodriver + recipes/ + common/ + SQLite
```

**When to leave:** When the automation must run unattended.

### Stage 2: 3-5 Jobs (Docker)

```
Dockerfile + docker-compose + .env + profiles/ + runs/
```

**Add:** Reproducibility, scheduled execution, per-run artifacts.

### Stage 3: 5-10 Jobs (Single VPS)

```
Docker + PostgreSQL + Slack alerts + metrics
```

**Add:** Concurrent workers, health checks, central storage.

### Stage 4: 10-20 Jobs (Worker Pool)

```
Job registry + worker pool + queue + recovery manager + dashboard
```

**Add:** Job orchestration, parallel execution, recovery automation.

### Stage 5: 20+ Jobs (Multi-Server)

```
Load balancer + distributed queue + worker nodes + replicated DB + central logging
```

**Add:** Horizontal scaling, no single point of failure.

### Stage 6: 100+ Jobs (Platform)

```
API + auto-scaling + cost tracking + client portal + SLA dashboards
```

**Add:** Multi-tenancy, self-service, cost allocation, SLAs.

---

## PART VIII — ARCHITECTURE REVIEW CHECKLIST

Before writing a line of code:

- [ ] **Is automation justified?** Would a Zapier/n8n workflow work? An API call?
- [ ] **What is the failure cost?** 10 minutes? Lost client? Compliance issue?
- [ ] **Single writer or multiple?** SQLite or PostgreSQL?
- [ ] **How long does one run take?** Seconds? Hours? Does it overlap with the next?
- [ ] **What is the recovery strategy?** Retry? Restart? Re-authenticate? Escalate?
- [ ] **Is the operation idempotent?** Running twice should not create duplicates.
- [ ] **What evidence is preserved on failure?** Screenshot? HTML? Console? Network?
- [ ] **Who is alerted and how?** Slack? Email? PagerDuty?
- [ ] **How are credentials managed?** `.env`? Secrets manager? Manual?
- [ ] **How is the environment reproduced?** Docker? Virtualenv? Pinned versions?
- [ ] **What is the monitoring threshold?** Failure rate? Data volume? Runtime deviation?
- [ ] **What is the rollback plan?** Can you revert a code change without downtime?

---

## PART IX — COMMON ARCHITECTURE MISTAKES

| Mistake | Why It Hurts | Better Approach |
|---------|-------------|-----------------|
| Starting with Kubernetes | Operational complexity for 1 container | Docker Compose on a single VPS |
| PostgreSQL before SQLite | Added server management for zero benefit | SQLite until you need concurrent writers |
| No job locking | Overlapping runs corrupt data | File-based or database advisory lock |
| Shared profile across workers | Random session failures | One profile per worker |
| Microservices for a batch job | Network calls, deployment complexity | Single process with asyncio queues |
| No validation pipeline | Bad data looks like good data | Validate before storing |
| No per-run artifacts | Cannot debug yesterday's failure | Screenshot + HTML per run |
| Hardcoded environment values | Every deployment requires code changes | Environment variables + .env |
| Monitoring only exit code | Script succeeds with empty data | Monitor data volume, not completion |

---

## Key Principles

1. **Simplicity scales.** The simplest architecture that meets requirements will outlast every complex alternative.

2. **Isolation prevents cascading failures.** One profile per worker. One browser per identity. Never share state.

3. **Design for recovery.** Every automation will fail. The question is not "if" but "how well does it recover?"

4. **Measure before optimizing.** A queue, a new database, or a distributed system should be a response to a measured bottleneck, not a guess.

5. **Architecture evolves with requirements.** Start with SQLite and cron. Add PostgreSQL and schedulers when the workload demands it — never before.

> **"Isolation is cheaper than debugging."**

> **"The simplest architecture that works today will outlast the clever one you design for tomorrow."**
