# Browser Automation Pattern Catalog

> **Read This If...**
> You know what you want to automate but are not sure which architectural pattern to choose. This catalog helps you select the right pattern for your constraints.

---

## 15 Engineering Patterns for Production Browser Automation

Each pattern is 2-3 pages and follows the same structure:

```
Pattern Name
Problem → Forces → Architecture → Implementation → When to Use → When NOT to Use → Trade-offs → Production Rule
```

---> **Quick Take**
> If you're short on time:
> - [Y] Default to Polling (simplest). Switch only when measured.
> - [Y] Always bound queue sizes — unbounded queues are memory leaks.
> - [Y] Circuit breakers protect targets; retry budgets protect you.
> - [Y] Design for idempotency before adding retry logic.
> - [Y] Caps on restarts prevent supervisors from masking permanent failures.
> 
> Estimated reading: 16 minutes
> 



## PATTERN 1 — Polling

**Intent:** Periodically check a source for new data with minimal complexity.

**Context:** You need data at regular intervals (every hour, daily, weekly). Missing an update is acceptable because the next poll catches it.

**Forces:** Simplicity vs. latency. Polling is simple but wasteful when nothing changed. Event-driven is efficient but complex.


**Engineering Principle:** Polling is the most reliable pattern because it is stateless. If a poll fails, the next poll will succeed. No state to recover, no checkpoint to restore.

**Complexity:** ■□□□□□ | **Operations:** ■□□□□□ | **Scalability:** ■■■□□□

### Problem
You need to check a website for updated data at regular intervals.

### Forces
- Data changes are unpredictable
- Missing an update is acceptable (the next poll will catch it)
- Simplicity is more important than latency

### Architecture
```
Scheduler (cron)
    ↓
Worker (browser)
    ↓
Extract → Validate → Store
    ↓
Sleep until next interval
```

### Implementation
```python
async def poll(url: str, interval: int = 3600):
    while True:
        try:
            data = await extract(url)
            validated = validate(data)
            store(validated)
        except Exception as e:
            logger.error(f"Poll failed: {e}")
        await asyncio.sleep(interval)
```

### When to Use
- Periodic price monitoring
- Daily report extraction
- Scheduled data collection

### When NOT to Use
- Real-time data requirements (use Event Observer)
- One-time extraction (use a direct script, not a pattern)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Simple, stateless | Wasted cycles when nothing changed |
| Easy to monitor | Higher resource usage than event-driven |
| Survives failures | Higher latency |


**Related Reading**
- Architecture Guide: Decision 11 — Polling vs Event-Driven
- Failure Playbook: Pattern 5 — Page Loads Forever
- Design Review: Pre-Flight — Is Automation Justified?


### Production Rule
> Polling is the default pattern. Use it until you measure a reason to switch.

---

## PATTERN 2 — Queue

**Intent:** Decouple work production from consumption so both sides operate at their natural speed.

**Context:** Work arrives faster than it can be processed. You need parallel workers, crash resilience, or variable processing times.

**Forces:** Throughput vs. ordering. Queues maximize throughput but do not guarantee order unless specifically configured.


**Engineering Principle:** A queue decouples work production from consumption. Use it when producers and consumers operate at different speeds or must be independently scalable.

**Complexity:** ■■■□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■■■□

### Problem
Work arrives faster than it can be processed. Multiple workers need to process independent units of work without coordination.

### Forces
- Variable work arrival rate
- Need for parallel processing
- Crash resilience (work must survive worker failure)

### Architecture
```
Producer(s)
    ↓
Queue (bounded, e.g. asyncio.Queue or Redis)
    ↓
Worker 1    Worker 2    Worker 3
    ↓           ↓           ↓
Results      Results      Results
```

### Implementation
```python
import asyncio

queue = asyncio.Queue(maxsize=100)

async def producer():
    for item in range(100):
        await queue.put(item)

async def worker():
    while True:
        item = await queue.get()
        await process(item)
        queue.task_done()
```

### When to Use
- Multiple suppliers to check
- Variable page load times
- Need to survive worker crashes

### When NOT to Use
- Single worker, single target (use direct execution)
- All work must complete in strict order (use a list, not a queue)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Parallel processing | Queue management overhead |
| Crash resilience | Items may be processed twice |
| Backpressure | Queue full = dropped work |


