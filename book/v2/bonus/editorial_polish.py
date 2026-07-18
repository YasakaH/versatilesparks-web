# Editorial Polish — Batch 3
# Vary openings, Intent/Context, Recovery Verification, Quotes, Next Read

import os, re

BONUS = "."

# ============================================================
# 1. Vary openings — add selection guides
# ============================================================

# Pattern Catalog: Add "Pattern Selection Guide" after Quick Take
path = os.path.join(BONUS, "automation-pattern-catalog.md")
content = open(path, encoding="utf-8").read()

selection_guide = """

## Pattern Selection Guide

| You need to... | Choose this pattern |
|---------------|-------------------|
| Check a website periodically | Polling |
| Process work in parallel | Queue → Worker Pool |
| Combine results from multiple sources | Fan-out/Fan-in |
| Protect a failing target | Circuit Breaker |
| Retry safely after transient errors | Retry with Backoff |
| Resume extraction after a crash | Checkpoint/Resume |
| Ensure retries don't create duplicates | Idempotent Consumer |
| Keep a worker running 24/7 | Supervisor |
| Roll back a multi-step workflow | Saga / Checkpoint with Saga |
| Monitor browser events in real time | Event Observer |
| Transform data through stages | Pipeline |
| Preserve failed items for review | Dead Letter Queue |

"""

if "Pattern Selection Guide" not in content:
    qt_marker = "\n---\n\n## PATTERN 1"
    idx = content.find(qt_marker)
    if idx != -1:
        # Find the Quick Take block end (blank line before Pattern 1)
        content = content[:idx] + selection_guide + content[idx:]
        open(path, "w", encoding="utf-8").write(content)
        print("Pattern Selection Guide added to Catalog")

# ============================================================
# 2. Intent + Context + Forces for every Pattern Catalog pattern
# ============================================================

catalog_intents = {
    "PATTERN 1 — Polling": {
        "intent": "Periodically check a source for new data with minimal complexity.",
        "context": "You need data at regular intervals (every hour, daily, weekly). Missing an update is acceptable because the next poll catches it.",
        "forces": "Simplicity vs. latency. Polling is simple but wasteful when nothing changed. Event-driven is efficient but complex."
    },
    "PATTERN 2 — Queue": {
        "intent": "Decouple work production from consumption so both sides operate at their natural speed.",
        "context": "Work arrives faster than it can be processed. You need parallel workers, crash resilience, or variable processing times.",
        "forces": "Throughput vs. ordering. Queues maximize throughput but do not guarantee order unless specifically configured."
    },
    "PATTERN 3 — Worker Pool": {
        "intent": "Limit concurrent execution to prevent resource exhaustion.",
        "context": "You have N units of work but server resources (RAM, CPU, API quota) can only handle M at a time (M < N).",
        "forces": "Resource budget vs. throughput. More workers = faster completion but higher risk of OOM or rate limiting."
    },
    "PATTERN 4 — Producer-Consumer": {
        "intent": "Separate fast producers from slow consumers with a buffer between them.",
        "context": "One part of the pipeline produces data faster than the downstream can consume it. The producer blocks on the consumer.",
        "forces": "Speed mismatch vs. complexity. A buffer decouples stages but adds memory pressure."
    },
    "PATTERN 5 — Circuit Breaker": {
        "intent": "Stop retrying a failing target and let it recover.",
        "context": "A target website or API is returning errors. Retrying makes recovery slower by adding load to already-struggling infrastructure.",
        "forces": "Protection vs. availability. A circuit breaker protects the target but delays recovery detection."
    },
    "PATTERN 6 — Retry with Backoff": {
        "intent": "Resolve transient failures while minimizing load on the target.",
        "context": "Network timeouts, DNS errors, and rate limit responses often succeed on retry — but only if the retry is delayed appropriately.",
        "forces": "Recovery speed vs. target load. Aggressive retry recovers faster but risks overwhelming the target."
    },
    "PATTERN 7 — Checkpoint/Resume": {
        "intent": "Avoid restarting from the beginning when an automation crashes mid-run.",
        "context": "An automation processes thousands of items over hours. A crash at 90% completion wastes 90% of the runtime.",
        "forces": "I/O overhead vs. wasted work. Checkpoints add writes per item but save time on restart."
    },
    "PATTERN 8 — Idempotent Consumer": {
        "intent": "Make retries safe by ensuring running an operation twice produces the same result as running it once.",
        "context": "Retries, manual re-runs, and cron misfires can cause the same work to be processed multiple times.",
        "forces": "Safety vs. memory. Idempotency requires tracking what has been seen, which consumes memory or storage."
    },
    "PATTERN 9 — Fan-out/Fan-in": {
        "intent": "Extract from multiple sources simultaneously, then combine results.",
        "context": "You need data from N independent sources and must aggregate all results before producing output.",
        "forces": "Parallelism vs. coordination. Fan-out is fast but requires all branches to complete before fan-in."
    },
    "PATTERN 10 — Supervisor": {
        "intent": "Keep a worker running by detecting crashes and restarting automatically.",
        "context": "Workers crash for reasons outside your control — OOM, segfault, network partition. A human cannot restart them instantly.",
        "forces": "Automation vs. masking. Supervisors keep things running but can hide recurring failures."
    },
    "PATTERN 11 — Saga (Workflow)": {
        "intent": "Manage multi-step workflows with compensating actions for each step on failure.",
        "context": "An automation has multiple steps with side effects. If a middle step fails, preceding steps must be rolled back.",
        "forces": "Consistency vs. complexity. Sagas provide clean rollback but require compensating logic for every step."
    },
    "PATTERN 12 — Event Observer (CDP)": {
        "intent": "Observe browser events in real time without polling.",
        "context": "You need to know when network requests complete, console errors occur, or page state changes — without busy-waiting.",
        "forces": "Real-time visibility vs. handler speed. Events arrive faster than handlers can process them without buffering."
    },
    "PATTERN 13 — Pipeline": {
        "intent": "Process data through discrete, independently testable stages.",
        "context": "Data must go through multiple transformations (extract, validate, normalize, store) with independent failure modes at each stage.",
        "forces": "Modularity vs. overhead. Pipelines make stages testable but copy data between them."
    },
    "PATTERN 14 — Dead Letter Queue": {
        "intent": "Preserve permanently failed items for analysis instead of discarding them.",
        "context": "An item in a queue fails permanently. Discarding it loses diagnostic evidence. Keeping it requires storage.",
        "forces": "Data preservation vs. storage cost. DLQs preserve evidence but must be reviewed periodically."
    },
    "PATTERN 15 — Checkpoint with Saga": {
        "intent": "Combine mid-run recovery with clean rollback for maximum reliability.",
        "context": "An automation has both long-running extraction (needs checkpoint) and multi-step workflows (needs saga compensation).",
        "forces": "Reliability vs. complexity. This is the most advanced pattern — use only when simpler patterns are insufficient."
    },
}

