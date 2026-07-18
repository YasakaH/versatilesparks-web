# Operating Browser Automation in Production

> The Operator's Handbook


## Previously

You designed, built, and deployed a production automation system. It has Docker, scheduling, monitoring, recovery, validation, and data provenance.

Now you need to operate it — day and night, through failures, upgrades, and incidents.


## Why This Chapter Exists

An automation system is not finished when it deploys. It is finished when an operator can respond to any failure mode without reading the source code. This chapter provides the runbooks, checklists, and decision frameworks that make that possible.


## The Cost of Getting This Wrong

| Gap | Outcome | Cost |
|-----|---------|------|
| No runbook | Alert fires at 3 AM. Operator has no idea what to check. | Incident response time: hours instead of minutes |
| No operator checklists | Routine maintenance is forgotten | Chrome updates break automation, nobody noticed the deprecation warning |
| No recovery decision matrix | Every failure is treated the same | Retrying permanent failures, stopping on recoverable ones |
| No preflight checks | Deployment fails at 2 AM — wrong .env, missing Chrome | Rollback takes 30 minutes, schedule is missed |




This is not a recipe. It is a narrative walkthrough of what happens when production automation runs, fails, and recovers — from the scheduler triggering a job to an alert firing at 3 AM. Senior operators use this guide to understand the automation lifecycle and build their runbooks.


## 00 — Scheduler Trigger

A cron job fires on your VPS. The scheduler process starts.

### What Happens

1. The system reads the environment configuration
2. Secrets are loaded from `.env` file
3. The working directory is set
4. A health check verifies the previous run completed

### What Could Go Wrong

- The `.env` file is missing → automation fails immediately
- Two cron instances overlap → lock file prevents duplicate execution
- The system clock is wrong → scheduled time is incorrect

### Decision: Should I Preflight?

| Condition | Check |
|-----------|-------|
| New deployment | Verify `.env` exists, required vars set, Chrome binary at expected path |
| Routine run | Quick check: previous run ended, disk space > 1GB, network reachable |
| After incident | Full preflight: profile not corrupted, lock released, metrics reset |

**Production rule:** Every job should start with a preflight check that verifies configuration, secrets, and system state. A preflight that takes 10 seconds can save 10 hours of debugging.


## 01 — Worker Initialization

The automation worker starts. It launches the browser.

### What Happens

1. Python imports modules and initializes logging
2. `common/metrics.py` starts a new run record
3. `common/logging.py` configures structured output
4. Chrome launches with the configured profile, locale, and command-line flags

### What Could Go Wrong

- Chrome binary not found → Docker ensures reproducibility
- Profile locked from previous crash → recovery process cleans stale locks
- Shared memory too small → `shm_size: 2gb` in docker-compose
- Port conflict → sequential debugging ports (9222, 9223, ...)

### Decision: Launch Failed. What Now?

```text
1. Is Chrome installed?        → If no, check Dockerfile or PATH
2. Is the profile locked?      → If yes, remove lockfile, run recovery
3. Did it timeout?             → If yes, check shm_size, GPU args
4. Did it crash immediately?   → If yes, check Chrome version, sandbox
```

Document the exact error message. Nine out of ten launch failures are caused by the same three problems (missing binary, locked profile, shared memory) and the fix is in the Dockerfile, not the automation code.


## 05 — Authentication Verification

The automation checks whether the current session is still valid.

### What Happens

1. Load saved cookies from the profile
2. Navigate to a known authenticated endpoint
3. Check for login indicators or redirect to login page

### What Could Go Wrong

- Session expired → re-login with saved credentials
- Cookie file corrupted → create fresh session
- MFA challenge → manual intervention required

### Decision: Session Failed. Should I Re-Login?

| Condition | Action |
|-----------|--------|
| Session expired normally | Re-login automatically. This is expected. |
| Login failed (wrong credentials) | Stop. Alert human. Credentials may have rotated. |
| CAPTCHA appeared | Stop. Alert human. Anti-bot triggered. |
| Account locked | Stop. Alert human. Too many failed attempts. |
| MFA required | Pause. Wait for manual approval. Poll approval file. |

**Never retry a failed login more than 3 times.** Each retry increases lockout risk.


## 10 — Execution Begins

The main automation logic runs — extracting data, filling forms, or navigating pages.

### What Happens

1. Target URL is loaded
2. CDP handlers are registered for network and console monitoring
3. Elements are located and interacted with
4. Data is extracted and collected

### What Could Go Wrong

- Page times out → retry with increasing backoff
- CDP handler overload → 1000+ requests in 2 seconds flood the queue
- `common/network_queue.py` uses asyncio.Queue to rate-limit processing