**Related Reading**
- Architecture Guide: Decision 12 — Queue vs Direct Execution
- Failure Playbook: Pattern 12 — Job Overlap
- War Stories: Story 11 — The Migration That Forgot the Profiles


### Production Rule
> A queue without backpressure is a memory leak. Always set `maxsize`.

---

## PATTERN 3 — Worker Pool

**Intent:** Limit concurrent execution to prevent resource exhaustion.

**Context:** You have N units of work but server resources (RAM, CPU, API quota) can only handle M at a time (M < N).

**Forces:** Resource budget vs. throughput. More workers = faster completion but higher risk of OOM or rate limiting.


**Engineering Principle:** A worker pool limits concurrency. It prevents resource exhaustion while maximizing throughput.

**Complexity:** ■■□□□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■■□□

### Problem
You have N units of work but can only process M concurrently (M < N). Exceeding M causes resource exhaustion (OOM, rate limiting).

### Forces
- Fixed resource budget (RAM, CPU, API quota)
- Work items are independent
- Need bounded concurrency

### Architecture
```
Jobs (list)
    ↓
Semaphore (max_workers=N)
    ↓
Worker 1    Worker 2    Worker 3
```

### Implementation
```python
import asyncio

MAX_WORKERS = 3
sem = asyncio.Semaphore(MAX_WORKERS)

async def process_all(jobs):
    async def bounded(job):
        async with sem:
            return await process(job)
    return await asyncio.gather(*[bounded(j) for j in jobs])
```

### When to Use
- 25 suppliers but only 3GB RAM
- API rate limits (10 requests/sec)
- Fixed-size VPS

### When NOT to Use
- Work items have dependencies (use Pipeline)
- Unlimited resources available (but this is rare)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Bounded resource usage | Workers idle when queue is empty |
| Simple implementation | No work prioritization |


**Related Reading**
- Architecture Guide: Decision 1 — Single vs Multiple Browsers, Decision 7 — Profiles per Worker
- Failure Playbook: Pattern 2 — Profile Locked
- War Stories: Story 14 — The Profile That Belonged to Two Clients


### Production Rule
> Set `MAX_WORKERS` to the number of concurrent browsers your server can sustain. For a 4GB VPS, this is usually 3.

---

## PATTERN 4 — Producer-Consumer

**Intent:** Separate fast producers from slow consumers with a buffer between them.

**Context:** One part of the pipeline produces data faster than the downstream can consume it. The producer blocks on the consumer.

**Forces:** Speed mismatch vs. complexity. A buffer decouples stages but adds memory pressure.


**Engineering Principle:** Separating production from consumption allows each side to operate at its natural speed without blocking the other.

**Complexity:** ■■■□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■■□□

### Problem
One part of the pipeline produces data faster than the downstream can consume it. The fast producer blocks on the slow consumer.

### Forces
- Different processing speeds upstream vs downstream
- Need for buffering between stages
- Both stages must operate independently

### Architecture
```
Producer (fast)
    ↓
Buffer (queue)
    ↓
Consumer (slow)
```

### Implementation
```python
async def produce(queue):
    while True:
        data = await fetch_page()
        await queue.put(data)

async def consume(queue):
    while True:
        data = await queue.get()
        await validate_and_store(data)  # Slow
        queue.task_done()
```

### When to Use
- Fast API responses, slow database writes
- CDP events arriving faster than handlers can process
- Page extraction faster than validation

### When NOT to Use
- Both sides operate at the same speed (no buffer needed)
- Processing is sequential (just call the next function)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Decoupled stages | Buffer memory |
| Independent scaling | Coordination complexity |


**Related Reading**
- Architecture Guide: Architecture B — Multi-Supplier Pipeline
- Failure Playbook: Pattern 11 — 0 Records Extracted
- Design Review: Red Flags — Stop and Fix Before Proceeding


### Production Rule
> Always bound the buffer. An unbounded producer-consumer is a memory leak.

---

## PATTERN 5 — Circuit Breaker

**Intent:** Stop retrying a failing target and let it recover.

**Context:** A target website or API is returning errors. Retrying makes recovery slower by adding load to already-struggling infrastructure.

**Forces:** Protection vs. availability. A circuit breaker protects the target but delays recovery detection.


**Engineering Principle:** When a system is failing, retrying makes it worse. A circuit breaker stops retries and lets the system recover.

**Complexity:** ■■■■□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■■□□

