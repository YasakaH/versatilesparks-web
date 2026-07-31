# Automation Design Review Checklist

> **Read This If...**
> You are about to write a new automation or reviewing an existing one. This checklist helps you catch design issues before they become production incidents.

---

## Pre-Flight: Should You Automate This At All?

Before writing a single line of code, confirm that automation is the right solution.

- [ ] **Is there an API?** If the website has a public API, use it instead of a browser. Browser automation is the most expensive way to get data.
- [ ] **Is a no-code tool sufficient?** n8n, Zapier, or Make can handle simple form filling and API integrations in minutes. Only build custom automation when these tools cannot meet your requirements.
- [ ] **Is the website legally authorizing this access?** Check robots.txt, terms of service, and rate limits. Automating against terms of service creates legal and reputational risk.
- [ ] **What is the cost of failure?** A personal price tracker failure costs 10 minutes. A client deliverable failure costs revenue. A compliance failure costs legal liability. Engineer to match the cost.
- [ ] **How long will this automation be needed?** A one-week task does not need Docker, monitoring, or recovery logic. A three-year engagement does.

### Decision

| Answer | Action |
|--------|--------|
| API exists | Use the API. Return to this checklist only if the API is insufficient. |
| n8n/Zapier works | Use the tool. Return to this checklist when the workflow exceeds the tool's capabilities. |
| Automation is justified | Continue to the full review. |

---> **Quick Take**
> If you're short on time:
> - [Y] Check for an API before writing any browser automation.
> - [Y] One profile per worker is non-negotiable.
> - [Y] No monitoring = no production readiness.
> - [Y] Validate before storing, not after.
> - [Y] Every failure needs a recovery strategy.
> 
> Estimated reading: 6 minutes
> 



## Full Review

### Requirements

- [ ] **Business problem documented.** What is the specific outcome this automation produces? "Monitor competitor prices" is a feature. "Alert when a competitor's price drops below our margin threshold" is a business problem.
- [ ] **Non-functional requirements listed.** How often does it run? How fast must it complete? What is the acceptable failure rate? How much data per run?
- [ ] **Failure cost estimated.** What is the cost of one missed run? One hour of downtime? One corrupted dataset?
- [ ] **Exit criteria defined.** When is this automation complete and ready to hand off to operations?

### Architecture

- [ ] **Pattern selected from catalog.** Which pattern (Polling, Queue, Worker Pool, etc.) fits this use case? Document the choice and why alternatives were rejected.
- [ ] **Single worker or pool?** A single worker with a single browser is the simplest correct architecture. Add workers only when concurrency is required.
- [ ] **Storage chosen for scale.** SQLite for single-writer. PostgreSQL for concurrent writers. Document why the other was not chosen.
- [ ] **Profile isolation confirmed.** One profile per worker. Never shared.
- [ ] **Stateless or persistent session documented.** Cookie-only or full browser profile? Why?
- [ ] **Idempotency designed.** Running twice produces the same result as running once. Natural key or UUID? Where is the dedup check?

### Execution

- [ ] **Schedule defined.** How often? What if the previous run is still executing? Lock mechanism chosen.
- [ ] **Timeout configured.** How long before a run is considered failed? Is the timeout per-page, per-job, or total?
- [ ] **Resource limits set.** RAM, CPU, disk, concurrent browsers. Document the limits and how they were calculated.
- [ ] **Async boundaries understood.** Which parts of the automation are I/O-bound (network, disk) and which are CPU-bound (parsing, validation)?
- [ ] **Rate limiting implemented.** Client-side delay between requests. Backoff strategy for 429 responses.

### Failure Modes

- [ ] **Chrome crash recovery.** Detect CDP disconnect. Restart browser. Resume from checkpoint.
- [ ] **Session expiry recovery.** Validate session before extraction. Re-authenticate if expired.
- [ ] **Selector failure detected.** Capture HTML dump and screenshot. Alert operator. Do not retry.
- [ ] **Empty data handled.** Distinguish between "page has no data" and "selector could not find data."
- [ ] **Validation failure handled.** Quarantine threshold. Alert on >10% failure rate.
- [ ] **Storage failure handled.** Database connection lost? Disk full? Backup storage?
- [ ] **Job overlap handled.** Lock mechanism prevents concurrent execution.

### Observability

- [ ] **Evidence collected on failure.** Screenshot, HTML dump, console output, CDP network log. Stored with run ID.
- [ ] **Record count logged at every stage.** Extracted N, validated M, stored K. If N > 0 and K = 0, alert.
- [ ] **Runtime tracked.** Expected duration, actual duration, deviation alert.
- [ ] **Success rate monitored.** Per-run, per-day, per-week. Degradation alert when rate drops.
- [ ] **Alert destination configured.** Slack webhook, email, PagerDuty. Test that alerts are delivered.
- [ ] **Operator runbook exists.** What does the operator do when the alert fires? Link to the relevant Failure Playbook pattern.

### Security

- [ ] **Credentials stored outside code.** `.env` file or secrets manager. Never in source code.
- [ ] **Least privilege applied.** Does the automation have access to only the minimum resources it needs?
- [ ] **Credential rotation planned.** How frequently do credentials expire? Who is notified? What is the update process?
- [ ] **No secrets in Dockerfile.** `ENV` commands bake secrets into the image. Use `env_file` or runtime environment variables.
- [ ] **`.env` never committed.** Added to `.gitignore`. Document required variables in `.env.example`.

### Operations