path = os.path.join(BONUS, "automation-pattern-catalog.md")
content = open(path, encoding="utf-8").read()

for pattern_key, data in catalog_intents.items():
    pattern_header = f"## {pattern_key}"
    if pattern_header in content:
        idx = content.find(pattern_header)
        # Find the next section after the header
        hdr_end = content.find("\n", idx) + 1
        # Check if Intent already exists
        next_part = content[hdr_end:hdr_end+500]
        if "### Intent" not in next_part:
            intro_block = f"""
**Intent:** {data['intent']}

**Context:** {data['context']}

**Forces:** {data['forces']}

"""
            content = content[:hdr_end] + intro_block + content[hdr_end:]
            print(f"Intent/Context added to {pattern_key}")

open(path, "w", encoding="utf-8").write(content)

# ============================================================
# 3. Recovery Verification for every Playbook pattern
# ============================================================

playbook_verify = {
    "PATTERN 1": """
### Recovery Verification

- [ ] Browser launches successfully: `google-chrome --version`
- [ ] Page loads without errors: screenshot confirms content
- [ ] Session is valid: extraction returns > 0 records
- [ ] Alert clears automatically

""",
    "PATTERN 2": """
### Recovery Verification

- [ ] Lockfile removed: `ls profile_dir/SingletonLock` returns empty
- [ ] Worker launches without "profile locked" error
- [ ] Previous run's data is intact

""",
    "PATTERN 3": """
### Recovery Verification

- [ ] Page shows authenticated content (not a login form)
- [ ] Data extraction returns expected record count
- [ ] Session age recorded for next run

""",
    "PATTERN 4": """
### Recovery Verification

- [ ] Updated selector returns elements: `page.find(sel)` is not null
- [ ] HTML dump confirms the target element is present
- [ ] Extraction produces expected record count

""",
    "PATTERN 5": """
### Recovery Verification

- [ ] Page loads within timeout window
- [ ] Resource blocking list verified against current page
- [ ] Navigation duration logged and < threshold

""",
    "PATTERN 6": """
### Recovery Verification

- [ ] CDP connection test: `browser.get("about:blank")` succeeds
- [ ] Chrome process is alive: `ps aux | grep chrome`
- [ ] Previous extraction state (checkpoint) is recoverable

""",
    "PATTERN 7": """
### Recovery Verification

- [ ] Quarantine file shows records in expected format (not login page HTML)
- [ ] First quarantined record matches expected schema
- [ ] Validation rules updated to match new format

""",
    "PATTERN 8": """
### Recovery Verification

- [ ] Request rate measured: stays below site's rate limit
- [ ] 429 responses no longer appear in a 5-minute window
- [ ] Blocked IP falls back to proxy rotation

""",
    "PATTERN 9": """
### Recovery Verification

- [ ] Container restarts without OOM
- [ ] Memory usage stays below 80% of container limit
- [ ] Browser launches and runs a full extraction cycle

""",
    "PATTERN 10": """
### Recovery Verification

- [ ] Quarantine retention policy applied: oldest records rotated
- [ ] Disk usage below 70% threshold
- [ ] Quarantine review scheduled for next week

""",
    "PATTERN 11": """
### Recovery Verification

- [ ] Pipeline tracing confirms records at every stage
- [ ] Extract > 0, Validate > 0, Store > 0
- [ ] Screenshot confirms page is not an error state

""",
    "PATTERN 12": """
### Recovery Verification

- [ ] Lock mechanism in place: `filelock` or database advisory lock
- [ ] Duplicate records identified and removed
- [ ] Concurrency test: running two jobs simultaneously fails gracefully

""",
    "PATTERN 13": """
### Recovery Verification

- [ ] Page renders content with headless mode disabled
- [ ] Console errors captured and reviewed
- [ ] CDP network log confirms API data received

""",
    "PATTERN 14": """
### Recovery Verification

- [ ] New credentials stored in `.env` or secrets manager
- [ ] Login test: runs a dry login and confirms success
- [ ] Alert threshold updated: expiry warning set for 7 days before rotation

""",
    "PATTERN 15": """
### Recovery Verification

- [ ] Profile deleted and recreated successfully
- [ ] Re-authentication works: login form submitted correctly
- [ ] Previous session state confirmed lost (expected — profile is disposable)

""",
}