### Problem
A target website is returning 5xx errors. The automation retries, which increases the load on the failing server, which makes recovery slower.

### Forces
- Need to detect when a target is genuinely down
- Retries during downtime waste resources
- Must test for recovery without overloading

### Architecture
```
CLOSED (normal operation)
    ↓ failures > threshold
OPEN (block all requests)
    ↓ timeout expires
HALF-OPEN (test request)
    ↓ success → CLOSED
    ↓ failure → OPEN (reset timeout)
```

### Implementation
```python
class CircuitBreaker:
    def __init__(self, threshold=5, cooldown=60):
        self.failures = 0
        self.threshold = threshold
        self.cooldown = cooldown
        self.state = "CLOSED"
        self.last_failure = 0

    async def call(self, fn, *args):
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.cooldown:
                self.state = "HALF-OPEN"
            else:
                raise CircuitOpenError()
        try:
            result = await fn(*args)
            self.failures = 0
            self.state = "CLOSED"
            return result
        except Exception:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.threshold:
                self.state = "OPEN"
            raise
```

### When to Use
- Target websites with known reliability issues
- Third-party APIs with rate limits
- Any remote system you do not control

### When NOT to Use
- Local resources (files, database) — use retry with backoff
- One-time extraction — circuit breaker adds complexity for no benefit

### Trade-offs
| Benefit | Cost |
|---------|------|
| Protects downstream systems | Delays recovery detection |
| Reduces resource waste | More complex than simple retry |


**Related Reading**
- Architecture Guide: Decision 6 — Retry vs Recover vs Restart
- Failure Playbook: Pattern 3 — Session Expired Mid-Run
- War Stories: Story 4 — The Retry Loop That DDoSed a Supplier


### Production Rule
> A circuit breaker protects the target. A retry budget protects your own system. Use both.

---

## PATTERN 6 — Retry with Backoff

**Intent:** Resolve transient failures while minimizing load on the target.

**Context:** Network timeouts, DNS errors, and rate limit responses often succeed on retry — but only if the retry is delayed appropriately.

**Forces:** Recovery speed vs. target load. Aggressive retry recovers faster but risks overwhelming the target.


**Engineering Principle:** A retry is only useful if the failure is transient. All retries must be bounded, backoff must be exponential, and jitter prevents thundering herd.

**Complexity:** ■■□□□□ | **Operations:** ■□□□□□ | **Scalability:** ■■■□□□

### Problem
Transient failures (network timeouts, DNS errors) succeed on retry. But retrying too fast or too many times causes more harm than the original failure.

### Forces
- Most transient failures resolve within seconds
- Retrying too fast overwhelms the target
- Retrying too many times delays alerting

### Architecture
```
Request
    ↓ failure
Wait 2s → Retry
    ↓ failure
Wait 4s → Retry
    ↓ failure
Wait 8s → Retry
    ↓ failure
Alert human
```

### Implementation
```python
import asyncio
import random

async def retry_with_backoff(fn, max_attempts=3, base_delay=2):
    for attempt in range(max_attempts):
        try:
            return await fn()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
```

### When to Use
- Network timeouts
- DNS resolution errors
- Rate limit responses (with longer backoff)

### When NOT to Use
- 4xx client errors (the request is wrong)
- Selector failures (the page changed)
- Authentication failures (wrong credentials)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Resolves most transient failures | Delays alert for permanent failures |
| Prevents thundering herd (with jitter) | More complex than fixed retry |


**Related Reading**
- Architecture Guide: Decision 6 — Retry vs Recover vs Restart
- Failure Playbook: Pattern 1 — Chrome Won't Start
- War Stories: Story 4 — The Retry Loop That DDoSed a Supplier


### Production Rule
> Never retry a permanent failure. Classify failure types before applying retry logic.

---

## PATTERN 7 — Checkpoint/Resume

**Intent:** Avoid restarting from the beginning when an automation crashes mid-run.

**Context:** An automation processes thousands of items over hours. A crash at 90% completion wastes 90% of the runtime.

**Forces:** I/O overhead vs. wasted work. Checkpoints add writes per item but save time on restart.


**Engineering Principle:** An automation that runs for hours should not restart from the beginning when it fails. Checkpoints allow mid-run recovery.

**Complexity:** ■■■□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■■□□