### Decision: Extraction Returns Zero Results. What's Wrong?

```text
1. Did the page load?           → Check screenshot. Was it a blank page, error page, or login page?
2. Did the selector match?      → Check HTML dump. Is the element present with different attributes?
3. Did the data arrive?         → Check CDP network log. Did the API call return data?
4. Did the validation reject?   → Check quarantine. Were records rejected by schema?
```

Each question eliminates one failure domain. Do not skip to "fix the selector" until you have confirmed the page is the correct page and the data correct.


## 20 — Validation

Extracted data passes through the validation pipeline.

### What Happens

1. Each record is validated against the expected schema
2. Valid records proceed to storage
3. Invalid records are quarantined with error details
4. If failure rate exceeds 10%, an alert is triggered

### What Could Go Wrong

- Validation schema doesn't match actual data → website may have changed
- All records fail → systematic problem, automation should pause
- Quarantine file grows unbounded → set disk usage monitoring

### Decision: All Records Failed Validation. Stop or Continue?

| Failure Rate | Action |
|-------------|--------|
| < 5% | Continue. Quarantine individual records. |
| 5-10% | Continue. Log warning. Review after run. |
| 10-50% | Alert. Review quarantine. Website may have changed. |
| > 50% | Stop. Systematic failure. Do not store any data. |

A 5% failure rate is normal website variation (occasional malformed data). A 100% failure rate means the extraction is broken — continuing would store an empty dataset that downstream systems treat as a legitimate result.


## 30 — Storage

Validated data is written to the database.

### What Happens

1. `common/data_pipeline.py` checks for duplicate keys
2. `UPSERT` pattern inserts or updates records
3. Metrics are recorded with record count and runtime

### What Could Go Wrong

- Database locked (SQLite with concurrent workers) → use WAL mode
- Disk full → monitor disk usage, alert before exhaustion
- Record count is 0 (no data found) → could mean page changed, not error


## 00 — Failure Scenario

Something breaks. Here is how recovery works.

### Example: Browser Crash

```text
1. Chrome process dies unexpectedly
2. CDP connection closes with ConnectionClosedError
3. `common/recovery.py` classifies: BROWSER_CRASH
4. Recovery strategy: restart browser
5. If restart succeeds: resume from last checkpoint
6. If restart fails: STOP, alert human
```

### Example: Session Expired Mid-Run

```text
1. API returns 401 Unauthorized
2. `common/recovery.py` classifies: SESSION_EXPIRED
3. Recovery strategy: re-authenticate
4. If login succeeds: continue from current point
5. If login fails: STOP, alert human
```



### Real Incident Timeline

```
03:01 — Alert fires: "Price extraction: 0 records extracted (expected > 100)"
03:02 — Operator acknowledges alert.
03:03 — Checks run metrics. Last 3 runs were normal. This is the first failure.
03:04 — Captures screenshot. Page shows empty table with "loading" spinner stuck.
03:05 — Captures HTML dump. The table exists but has zero rows.
03:06 — Checks CDP network log. The API call to fetch product data returned 504.
03:08 — Checks console. Error: "Uncaught TypeError: Cannot read properties of null"
03:10 — Classifies failure: transient (API gateway timeout + JS error from null data).
03:11 — Executes recovery: restart browser, re-navigate to page.
03:12 — Recovery succeeds. Page loads with 125 products. Validation passes.
03:14 — Automation resumes from where it failed. Records extracted.
03:16 — Run completes. 125 products stored. Alert auto-resolves.
03:20 — Operator documents incident. Root cause: upstream API degraded.
```

Every step has a corresponding tool or log entry. No guesswork.


### Recovery Decision Matrix

| Failure | Evidence | Recoverable? | Strategy | Risk of Retry |
|---------|----------|-------------|----------|---------------|
| Browser crash | ConnectionClosedError | Yes | Restart browser | Low — clean state |
| Session expired | 401, login redirect | Yes | Re-authenticate | Low — design for this |
| Network timeout | asyncio.TimeoutError | Yes | Backoff + retry | Medium — amplify load |
| Selector not found | NoSuchElementException | No | Stop, alert | High — will always fail |
| No data extracted | Zero records | Conditional | Validate structure first | High — may corrupt DB |
| Disk full | write() IOError | No | Stop, alert | High — cannot recover |
| All records fail validation | 100% quarantine rate | No | Stop, alert | High — systematic failure |

### When to Give Up

Some failures should not be recovered automatically:

- Authentication changed (password rotated)
- Website structure redesigned (all selectors broken)
- Legal/ToS changes (you may not have permission anymore)
- Account suspended or flagged

These require human judgment. The automation should alert and stop.