- [ ] **Owner assigned.** A specific person or team is responsible for this automation's operation, monitoring, and maintenance.
- [ ] **Deployment documented.** How is a new version deployed? Rollback procedure?
- [ ] **Dependencies version-pinned.** Python packages, nodriver, Chrome. Pin versions to prevent unexpected upgrades.
- [ ] **Docker image tagged.** Use version tags, not `latest`. `v1.2.3` not `latest`.
- [ ] **Backup strategy defined.** How often is the database backed up? Retention policy?
- [ ] **Maintenance window scheduled.** When can the automation be down for upgrades without impacting users?

### Scalability

- [ ] **Scaling path documented.** What is the next stage when this automation outgrows its current architecture? (Docker → VPS → Worker Pool → Platform)
- [ ] **Bottleneck identified.** What will break first as load increases? Database? Chrome processes? IP reputation?
- [ ] **Cost per run estimated.** RAM, CPU, bandwidth, storage per execution. Does the budget support 10x growth?

---

## Review Outcomes

| Result | Meaning | Action |
|--------|---------|--------|
| [Y] Pass | All critical checks pass | Proceed to implementation |
| [!] Pass with conditions | Minor issues found | Document issues, proceed with plan to fix |
| [X] Fail | Critical issues found | Do not proceed. Fix issues before writing code. |
| [Cycle] Reroute | Automation not the right solution | Use API or no-code tool instead |

---

## Production Readiness Score

After the review, assign a score:

| Score | Meaning |
|-------|---------|
| 0-3 | Prototype. Works on your machine. No retries, no monitoring, no recovery. |
| 4-6 | Internal tool. Reliable for personal use. Basic retry and logging. |
| 7-9 | Production ready. Docker, monitoring, recovery, validation, alerts. |
| 10 | Enterprise grade. Idempotent, audited, cost-tracked, SLA-monitored, multi-worker. |

---

## Red Flags — Stop and Fix Before Proceeding

If any of these are true, do not ship the automation. The issues must be resolved before any code is written:

| Red Flag | Why It's Fatal |
|----------|---------------|
| Shared profiles across workers | Guarantees eventual profile corruption. One profile per worker — non-negotiable. |
| Hardcoded credentials in source code | Credentials are permanently compromised if committed to git. |
| Infinite retry loop (`while True`) | Masks permanent failures, delays alerting, consumes resources. |
| No logging | Cannot diagnose failures. Every failure requires reproducing. |
| No timeout configured | A stuck page hangs the automation indefinitely. |
| No validation before storage | Bad data enters the database silently. |
| No monitoring or alerting | Automation fails for days without anyone knowing. |
| No recovery strategy | Every crash requires manual restart. 3 AM pages for transient failures. |
| Credentials in Dockerfile | Anyone with image access can extract secrets. Use `.env` or runtime env vars. |

## Estimated Build Size

| Scope | Team Size | Calendar Time | Engineering Hours |
|-------|-----------|--------------|-------------------|
| Prototype (single script) | 1 dev | 1 day | 4-6 hours |
| Production automation | 1 dev | 3-5 days | 15-25 hours |
| Client deliverable | 1-2 devs | 1-2 weeks | 40-80 hours |
| Platform (10+ jobs) | 2-3 devs | 4-6 weeks | 200-400 hours |
| Fleet (100+ jobs) | 3-5 devs | 3-6 months | 2000-4000 hours |

These estimates assume experienced developers familiar with the common/ library. Add 30-50% for teams new to the toolkit.

---



## Questions Every Reviewer Asks

Before signing off on any automation design, an experienced reviewer checks these:

| Question | Why It Matters |
|----------|---------------|
| **What breaks first?** | Every system has a weakest link. Identify it before it fails. |
| **How do you recover?** | Not "if" it fails, but "how" the recovery works. Walk through the scenario. |
| **How do you know it's broken?** | Monitoring is not "is the script running?" — it is "is the data correct?" |
| **Can this run twice safely?** | Idempotency. If the cron fires twice, does the database survive? |
| **What's the rollback?** | Code rollback, data rollback, and credential rollback — all separate concerns. |
| **What's the blast radius?** | One worker crashes vs all workers crash — different responses. |
| **How do credentials get rotated?** | Not "we have a password" — but "what happens when it expires?" |
| **What does success look like?** | Not "the script ran" — but "the business outcome was achieved." |
| **Who owns this at 3 AM?** | If the on-call person does not know the automation exists, it is unsupported. |
| **When do we replace this?** | Every architecture has a shelf life. Plan for it now. |


## Post-Implementation Review

After the first week of production operation:

- [ ] Success rate meets target (99%+ for production systems)
- [ ] No unexpected failure patterns emerged
- [ ] Alert thresholds are correct (not too noisy, not too quiet)
- [ ] Runtime is within expected bounds
- [ ] Data volume is as expected
- [ ] Recovery paths have been exercised at least once
- [ ] Operator runbook has been tested
- [ ] Stakeholders have verified the output

---

## Key Principles

1. **Automation is the last resort.** Always check for an API, a no-code tool, or a manual workflow before building custom automation.

2. **Validate before storing.** If bad data reaches the database, it will be treated as correct until someone proves otherwise.

3. **Monitoring without alerting is not monitoring.** A dashboard that nobody watches during off-hours is a false sense of security.

4. **Every feature has a maintenance cost.** Production features (queue, dashboard, recovery) should be added intentionally, not by default.

5. **A postmortem without follow-up is a diary entry.** Every incident should produce at least one action item that prevents recurrence.

> **"A postmortem without follow-up is a diary entry."**