### Problem
An automation processes 10,000 products over 2 hours. At 90% completion, Chrome crashes. Without checkpoints, the automation restarts from product 1.

### Forces
- Long-running extractions
- Non-deterministic processing order
- Need to minimize data loss on crash

### Architecture
```
For each item in items:
    process(item)
    save_checkpoint(item_id)

On restart:
    load_checkpoint() → resume_from
    process(items[resume_from:])
```

### Implementation
```python
import json

def save_checkpoint(item_id: str, file="checkpoint.json"):
    json.dump({"last": item_id}, open(file, "w"))

def load_checkpoint(file="checkpoint.json") -> str:
    try:
        return json.load(open(file))["last"]
    except FileNotFoundError:
        return None
```

### When to Use
- Processing 1,000+ items per run
- Each item takes 5+ seconds
- Runs cost time or money

### When NOT to Use
- Runs complete in under 5 minutes
- Items are in random order (checkpoint may skip)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Saves time on restart | Extra I/O per item |
| Reduces data loss | Checkpoint may be stale |


**Related Reading**
- Architecture Guide: Decision 7 — Profiles per Worker vs Shared
- Failure Playbook: Pattern 15 — Profile Corruption
- Design Review: Red Flags — Shared Profiles


### Production Rule
> Checkpoint after every item that would be expensive to re-process. Do not checkpoint after every single operation — batch writes every 10-50 items.

---

## PATTERN 8 — Idempotent Consumer

**Intent:** Make retries safe by ensuring running an operation twice produces the same result as running it once.

**Context:** Retries, manual re-runs, and cron misfires can cause the same work to be processed multiple times.

**Forces:** Safety vs. memory. Idempotency requires tracking what has been seen, which consumes memory or storage.


**Engineering Principle:** An operation is idempotent if running it twice produces the same result as running it once. Idempotency is the foundation of reliable retry.

**Complexity:** ■■□□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■■□□

### Problem
A retry, manual re-run, or cron misfire causes the same work to be processed twice. Without idempotency, the result is duplicate records, double charges, or inconsistent state.

### Forces
- Automations are retried by nature
- Network failures mask whether an operation completed
- Downstream systems cannot always deduplicate

### Architecture
```
Operation
    ↓
Check natural key (e.g., company + email)
    ↓
Exists? → Skip (already processed)
Doesn't exist? → Process → Store → Complete
```

### Implementation
```python
class IdempotentProcessor:
    def __init__(self):
        self.seen = set()

    async def process(self, item: dict) -> str:
        key = f"{item.get('company')}|{item.get('email')}"
        if key in self.seen:
            return "duplicate"
        self.seen.add(key)
        await self._store(item)
        return "accepted"
```

### When to Use
- Form submission workflows
- Lead processing
- Any operation that creates external records

### When NOT to Use
- Read-only extractions
- Destructive operations (deletes — still want idempotent, but cannot use skip)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Safe to retry | Memory for seen keys |
| Simple to implement | Redis or DB needed for multi-worker |


**Related Reading**
- Architecture Guide: Decision 8 — Browser Profiles vs Stateless Sessions
- Failure Playbook: Pattern 3 — Session Expired Mid-Run
- War Stories: Story 1 — The Login That Failed Only on Mondays


### Production Rule
> Design every write operation to be idempotent before adding retry logic.

---

## PATTERN 9 — Fan-out/Fan-in

**Intent:** Extract from multiple sources simultaneously, then combine results.

**Context:** You need data from N independent sources and must aggregate all results before producing output.

**Forces:** Parallelism vs. coordination. Fan-out is fast but requires all branches to complete before fan-in.


**Engineering Principle:** Independent work should be parallelized. Dependent results should be aggregated. Fan-out/fan-in is the natural pattern for multi-source extraction.

**Complexity:** ■■■□□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■■■□

### Problem
You need to extract data from 10 sources simultaneously, then combine the results into a single report.

### Forces
- Sources are independent
- All results are needed for the final output
- Sources have different latencies

### Architecture
```
Fan-out:
    Task 1 ──→ Source A
    Task 2 ──→ Source B
    Task 3 ──→ Source C

Fan-in:
    Result A
    Result B  → Combine → Report
    Result C
```