## 05 — Recovery

The automation has recovered and continues processing.

### What Happens

1. Browser restarts (if needed)
2. Session is re-established (if needed)
3. Automation resumes from the last known good state
4. The recovery event is logged for post-mortem analysis

### Post-Recovery Validation

After any recovery, validate that the system is in a correct state before continuing:

- [ ] Browser process is running and responsive
- [ ] CDP connection is established
- [ ] Session is authenticated (if required)
- [ ] Page navigates correctly
- [ ] First record extracts successfully

Do not assume recovery succeeded because the browser started. A browser that launches but cannot reach the internet is worse than no browser — it produces error messages instead of failure alerts.


## 10 — Cleanup

### What Happens

1. Metrics are finalized and written
2. Logs are rotated (if needed)
3. Browser is closed
4. Lock file is released

### What Could Go Wrong

- Browser close times out → force kill by PID
- Metrics write fails → data still valid, but alert for investigation
- Lock file not released → next run fails at preflight


## Operator Checklists

### Morning Checklist

First check of the day. Should take 5 minutes.

- [ ] All scheduled jobs from last night completed
- [ ] No alerts firing (Slack, email, dashboard)
- [ ] Quarantine file is empty or contains expected count
- [ ] Disk usage < 80% on all volumes
- [ ] Database size within normal range
- [ ] Yesterday's data looks reasonable (spot-check 3 records)
- [ ] All Chrome profiles are healthy (not corrupted)
- [ ] `.env` has not expired (credentials, API keys)

### Weekly Checklist

Deeper review. Should take 15 minutes.

- [ ] Review this week's failure rate and compare to last week
- [ ] Review quarantine records — are there patterns? (same selector failing, same supplier?)
- [ ] Check for Chrome updates that may affect behavior
- [ ] Review logs for warnings that did not trigger alerts
- [ ] Verify backup is running correctly
- [ ] Test alert delivery (send a test notification)
- [ ] Rotate any credentials that expire this week

### Monthly Checklist

Architecture review. Should take 30 minutes.

- [ ] Review all automation jobs: are they all still needed? Still running?
- [ ] Review page count, record count, and success rate trends
- [ ] Check for websites that have redesigned or changed authentication
- [ ] Update dependency versions (Python packages, nodriver, Chrome)
- [ ] Review monitoring thresholds: are they too sensitive (noise) or not sensitive enough (missed failures)?
- [ ] Review operator checklists: are they still accurate?
- [ ] Plan next month's work: improvements, new targets, deprecations

### Incident Checklist

When an alert fires at 3 AM.

1. **Acknowledge the alert.** Silence or acknowledge within 5 minutes.
2. **Determine severity.** Is this a single record, single job, or platform-wide failure?
3. **Collect evidence.** Screenshot, HTML dump, console log, network capture.
4. **Classify the failure.** Hard, soft, silent, or business? Transient or permanent?
5. **Decide: recover or escalate?** Use the recovery decision matrix above.
6. **Execute recovery.** Restart, re-authenticate, or stop.
7. **Document.** One paragraph: what happened, what was the root cause, what was the fix.
8. **Follow up.** Within 24 hours, determine if a code change is needed.

### Upgrade Checklist

Before upgrading Chrome, nodriver, or Python.

- [ ] Read the changelog (breaking changes, deprecations)
- [ ] Run the automation in a staging environment
- [ ] Compare record counts and success rates: staging vs production
- [ ] Check for deprecated CDP events or arguments
- [ ] Update the compatibility matrix in README
- [ ] Run the full test suite (if one exists)
- [ ] Deploy to production during low-activity hours
- [ ] Monitor the first 3 production runs after upgrade


## The Full Production Cycle

```text
00:00  Scheduler fires
00:01  Worker start + Chrome launch
00:05  Auth verification
00:10  Extraction / interaction
00:20  Data validation
00:30  Storage + metrics
00:35  Cleanup + report
      ↓
03:00  (Something fails)
03:05  Recovery
03:10  Resume + continue
```


## Key Takeaways

1. **Automation is not a script — it is a lifecycle.** Every phase can fail independently.
2. **Failure classification is more important than retrying.** A browser crash and a session expiry need different recovery strategies.
3. **Observability is not optional.** Without metrics, alerts, and logs, you cannot tell whether your automation is working.
4. **Validation is not optional.** A scraper that produces bad data is worse than a scraper that fails.
5. **Design for 3 AM.** If your automation crashes at 3 AM, will it recover automatically? Will anyone be notified? Will the logs be useful for diagnosis?
6. **Operators need runbooks, not code.** When a human responds to an alert, they should follow a checklist — not read the Python source to understand what happened.