path = os.path.join(BONUS, "failure-playbook.md")
content = open(path, encoding="utf-8").read()

for pattern_name, verify_block in playbook_verify.items():
    marker = f"## {pattern_name}"
    if marker in content:
        idx = content.find(marker)
        # Find the "### Prevention" section (which is the last section before Related Reading)
        prev_marker = "### Prevention"
        prev_idx = content.find(prev_marker, idx)
        if prev_idx != -1:
            # Find the end of Prevention section (next section or blank line)
            eod = content.find("\n\n**", prev_idx)
            if eod == -1:
                eod = content.find("\n\n#", prev_idx + 20)
            if eod != -1:
                content = content[:eod] + verify_block + "\n" + content[eod:]
                print(f"Recovery Verification added to {pattern_name}")

open(path, "w", encoding="utf-8").write(content)

# ============================================================
# 4. Architecture Lifecycle for Field Guide
# ============================================================

lifecycle_section = """

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
"""

path = os.path.join(BONUS, "architecture-field-guide.md")
content = open(path, encoding="utf-8").read()

if "## Architecture Lifecycle" not in content:
    # Insert after Part V (Architecture Review Checklist)
    marker = "## PART VI — REFERENCE ARCHITECTURES"
    idx = content.find(marker)
    if idx != -1:
        # Insert before the marker
        content = content[:idx] + lifecycle_section + "\n\n" + content[idx:]
        open(path, "w", encoding="utf-8").write(content)
        print("Architecture Lifecycle added to Field Guide")

# ============================================================
# 5. Questions Every Reviewer Asks for Design Review
# ============================================================

reviewer_questions = """

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

"""

path = os.path.join(BONUS, "automation-design-review.md")
content = open(path, encoding="utf-8").read()

if "Questions Every Reviewer Asks" not in content:
    # Insert after Production Readiness Score
    marker = "## Post-Implementation Review"
    idx = content.find(marker)
    if idx != -1:
        content = content[:idx] + reviewer_questions + "\n" + content[idx:]
        open(path, "w", encoding="utf-8").write(content)
        print("Reviewer Questions added to Design Review")

# ============================================================
# 6. Engineering Quotes — scatter through all docs
# ============================================================

quotes = {
    "architecture-field-guide.md": [
        "\n> **\"Isolation is cheaper than debugging.\"**\n",
        "\n> **\"The simplest architecture that works today will outlast the clever one you design for tomorrow.\"**\n",
    ],
    "failure-playbook.md": [
        "\n> **\"Every retry is a request to a struggling system.\"**\n",
        "\n> **\"Automation isn't successful because it ran. It's successful because the outcome is correct.\"**\n",
    ],
    "automation-pattern-catalog.md": [
        "\n> **\"A pattern is not a recipe. It is a response to recurring forces.\"**\n",
        "\n> **\"Bound everything. Unbounded resources are the most common pattern failure.\"**\n",
    ],
    "automation-design-review.md": [
        "\n> **\"A postmortem without follow-up is a diary entry.\"**\n",
    ],
    "war-stories.md": [
        "\n> **\"The most dangerous automation is the one that has never failed.\"**\n",
        "\n> **\"If you don't measure the outcome, you don't know if the automation is working.\"**\n",
    ],
}