### Implementation
```python
import asyncio

async def extract_all(sources: list) -> dict:
    results = await asyncio.gather(
        *[extract(s) for s in sources],
        return_exceptions=True
    )
    combined = {}
    for source, result in zip(sources, results):
        if isinstance(result, Exception):
            logger.error(f"{source} failed: {result}")
        else:
            combined[source] = result
    return combined
```

### When to Use
- Multi-supplier extraction
- Price comparison across marketplaces
- Any "collect from N sources, merge" workflow

### When NOT to Use
- Sources have dependencies (one result is input to another)
- Sequential processing is required (rate limits per IP)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Maximum parallelism | All workers must finish before fan-in |
| Fastest total time | Failure in one affects all (use return_exceptions) |


**Related Reading**
- Architecture Guide: Architecture B — Multi-Supplier Pipeline
- Failure Playbook: Pattern 12 — Job Overlap
- War Stories: Story 12 — The Endless Loop That Cost $5,000


### Production Rule
> Always use `return_exceptions=True` with `gather`. A failure in one source should not crash the entire fan-out.


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


---

## PATTERN 10 — Supervisor

**Intent:** Keep a worker running by detecting crashes and restarting automatically.

**Context:** Workers crash for reasons outside your control — OOM, segfault, network partition. A human cannot restart them instantly.

**Forces:** Automation vs. masking. Supervisors keep things running but can hide recurring failures.


**Engineering Principle:** A supervisor monitors worker health and restarts failed workers. It is the simplest reliable way to keep an automation running.

**Complexity:** ■■□□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■□□□

### Problem
A worker crashes. Without a supervisor, the automation stops until a human restarts it.

### Forces
- Workers crash for reasons outside your control
- Restart should be automatic for recoverable failures
- Excessive restarts indicate a deeper problem

### Architecture
```
Supervisor
    ├── spawn → Worker
    │              ↓ crash
    └── detect → restart (max N times)
                  ↓ exceeded
              alert human
```

### Implementation
```python
class Supervisor:
    MAX_RESTARTS = 3

    async def run(self):
        restarts = 0
        while restarts < self.MAX_RESTARTS:
            try:
                await self.worker()
            except Exception as e:
                logger.warning(f"Worker crashed: {e}, restarting")
                restarts += 1
        logger.error(f"Worker crashed {self.MAX_RESTARTS} times — escalating")
```

### When to Use
- 24/7 automation services
- Unattended long-running workers
- Any worker that must survive without human intervention

### When NOT to Use
- Batch jobs that run once per day (cron handles restart)
- Experimental scripts (let them fail visibly)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Keeps automation running | Masks recurring failures |
| Simple implementation | No state preservation across restarts |


**Related Reading**
- Architecture Guide: Decision 6 — Retry vs Recover vs Restart
- Failure Playbook: Pattern 6 — CDP Connection Lost
- War Stories: Story 3 — The Chrome Update That Corrupted Profiles


### Production Rule
> Always cap restart attempts. A worker that crashes 10 times in 5 minutes has a permanent problem — restarting hides it.

---

## PATTERN 11 — Saga (Workflow)

**Intent:** Manage multi-step workflows with compensating actions for each step on failure.

**Context:** An automation has multiple steps with side effects. If a middle step fails, preceding steps must be rolled back.

**Forces:** Consistency vs. complexity. Sagas provide clean rollback but require compensating logic for every step.


**Engineering Principle:** A saga is a sequence of steps with compensating actions for each step. If a step fails, the saga rolls back the preceding steps.

**Complexity:** ■■■■□□ | **Operations:** ■■■■□□ | **Scalability:** ■■■■■□

### Problem
An automation has multiple steps (login → navigate → extract → store → notify). If storage fails, the extraction should be retried, not lost. If login fails, the entire saga must roll back.

### Forces
- Steps have dependencies
- Failure recovery is different for each step
- Some steps are reversible, some are not

### Architecture
```
Step 1: Login (compensate: none — can't "un-login")
Step 2: Navigate (compensate: none — stateless)
Step 3: Extract (compensate: discard extracted data)
Step 4: Store (compensate: delete stored records)
Step 5: Notify (compensate: none — sent already)
```

### Implementation
```python
async def run_saga():
    compensations = []
    try:
        data = await extract()
        compensations.append(lambda: discard(data))
        await store(data)
        compensations.append(lambda: delete(data))
        await notify()
    except Exception:
        for compensate in reversed(compensations):
            await compensate()
        raise
```

