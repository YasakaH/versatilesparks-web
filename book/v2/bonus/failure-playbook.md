# Browser Automation Failure Playbook

> **Read This If...**
> An automation is failing in production or you are designing recovery strategies. This playbook helps you diagnose by symptom, choose the right fix, and prevent recurrence.

---

## Symptom-to-Diagnosis Reference for Production Incidents

---> **Quick Take**
> If you're short on time:
> - ✓ Never retry login failures — they are permanent.
> - ✓ Capture screenshot + HTML before restarting Chrome.
> - ✓ Validate session before every extraction.
> - ✓ One profile per worker — always.
> - ✓ Alert on 0 records, not just exit code 1.
> 
> Estimated reading: 14 minutes
> 



### How to Use This Playbook

1. **Find the symptom** that matches what you are seeing
2. **Check the severity** to prioritize
3. **Follow the diagnosis flow** — each step tells you what to check next
4. **Apply the fix**
5. **Run the postmortem** to prevent recurrence

---

### Failure Taxonomy

Every failure pattern is tagged by category. This helps narrow down the root cause quickly:

| Category | Examples | Tag |
|----------|----------|-----|
| **Infrastructure** | Docker, memory, disk, permissions | `[INFRA]` |
| **Browser** | Chrome crash, launch failure, CDP disconnect | `[BROWSER]` |
| **Authentication** | Session expired, login failed, MFA required | `[AUTH]` |
| **Navigation** | Page timeout, blank page, redirect loop | `[NAV]` |
| **Extraction** | Selector missing, empty data, wrong format | `[EXTRACT]` |
| **Validation** | All records rejected, schema mismatch | `[VALIDATE]` |
| **Storage** | Database locked, disk full, write failure | `[STORAGE]` |
| **Operations** | Job overlap, cron misfire, credential rotation | `[OPS]` |

---

## PATTERN 1 — Chrome Won't Start `[INFRA]` `[BROWSER]`

**Engineering Principle:** Fail fast. If Chrome does not start, do not retry indefinitely — collect evidence and escalate.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Critical — automation dead. No data collected until Chrome starts. Manual intervention required.


| P0 — Automation dead | 5 min | 15 min | One worker |

### Symptom

```
Error: "Unable to connect to browser"
Error: "Connection refused"
Container exits immediately with code 1
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Chrome not installed in container | High for new Docker deployments |
| 2 | Missing shared memory (`/dev/shm` too small) | High for Docker |
| 3 | Sandbox error when running as root | Medium for Docker |
| 4 | Chrome version mismatch with nodriver | Medium on rebuild |
| 5 | Port 9222 in use from orphaned Chrome | Low |

### Evidence to Collect

- [ ] Docker logs: `docker logs <container> 2>&1 | tail -50`
- [ ] Process list: `ps aux | grep chrome | wc -l`
- [ ] Shared memory: `df -h /dev/shm`
- [ ] Chrome version: `google-chrome --version`

### Diagnosis Flow

```text
Chrome won't start
    ↓
Is Chrome installed?
  NO  → Install Chrome in Dockerfile
  YES → Is /dev/shm large enough?
    NO  → Set shm_size: 2gb
    YES → Running as root?
      YES → Add --no-sandbox
      NO  → Port in use?
        YES → pkill chrome
        NO  → Check Chrome vs nodriver version
```

### Fix

```yaml
# docker-compose.yml
services:
  automation:
    shm_size: 2gb
```

```python
# launch arguments
browser = await launch_browser(
    arguments=["--no-sandbox", "--disable-dev-shm-usage"]
)
```

**Confidence:** ***** (Restart browser) | ***☆☆ (Delete profile)

### Prevention

- Add a pre-flight health check that tests browser launch
- Pin Chrome version in Dockerfile (never `latest`)
- Run `google-chrome --version` and fail fast if missing

### False Positive

```
No Chrome in PATH
    ↓
But you installed it via Snap instead of APT.
    ↓