for fname, doc_quotes in quotes.items():
    path = os.path.join(BONUS, fname)
    content = open(path, encoding="utf-8").read()
    for q in doc_quotes:
        # Find a natural insertion point (after a --- section divider, not near other quotes)
        content = content + q
        print(f"Quote added to {fname}")
    open(path, "w", encoding="utf-8").write(content)

# ============================================================
# 7. Add Prevention cross-refs to War Stories endings
# ============================================================

war_prevention = {
    1: "- **Could this have been prevented?** YES → [Decision 8 — Profiles vs Sessions](architecture-field-guide.md) and [Pattern 3 — Session Validation](failure-playbook.md)",
    2: "- **Could this have been prevented?** YES → [Pattern 4 — Selector Fallback Chains](automation-pattern-catalog.md)",
    3: "- **Could this have been prevented?** YES → [Decision 7 — Profile per Worker](architecture-field-guide.md) and [Failure Pattern 15](failure-playbook.md)",
    4: "- **Could this have been prevented?** YES → [Pattern 6 — Retry with Backoff](automation-pattern-catalog.md) and [Circuit Breaker](automation-pattern-catalog.md)",
    5: "- **Could this have been prevented?** YES → [Decision 13 — Evidence Types](architecture-field-guide.md) and statistical monitoring",
    6: "- **Could this have been prevented?** YES → [Decision 6 — Failure Classification](architecture-field-guide.md) and [Failure Pattern 14](failure-playbook.md)",
    7: "- **Could this have been prevented?** YES → [Cost Table](architecture-field-guide.md) and storage monitoring in [Design Review](automation-design-review.md)",
    8: "- **Could this have been prevented?** YES → [Decision 9 — Browser vs API](architecture-field-guide.md) and [Pattern 12 — Event Observer](automation-pattern-catalog.md)",
    9: "- **Could this have been prevented?** YES → Timezone test in [Design Review](automation-design-review.md) — test at both DST boundaries",
    10: "- **Could this have been prevented?** YES → [Design Review — Alert Deduplication](automation-design-review.md) and [Failure Pattern 8](failure-playbook.md)",
    11: "- **Could this have been prevented?** YES → [Decision 7 — Profiles](architecture-field-guide.md) — include profiles in deployment checklist",
    12: "- **Could this have been prevented?** YES → [Pattern 7 — Checkpoint/Resume](automation-pattern-catalog.md) with deduplication check",
    13: "- **Could this have been prevented?** YES → [Pattern 12 — Event Observer](automation-pattern-catalog.md) — wait for a condition, not a duration",
    14: "- **Could this have been prevented?** YES → [Decision 7 — Profile per Worker](architecture-field-guide.md) and startup assertions",
    15: "- **Could this have been prevented?** YES → [Design Review — Monitoring](automation-design-review.md) — monitor the monitoring system",
    16: "- **Could this have been prevented?** YES → Production-data tests in [Design Review](automation-design-review.md) — test with real data shape",
    17: "- **Could this have been prevented?** YES → Auth method detection in [Failure Pattern 3](failure-playbook.md)",
    18: "- **Could this have been prevented?** YES → Log rotation in [Design Review](automation-design-review.md) — monitor log directory size",
    19: "- **Could this have been prevented?** YES → [Pattern 7 — Checkpoint/Resume](automation-pattern-catalog.md) — use completion signals, not time gaps",
    20: "- **Could this have been prevented?** YES → Statistical monitoring in [Design Review](automation-design-review.md) — compare to 7-day rolling average",
}

path = os.path.join(BONUS, "war-stories.md")
content = open(path, encoding="utf-8").read()

for story_num, prevention_text in war_prevention.items():
    if story_num < 10:
        marker = f"## STORY {story_num}"
    else:
        marker = f"## STORY {story_num}"
    if marker in content:
        idx = content.find(marker)
        # Find the Lesson section
        lesson_end = content.find("\n---\n", idx)
        if lesson_end == -1:
            lesson_end = content.find("\n## STORY", idx + 10)
        if lesson_end != -1:
            insert = "\n" + prevention_text + "\n"
            content = content[:lesson_end] + insert + content[lesson_end:]
            print(f"Prevention link added to Story {story_num}")

open(path, "w", encoding="utf-8").write(content)

print("\nALL EDITORIAL POLISH COMPLETE")