### When to Use
- Multi-step workflows with side effects
- Operations where partial execution is unacceptable
- Financial or compliance-critical automations

### When NOT to Use
- Read-only extractions (no side effects to roll back)
- Single-step operations (use retry instead)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Clean failure recovery | Complex to implement |
| No partial state | Compensating actions may also fail |


**Related Reading**
- Architecture Guide: Decision 6 — Retry vs Recover vs Restart
- Failure Playbook: Pattern 11 — 0 Records Extracted
- War Stories: Story 6 — The Account Lockout From 5 Login Retries


### Production Rule
> Not all steps have meaningful compensating actions. If a step cannot be rolled back, log it prominently — operators need to know what was committed before the failure.

---

## PATTERN 12 — Event Observer (CDP)

**Intent:** Observe browser events in real time without polling.

**Context:** You need to know when network requests complete, console errors occur, or page state changes — without busy-waiting.

**Forces:** Real-time visibility vs. handler speed. Events arrive faster than handlers can process them without buffering.


**Engineering Principle:** The browser emits events for everything it does. Observing these events gives you insight without adding load.

**Complexity:** ■■■■□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■■□□

### Problem
You need to know when a page has finished loading, when a network request completes, or when a console error occurs — without polling.

### Forces
- Events arrive in real time
- Multiple event types need different handlers
- Handlers must be fast (events arrive faster than handlers can process)

### Architecture
```
Chrome → CDP Event → WebSocket → nodriver → Handler
    ↓                                              ↓
Event queue                                    Background
(bounded)                                     worker
```

### Implementation
```python
from common.cdp import subscribe_to_events

async def monitor_network(page):
    events = []
    async def handler(event):
        events.append(event)
        if len(events) > 1000:
            events.pop(0)  # bounded queue
    await subscribe_to_events(page, handler)
    return events
```

### When to Use
- Monitoring page load performance
- Detecting API calls without DOM interaction
- Catching console errors in real time

### When NOT to Use
- Periodic data extraction (polling is simpler)
- One-time page snapshots

### Trade-offs
| Benefit | Cost |
|---------|------|
| Real-time visibility | Handler must be non-blocking |
| No polling overhead | Queue required for backpressure |


**Related Reading**
- Architecture Guide: Decision 9 — Browser Automation vs API, Architecture B
- Failure Playbook: Pattern 8 — Rate Limited
- War Stories: Story 8 — The CAPTCHA That Wasn't


### Production Rule
> Never do heavy work in an event handler. Queue the event, process it in a background worker.

---

## PATTERN 13 — Pipeline

**Intent:** Process data through discrete, independently testable stages.

**Context:** Data must go through multiple transformations (extract, validate, normalize, store) with independent failure modes at each stage.

**Forces:** Modularity vs. overhead. Pipelines make stages testable but copy data between them.


**Engineering Principle:** A pipeline processes data through discrete stages. Each stage is independently testable, replaceable, and monitorable.

**Complexity:** ■■□□□□ | **Operations:** ■■□□□□ | **Scalability:** ■■■■□□

### Problem
Data must go through multiple transformations before it is ready for storage. Each transformation has its own failure modes.

### Forces
- Multiple processing stages
- Each stage can fail independently
- Stages may run at different speeds

### Architecture
```
Extract → Validate → Normalize → Enrich → Store → Export
```

### Implementation
```python
class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, fn):
        self.stages.append(fn)

    async def run(self, data):
        for stage in self.stages:
            data = await stage(data)
            if data is None:
                raise PipelineError(f"Stage {stage.__name__} failed")
        return data
```

### When to Use
- Data processing chains (extract → validate → store)
- ETL workflows
- Any multi-stage transformation

### When NOT to Use
- Single-step operations (the pipeline adds complexity)
- Operations where stages are tightly coupled

### Trade-offs
| Benefit | Cost |
|---------|------|
| Testable stages | Data copying between stages |
| Replaceable components | Pipeline overhead |


**Related Reading**
- Architecture Guide: Decision 2 — Tabs vs Processes
- Failure Playbook: Pattern 11 — 0 Records Extracted, Pattern 6 — CDP Connection Lost


### Production Rule
> Log the record count at the input and output of every pipeline stage. A stage where records disappear is a bug.

---

## PATTERN 14 — Dead Letter Queue

**Intent:** Preserve permanently failed items for analysis instead of discarding them.