Chrome IS installed — just not where nodriver looks.
Fix: Set CHROME_PATH environment variable.
```

---

### Recovery Verification

- [ ] Browser launches successfully: `google-chrome --version`
- [ ] Page loads without errors: screenshot confirms content
- [ ] Session is valid: extraction returns > 0 records
- [ ] Alert clears automatically




**Related Reading**
- Architecture Guide: [Decision 5 — Docker vs Bare Metal](#)
- Pattern Catalog: [Supervisor](#), [Retry with Backoff](#)
- War Stories: [Story 3 — Chrome Update Corrupted Profiles](#)



## PATTERN 2 — Profile Locked `[BROWSER]` `[OPS]`

**Engineering Principle:** One profile per worker is not a suggestion — it is a constraint. Violating it guarantees eventual corruption.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Medium — one worker blocked. Other workers unaffected. Job delayed, not lost.


| P1 — Job blocked | 2 min | 5 min | One worker |

### Symptom

```
Error: "Profile locked"
Two concurrent automations fail with the same error
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Two workers sharing the same profile directory | High |
| 2 | Previous run crashed without releasing lockfile | Medium |
| 3 | File permissions (Docker user mismatch) | Low |

### Diagnosis

```bash
ls -la profiles/worker-1/SingletonLock
# If lockfile exists and no Chrome process is running, it is stale
```

### Fix

```bash
rm profiles/worker-1/SingletonLock
```

**Prevention:** One directory per worker:
```python
PROFILE_DIR = Path(f"./profiles/worker-{worker_id}")
```

Post-run cleanup: remove lockfile in `finally` block.

**Confidence:** ***** (Delete lockfile) | ****☆ (Recreate profile)

### False Positive

```
Profile locked error
    ↓
Lockfile exists but Chrome is running.
The profile is legitimately in use — do not delete the lockfile.
Fix: Wait for the other worker to finish, or kill the stale Chrome.
```

---