**Context:** An item in a queue fails permanently. Discarding it loses diagnostic evidence. Keeping it requires storage.

**Forces:** Data preservation vs. storage cost. DLQs preserve evidence but must be reviewed periodically.


**Engineering Principle:** Failed items should not be discarded. They should be moved to a dead letter queue for analysis and reprocessing.

**Complexity:** ■■□□□□ | **Operations:** ■■■□□□ | **Scalability:** ■■■□□□

### Problem
An item in a queue fails processing. It cannot be retried (permanent failure). But discarding it loses evidence of why it failed.

### Forces
- Some failures are permanent
- Failed items contain diagnostic information
- Operators need to review failures periodically

### Architecture
```
Queue → Worker
    ↓ success → Acknowledge
    ↓ failure (permanent) → Dead Letter Queue
                             ↓
                         Review weekly
```

### Implementation
```python
async def process_with_dlq(queue, dlq):
    item = await queue.get()
    try:
        await process(item)
    except PermanentError:
        await dlq.put(item)  # Dead letter
        logger.warning(f"Moved to DLQ: {item}")
```

### When to Use
- Queue-based extraction systems
- Any pattern where items can permanently fail
- Systems where data loss is unacceptable

### When NOT to Use
- Synchronous processing (just log the error)
- Systems where reprocessing is never needed

### Trade-offs
| Benefit | Cost |
|---------|------|
| No data loss | Storage for dead letters |
| Audit trail | DLQ must be monitored |


**Related Reading**
- Architecture Guide: Architecture C — Client Reporting Platform
- Failure Playbook: Pattern 10 — Quarantine Growth
- Design Review: Post-Implementation Review


### Production Rule
> A dead letter queue that is never reviewed is just a storage sink. Schedule weekly DLQ review.

---

## PATTERN 15 — Checkpoint with Saga

**Intent:** Combine mid-run recovery with clean rollback for maximum reliability.

**Context:** An automation has both long-running extraction (needs checkpoint) and multi-step workflows (needs saga compensation).

**Forces:** Reliability vs. complexity. This is the most advanced pattern — use only when simpler patterns are insufficient.


**Engineering Principle:** Combining checkpoint and saga patterns gives you mid-run recovery AND clean rollback on failure.

**Complexity:** ■■■■■□ | **Operations:** ■■■■■□ | **Scalability:** ■■■■■□

### Problem
An automation has both long-running extraction (needs checkpoint) and multi-step workflows (needs saga). Neither pattern alone is sufficient.

### Forces
- Long processing time (need checkpoint)
- Side effects (need saga compensation)
- Recovery must be automatic

### Architecture
```
For each item in items:
    save_checkpoint(item.id)
    try:
        step1(item)  # Side effect
        step2(item)  # Side effect
    except:
        rollback_to_checkpoint(item.id)
        raise
```

### When to Use
- High-value extractions (financial data, compliance)
- Long-running workflows with side effects
- Systems where partial failure is unacceptable

### When NOT to Use
- Read-only extractions (no side effects)
- Short-running jobs (checkpoint overhead exceeds benefit)

### Trade-offs
| Benefit | Cost |
|---------|------|
| Full recovery capability | Most complex pattern |
| No data loss | Rollback logic must be tested |


**Related Reading**
- Architecture Guide: Architecture D — Full Operations Platform
- Failure Playbook: Recovery Decision Tree
- War Stories: Story 20 — The 18-Month Silent Failure


### Production Rule
> This is the most advanced pattern in the catalog. Use it only when simpler patterns (Retry, Checkpoint, or Saga alone) are insufficient for your reliability requirements.

---



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


## Key Principles

1. **Default to the simplest pattern.** Polling is always the right starting point. Switch only when you measure a reason to.

2. **Bound everything.** Queues need maxsize. Retries need max_attempts. Workers need a semaphore. Unbounded resources are the most common pattern failure.

3. **Idempotency enables reliability.** If running an operation twice produces the same result as running it once, you can retry safely.

4. **Patterns compose.** Worker Pool + Queue + Supervisor is more powerful than any single pattern. Choose patterns that work together.

5. **Isolation before coordination.** One profile per worker, one browser per target. Shared state is the enemy of reliability.

> **"A pattern is not a recipe. It is a response to recurring forces."**

> **"Bound everything. Unbounded resources are the most common pattern failure."**