**Related Reading**
- Architecture Guide: [Decision 7 — Profile per Worker](#)
- Pattern Catalog: [Worker Pool](#)
- Design Review: [Red Flags — Shared Profiles](#)



## PATTERN 3 — Session Expired Mid-Run `[AUTH]`

**Engineering Principle:** Sessions expire. Design for it. Session validation before every extraction eliminates an entire class of silent failures.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** High — data lost for this run. Next run recovers, but a gap exists in the dataset.


| P1 — Data lost for this run | 5 min | 5 min | One job |

### Symptom

```
Mid-run, automation starts returning login pages.
401 errors from API calls.
Elements that were present are now missing.
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Session has a fixed expiry (e.g., 24 hours) | High |
| 2 | Idle timeout — automation paused too long | Medium |
| 3 | Token rotated by the server during session | Low |
| 4 | Multiple logins from different workers | Medium |

### Diagnosis Flow

```text
Session expired mid-run
    ↓
Is the page showing a login form?
  YES → Session expired. Re-authenticate.
  NO  → Is the dashboard visible but data empty?
    YES → Token expired. Session cookie is still valid. Refresh token.
    NO  → Idle timeout? Reduce time between interactions.
```

### Fix

```python
async def run_with_recovery(browser, url):
    page = await browser.get(url)
    if "login" in await page.evaluate("location.pathname"):
        await login(browser, url)
    # Continue extraction
```

**Confidence:** ***** (Re-authenticate) | **☆☆☆ (Create new profile)

### Prevention

- Validate session at the START of every extraction, not when failure occurs
- Keep sessions alive with periodic pings during long runs
- Monitor session age and proactively re-authenticate before expiry

---

### Recovery Verification

- [ ] Lockfile removed: `ls profile_dir/SingletonLock` returns empty
- [ ] Worker launches without "profile locked" error
- [ ] Previous run's data is intact



### Recovery Verification

- [ ] Page shows authenticated content (not a login form)
- [ ] Data extraction returns expected record count
- [ ] Session age recorded for next run




**Related Reading**
- Architecture Guide: [Decision 8 — Browser Profiles vs Stateless Sessions](#)
- Pattern Catalog: [Idempotent Consumer](#), [Checkpoint/Resume](#)
- War Stories: [Story 1 — Login That Failed Only on Mondays](#)



## PATTERN 4 — Selector Returns No Elements `[EXTRACT]`

**Engineering Principle:** A missing selector is never a retry problem. It is always a diagnosis problem. The data is either absent, moved, or in a different context.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** High — no data collected for the affected selector. Manual fix required (update selector).


| P1 — No data | 10 min | 30 min | One selector |

### Symptom

```
page.find(".price") → None
QuerySelector returns null
Extraction produces zero records
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Page not fully loaded (SPA data still arriving) | High |
| 2 | CSS class renamed in frontend deployment | High |
| 3 | Element in iframe or Shadow DOM | Medium |
| 4 | Page returned error or empty state | Medium |

### Evidence

- [ ] HTML dump: `page.evaluate("document.documentElement.outerHTML")`
- [ ] Screenshot
- [ ] CDP network log — did the data API call return data?
- [ ] Console errors — JavaScript exceptions?

### Diagnosis Flow

```text
Selector returns no elements
    ↓
Capture HTML dump
    ↓
Is the element in the HTML?
  YES → Update selector
  NO  → Is it in an iframe?
    YES → Switch context
    NO  → In Shadow DOM?
      YES → Access shadowRoot
      NO  → Page showing error state?
        YES → Check CDP network log
```

### Fix

```python
selectors = ["[data-product-id]", ".price", "[aria-label='Price']"]
for sel in selectors:
    el = await page.find(sel)
    if el:
        break
```

**Confidence:** ***** (Update selector) | ***☆☆ (Add fallback chain)

### False Positive

```
Selector returns 0 elements
    ↓
The website legitimately has 0 products in this category.
This is not a failure — the data is accurate.
Fix: Distinguish between "page has no data" and "selector couldn't find data."
```

---


**Related Reading**
- Pattern Catalog: [Retry with Backoff](#)
- Design Review: [Pre-Flight — Is Automation Justified?](#)
- War Stories: [Story 2 — Selector Broken by A/B Testing](#)



## PATTERN 5 — Page Loads Forever (Timeout) `[NAV]`

**Engineering Principle:** A page that never finishes loading is usually waiting for a resource that does not exist. Block unnecessary resources before navigating.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Medium — one page delayed. Automation may still complete if timeout is reasonable.


| P1 — Job stuck | 5 min | 10 min | One page |

### Symptom

```
browser.get(url) never completes.
Navigation timeout after 30 seconds.
Page shows "loading" spinner indefinitely.
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | One slow resource (analytics, font, ad) blocks load event | High |
| 2 | Server-sent events or WebSocket that never closes | Medium |
| 3 | CDN or origin server is slow | Low |

### Fix

**Block slow resources:**
```python
BLOCK_PATTERNS = [".com/metrics", "google-analytics", "fonts.googleapis"]
```

**Set reasonable timeout:**
```python
page = await browser.get(url, timeout=15)
```

**Confidence:** ***** (Block resources) | ***☆☆ (Increase timeout)

### Prevention

- Block analytics, fonts, and social widgets before navigation
- Set navigation timeout to 15-30 seconds (not default 300)
- Monitor page load performance — regressions signal website changes

---

### Recovery Verification

- [ ] Updated selector returns elements: `page.find(sel)` is not null
- [ ] HTML dump confirms the target element is present
- [ ] Extraction produces expected record count



### Recovery Verification

- [ ] Page loads within timeout window
- [ ] Resource blocking list verified against current page
- [ ] Navigation duration logged and < threshold




**Related Reading**
- Architecture Guide: [Decision 11 — Polling vs Event-Driven](#)
- Pattern Catalog: [Event Observer](#)
- War Stories: [Story 13 — The 1-Second Wait That Missed the Data](#)



## PATTERN 6 — CDP Connection Lost `[BROWSER]`

**Engineering Principle:** The WebSocket connection between nodriver and Chrome is the single point of failure. Monitor it before every major interaction, not just at startup.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Critical — entire browser session lost. Currently extracting data is discarded.


| P0 — Automation dead | 2 min | 5 min | One browser |

### Symptom

```
WebSocket connection closed unexpectedly
ConnectionClosedError
Cannot send CDP message — no active session
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Chrome process crashed (OOM, segfault) | High |
| 2 | Chrome was closed by another process | Medium |
| 3 | Idle timeout — Chrome background throttling | Low |

### Fix

**Reconnect with backoff:**
```python
for attempt in range(3):
    try:
        browser = await launch_browser()
        return await extract(browser, url)
    except ConnectionClosedError:
        await asyncio.sleep(2 ** attempt)
raise
```

**Confidence:** ***** (Restart Chrome) | ****☆ (Restart from checkpoint)

### Prevention

- Monitor CDP health before each major extraction step
- Implement browser health telemetry
- Limit continuous runtime — restart browser every 100 pages

---

### Recovery Verification

- [ ] CDP connection test: `browser.get("about:blank")` succeeds
- [ ] Chrome process is alive: `ps aux | grep chrome`
- [ ] Previous extraction state (checkpoint) is recoverable




**Related Reading**
- Pattern Catalog: [Supervisor](#), [Circuit Breaker](#)
- Architecture Guide: [Decision 6 — Retry vs Recover vs Restart](#)
- War Stories: [Story 3 — Chrome Update Corrupted Profiles](#)



## PATTERN 7 — All Records Fail Validation `[VALIDATE]`

**Engineering Principle:** 100% validation failure is never a data quality issue — it is a structural issue. The extraction is broken, not the data.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Critical — no data stored. Zero records in database. Structural issue, not transient.


| P0 — No data stored | 10 min | 30 min | One job |

### Symptom

```
100% of records quarantined.
Alert: "Validation failure rate: 100%."
Database received zero records.
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Website redesigned (data format changed) | High |
| 2 | Validation schema too strict for current data | Medium |
| 3 | Selector returning wrong content | Medium |
| 4 | Page returning error page instead of data | Low |

### Diagnosis

Check the first quarantined record:
```bash
head -1 quarantine.json | python -m json.tool
```

Compare with expected schema:
```python
# Expected: {"sku": "...", "price": 123.45}
# Received: {"product_id": "...", "price": "₹123.45"}
```

**Confidence:** ***** (Update schema) | ***☆☆ (Relax validation rule)

### False Positive

```
100% validation failure
    ↓
The website legitimately changed their data format.
Validation rules are correct — the extraction needs updating.
Fix: Update selectors, then the validation schema will pass again.
```

---


**Related Reading**
- Architecture Guide: [Decision 13 — Screenshot vs HTML vs Structured Data](#)
- Pattern Catalog: [Pipeline](#), [Dead Letter Queue](#)
- War Stories: [Story 5 — Dashboard Reported Success While Storing Zero Rows](#)



## PATTERN 8 — Rate Limited or IP Blocked `[INFRA]`

**Engineering Principle:** Rate limiting is a signal, not an error. Respect the signal before it becomes a block.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Medium — extraction delayed until cooldown expires. No permanent data loss.


| P2 — Delayed | 5 min | 15 min | One IP |

### Symptom

```
HTTP 429 (Too Many Requests)
HTTP 403 (Forbidden)
CAPTCHA page appears
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Automation faster than site's rate limit | High |
| 2 | Multiple workers sharing the same IP | Medium |
| 3 | Site deployed new anti-bot protection | Medium |

### Fix

```python
await asyncio.sleep(2.0)  # Max 30 requests/minute

# On 429:
wait = int(response.headers.get("Retry-After", 60))
await asyncio.sleep(wait)
```

**Confidence:** ***** (Add rate limiting) | ***☆☆ (Rotate IP)

### Prevention

- Implement client-side rate limiting before the first request
- Distribute requests across IPs if possible
- Monitor 429 rates — a sudden increase means the site changed limits

---

### Recovery Verification

- [ ] Quarantine file shows records in expected format (not login page HTML)
- [ ] First quarantined record matches expected schema
- [ ] Validation rules updated to match new format



### Recovery Verification

- [ ] Request rate measured: stays below site's rate limit
- [ ] 429 responses no longer appear in a 5-minute window
- [ ] Blocked IP falls back to proxy rotation




**Related Reading**
- Architecture Guide: [Decision 9 — Browser vs API](#)
- Pattern Catalog: [Retry with Backoff](#), [Circuit Breaker](#)
- War Stories: [Story 4 — Retry Loop DDoSed a Supplier](#)



## PATTERN 9 — Docker Container OOM `[INFRA]`

**Engineering Principle:** Chrome is the most memory-intensive component. If the container runs out of memory, the browser is always the first to be killed.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Critical — container dead. Automation stops until container restarts.


| P0 — Container dead | 5 min | 10 min | One worker |

### Symptom

```
Container exits with code 137 (SIGKILL)
dmesg shows "oom-killer" messages
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Container memory limit too low (< 2GB) | High |
| 2 | Memory leak from not closing tabs | Medium |
| 3 | Profile grows too large (cache, IndexedDB) | Low |

### Fix

```yaml
services:
  automation:
    deploy:
      resources:
        limits:
          memory: 4g
```

**Confidence:** ***** (Increase memory limit) | ***☆☆ (Periodic Chrome restart)

### Prevention

- Set `memory: 4g` as Docker default for browser automation
- Close unused tabs — each tab adds ~100MB
- Use `--disable-extensions` to reduce Chrome's footprint

---

### Recovery Verification

- [ ] Container restarts without OOM
- [ ] Memory usage stays below 80% of container limit
- [ ] Browser launches and runs a full extraction cycle




**Related Reading**
- Architecture Guide: [Part III — Cost Table](#)
- Pattern Catalog: [Worker Pool](#)
- War Stories: [Story 7 — Database Grew 50GB in One Weekend](#)



## PATTERN 10 — Quarantine File Grows Unbounded `[OPS]`

**Engineering Principle:** A quarantine file that grows indefinitely is a symptom of an unexamined process. Review quarantined records weekly.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Low — storage warning only. Does not affect extraction. Risk of disk full if ignored.


| P3 — Disk warning | 5 min | 30 min | Storage volume |

### Fix

```python
MAX_QUARANTINE_AGE_DAYS = 30
# Rotate: quarantine.2026-07-01.json
```

**Confidence:** ***** (Add retention policy) | **☆☆☆ (Manual cleanup)

### Prevention

- 30-day retention policy on quarantine records
- Weekly review of quarantine patterns
- Alert when quarantine file exceeds 100MB

---

### Recovery Verification

- [ ] Quarantine retention policy applied: oldest records rotated
- [ ] Disk usage below 70% threshold
- [ ] Quarantine review scheduled for next week




**Related Reading**
- Pattern Catalog: [Dead Letter Queue](#)
- Design Review: [Post-Implementation Review — Weekly checks](#)
- War Stories: [Story 7 — Database Grew 50GB in One Weekend](#)



## PATTERN 11 — 0 Records Extracted `[EXTRACT]` `[VALIDATE]`

**Engineering Principle:** Zero is never a normal extraction result. If extraction returns 0 records, something is wrong — even if the exit code is 0.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** High — data gap. No records stored despite successful script execution. May be silent.


| P1 — Data gap | 10 min | 30 min | One job |

### Symptom

```
Scheduler fired. Worker started. Exit code: 0.
No data in database. Logs: "Extracted 0 records."
```

### Diagnosis Flow

```text
0 records extracted
    ↓
Check extraction log
    ↓
Did selectors match anything?
  NO  → Pattern 4 (Selector empty)
  YES → Did validation pass?
    NO  → Pattern 7 (All fail validation)
    YES → Did storage succeed?
      NO  → Database connection issue
```

### Fix

```python
logger.info(f"Extracted: {len(raw)}")
logger.info(f"Validated: {len(valid)}")
logger.info(f"Stored: {len(stored)}")
```

**Confidence:** ***** (Add pipeline tracing) | **☆☆☆ (Restart job)

### False Positive

```
0 records extracted
    ↓
The supplier genuinely has no products in stock today.
Do not alert — this is an accurate extraction.
Fix: Check for a human-visible "no results" message on the page.
```

---


**Related Reading**
- Architecture Guide: [Decision 13 — Evidence Types](#)
- Pattern Catalog: [Checkpoint/Resume](#), [Pipeline](#)
- War Stories: [Story 5 — Dashboard Reporting Success While Storing Zero Rows](#)



## PATTERN 12 — Job Overlap and Data Corruption `[OPS]`

**Engineering Principle:** Concurrency without coordination is corruption. Every scheduled job must have a mechanism to prevent overlapping executions.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Medium — data quality issue. Duplicate records require cleanup. No permanent data loss.


| P1 — Data quality | 15 min | 15 min | One job |

### Symptom

```
Duplicate records in the database.
Random "record already exists" errors.
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | No job lock — cron fires before previous run finishes | High |
| 2 | Scheduler misfire — wrong interval configured | Medium |
| 3 | Manual run overlaps with scheduled run | Medium |

### Fix

```python
from filelock import FileLock
with FileLock("job.lock", timeout=0):
    run_automation()
```

**Confidence:** ***** (Add filelock) | ****☆ (Database advisory lock)

### False Positive

```
Job overlap detected
    ↓
The overlap was intentional — two jobs process different data.
Fix: Use separate lock files per job type.
```

---


**Related Reading**
- Architecture Guide: [Decision 4 — Cron vs Scheduler](#)
- Pattern Catalog: [Queue](#), [Idempotent Consumer](#)
- War Stories: [Story 19 — The Race Condition at Midnight](#)



## PATTERN 13 — Browser Starts but Page Is Blank `[NAV]` `[BROWSER]`

**Engineering Principle:** A blank page is either a network issue, a rendering issue, or a compatibility issue. Headless Chrome is not identical to headed Chrome — test both.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** High — no data from this page navigation. May be site-specific or environment-specific.


| P1 — No data | 10 min | 20 min | One page |

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Site blocks headless Chrome | Medium |
| 2 | CSP or CORS blocking resources | Low |
| 3 | Browser version too old for the website | Low |

### Diagnosis

Run with `headless=False` — does it work headed?
- Yes → The site detects headless mode.
- No → The site itself is broken or unreachable.

Check CDP console log for errors.

**Confidence:** ***** (Switch to headed + Xvfb) | ***☆☆ (Update user agent)

---


**Related Reading**
- Architecture Guide: [Decision 1 — Single vs Multiple Browsers](#)
- Pattern Catalog: [Event Observer](#)
- War Stories: [Story 13 — The 1-Second Wait That Missed the Data](#)



## PATTERN 14 — Credential Rotation Breaks Login `[AUTH]` `[OPS]`

**Engineering Principle:** Passwords expire. Design your automation to survive credential rotation without manual intervention.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** High — login fails for one account. Manual credential update required. May be recurring.


| P1 — Login dead | 5 min | 5 min | One account |

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Password expired (30/60/90 day policy) | High |
| 2 | Password manually changed by account owner | Medium |
| 3 | MFA or 2FA enabled on the account | Medium |

### Fix

```python
if (datetime.now() - last_successful_login).days > 60:
    send_alert("Credentials may have expired")
```

**Confidence:** ****☆ (Update .env) | **☆☆☆ (Secrets manager rotation)

### Prevention

- Track last successful login date
- Alert before credential expiry window
- Use a secrets manager (Vault, AWS Secrets Manager) for automatic rotation

---

### Recovery Verification

- [ ] Pipeline tracing confirms records at every stage
- [ ] Extract > 0, Validate > 0, Store > 0
- [ ] Screenshot confirms page is not an error state



### Recovery Verification

- [ ] Lock mechanism in place: `filelock` or database advisory lock
- [ ] Duplicate records identified and removed
- [ ] Concurrency test: running two jobs simultaneously fails gracefully



### Recovery Verification

- [ ] Page renders content with headless mode disabled
- [ ] Console errors captured and reviewed
- [ ] CDP network log confirms API data received



### Recovery Verification

- [ ] New credentials stored in `.env` or secrets manager
- [ ] Login test: runs a dry login and confirms success
- [ ] Alert threshold updated: expiry warning set for 7 days before rotation




**Related Reading**
- Architecture Guide: [Decision 8 — Browser Profiles vs Stateless Sessions](#)
- Design Review: [Security — Credential Rotation](#)
- War Stories: [Story 6 — Account Lockout From 5 Login Retries](#)



## PATTERN 15 — Profile Corruption `[BROWSER]` `[STORAGE]`

**Engineering Principle:** Profiles are disposable infrastructure. The automation must survive profile deletion and recreation.

| Severity | Diagnosis Time | Repair Time | Blast Radius |
|----------|---------------|-------------|--------------|
**Business Impact:** Medium — one worker unable to start. Profile can be recreated and session re-established.


| P1 — Browser won't start | 10 min | 15 min | One worker |

### Symptom

```
Chrome crashes on startup with existing profile.
"Your profile could not be opened correctly."
```

### Root Causes

| # | Cause | Likelihood |
|---|-------|------------|
| 1 | Two workers wrote to same profile simultaneously | High |
| 2 | Chrome version upgrade incompatible with old profile | Medium |
| 3 | Disk full during profile write | Low |

### Fix

```python
import shutil
shutil.rmtree(profile_dir, ignore_errors=True)
os.makedirs(profile_dir)
```

**Confidence:** ****☆ (Delete and recreate profile) | *☆☆☆☆ (Repair corrupted profile)

### Prevention

- One profile per worker — never share
- Run pre-launch profile health check
- Design automation to survive profile loss — re-authentication should be automated

---

### Recovery Verification

- [ ] Profile deleted and recreated successfully
- [ ] Re-authentication works: login form submitted correctly
- [ ] Previous session state confirmed lost (expected — profile is disposable)




**Related Reading**
- Architecture Guide: [Decision 7 — Profiles per Worker](#)
- Pattern Catalog: [Checkpoint/Resume](#)
- War Stories: [Story 3 — Chrome Update Corrupted Profiles](#)



## QUICK REFERENCE — Symptom to Pattern

| Symptom | Pattern | Tag |
|---------|---------|-----|
| "Unable to connect to browser" | 1 — Chrome Won't Start | `[INFRA]` |
| "Profile locked" | 2 — Profile Locked | `[BROWSER]` |
| Login page appears mid-run | 3 — Session Expired | `[AUTH]` |
| Selector returns nothing | 4 — Selector Failure | `[EXTRACT]` |
| Page never finishes loading | 5 — Page Timeout | `[NAV]` |
| WebSocket disconnected | 6 — CDP Connection Lost | `[BROWSER]` |
| All records quarantined | 7 — Validation Failure | `[VALIDATE]` |
| HTTP 429 / 403 | 8 — Rate Limited | `[INFRA]` |
| Container killed (exit 137) | 9 — Out of Memory | `[INFRA]` |
| Quarantine file gigabytes | 10 — Quarantine Growth | `[OPS]` |
| 0 records extracted | 11 — No Output | `[EXTRACT]` |
| Duplicate records | 12 — Job Overlap | `[OPS]` |
| White/blank page | 13 — Page Is Blank | `[NAV]` |
| Login suddenly fails | 14 — Credential Rotation | `[AUTH]` |
| Chrome crashes on profile | 15 — Profile Corruption | `[BROWSER]` |

---

## RECOVERY DECISION TREE

```text
Alert: Automation failed
    ↓
Classify by symptom (see Quick Reference)
    ↓
┌─ Browser issue?
│   YES → Chrome crash? → Restart → Resume
│   │    → Profile corrupt? → Delete + recreate → Resume
│   │    → CDP lost? → Reconnect → Resume
│   NO
│
├─ Authentication issue?
│   YES → Session expired? → Re-login → Resume
│   │    → Login failed? → Stop. Alert human.
│   │    → MFA required? → Pause. Wait for approval.
│   NO
│
├─ Navigation issue?
│   YES → Timeout? → Retry with backoff
│   │    → Blank page? → Check headless + user agent
│   │    → Wrong page? → Re-navigate
│   NO
│
├─ Extraction issue?
│   YES → Selector missing? → Stop. Alert human.
│   │    → 0 records? → Validate page state first
│   │    → Wrong format? → Update schema
│   NO
│
├─ Validation issue?
│   YES → All fail? → Stop. Website likely changed.
│   │    → Some fail? → Continue. Quarantine individual records.
│   NO
│
├─ Storage issue?
│   YES → DB locked? → Wait. Retry.
│   │    → Disk full? → Stop. Alert ops.
│   NO
│
└─ Operations issue?
    YES → Job overlap? → Kill duplicate. Add lock.
         → Credential expired? → Update. Alert.
```

---

## FALSE POSITIVES — When "Failure" Is Actually Correct

Before treating any symptom as a failure, rule out that it is actually correct behavior.

| Symptom | Possible False Positive | How to Check |
|---------|------------------------|--------------|
| 0 products extracted | Supplier has no inventory today | Look for a "no results" message on page |
| No login (redirect to login) | Weekend maintenance page | Check for maintenance banner text |
| Slow page load (30s) | Temporary CDN slowness | Retry once. If still slow, log and continue. |
| All records fail validation | Website changed data format | Compare quarantined data with new format |
| HTTP 403 | IP blocked on shared network | Test from a different IP |
| Empty table | Query returned zero results by design | Check for pagination or "no data" indicator |

**Production Rule:** A false positive is worse than a missed failure — it erodes trust in the monitoring system. Design every alert to be verifiable with a single check.

---

## INCIDENT TIMELINE

```
03:01 — Alert: "Price extraction: 0 records extracted (expected > 100)"
03:02 — Operator acknowledges alert.
03:03 — Checks run metrics. Last 3 runs normal. First failure.
03:04 — Captures screenshot. Page shows empty table with spinner.
03:05 — Captures HTML dump. Table exists but has 0 rows.
03:06 — Checks CDP network log. API returned 504.
03:08 — Checks console. Error: "Uncaught TypeError: Cannot read properties of null"
03:10 — Classifies: transient (API gateway timeout).
03:11 — Executes recovery: restart browser, re-navigate.
03:12 — Recovery succeeds. 125 products extracted.
03:14 — Validation passes. Records stored.
03:16 — Alert auto-resolves.
03:20 — Postmortem written. Root cause: upstream API degraded.
```

---

## POSTMORTEM TEMPLATE

```text
## POSTMORTEM — [DATE]

### Incident Summary
[One paragraph: what happened, when, impact]

### Severity
P0 / P1 / P2 / P3

### Root Cause
[One sentence: what actually broke]

### Why It Happened
- [Reason 1]
- [Reason 2]

### Why Monitoring Missed It
- [Gap in monitoring]
- [False positive or false negative]

### Fix Applied
[What was changed to resolve the incident]

### Permanent Prevention
[What prevents this from happening again — code change, process change, monitoring addition]

### Detection Improvement
[New alert or check that would have caught this faster]

### Owner
[Who is responsible for the follow-up items]

### Follow-up Items
- [ ] Item 1 (due date)
- [ ] Item 2 (due date)
- [ ] Item 3 (due date)

### Lessons Learned
[One sentence: what the team should remember from this incident]
```

---

## OPERATIONAL CHECKLIST

### Pre-Deployment
- [ ] Chrome launch tested in target environment
- [ ] Profile isolation enforced
- [ ] Session validation before every extraction
- [ ] Selectors have fallback chains
- [ ] Resource blocking configured
- [ ] Job lock prevents overlaps
- [ ] Validation alerts on >10% failure rate
- [ ] Quarantine has retention policy
- [ ] Rate limiting implemented
- [ ] CDP health monitored before each interaction
- [ ] Credential expiry monitored
- [ ] Profiles are disposable — automation survives recreation
- [ ] Exit code 0 not trusted without data verification

### During Incident
- [ ] Acknowledge alert (within 5 min)
- [ ] Determine severity (P0-P3)
- [ ] Collect evidence (screenshot, HTML, console, network)
- [ ] Classify failure (by category + confidence)
- [ ] Choose recovery strategy (Restart / Retry / Recover / Stop)
- [ ] Execute recovery
- [ ] Write postmortem (within 24 hours)

### Weekly
- [ ] Review quarantine patterns (same error repeating?)
- [ ] Review success rate trend (degrading?)
- [ ] Check for website changes (structural comparison alerts?)
- [ ] Verify Chrome version (any breaking changes?)

### Monthly
- [ ] Review all automations (still needed? still running?)
- [ ] Update dependency versions (Python, nodriver, Chrome)
- [ ] Review monitoring thresholds (too sensitive? not sensitive enough?)
- [ ] Test credential rotation (update .env, verify login)
- [ ] Review incident postmortems (patterns? recurring themes?)

---

## Key Principles

1. **Retry only transient failures.** Login failures, selector failures, and validation failures are permanent — retrying them makes things worse.

2. **Capture evidence before recovery.** Screenshot, HTML dump, and console output must be preserved before Chrome is restarted.

3. **One profile per worker.** Shared profiles are the root cause of an entire class of unreproducible bugs.

4. **Validate sessions before extraction.** A page that loads but shows a login form is a session failure, not a navigation failure.

5. **Outcome matters more than exit codes.** Exit code 0 with zero records is a failure. Monitor data volume, not just execution status.

> **"Every retry is a request to a struggling system."**

> **"Automation isn't successful because it ran. It's successful because the outcome is correct."**
