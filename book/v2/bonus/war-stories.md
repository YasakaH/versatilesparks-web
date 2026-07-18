# Browser Automation War Stories

## 20 Production Incidents — What Broke, Why, and What We Learned

> **Read This If...**
> You want to learn from other people's production incidents instead of experiencing them yourself. Each story is a real failure mode that has happened to real automation teams.

---

### How to Read These Stories

Each story follows the same format:

```
Situation      → What was the automation supposed to do?
What We Thought → What everyone assumed was happening
What Happened   → The actual failure (with timeline)
Root Cause      → Why it broke
Fix             → How it was resolved
Lesson          → The engineering principle to remember
```

---> **Quick Take**
> If you're short on time:
> - ✓ Read Story 4 (retry loops DDoS suppliers) and Story 5 (exit code 0 != success).
> - ✓ Read Story 10 (alert storms) and Story 20 (18-month silent failure).
> - ✓ Every story ends with a lesson — scan the Lessons first.
> - ✓ Warning: reading these will make you paranoid. That is the point.
> 
> Estimated reading: 20 minutes (or 5 minutes scanning lessons)
> 



## STORY 1 — The Login That Failed Only on Mondays

### Situation

An agency automated client reporting for 12 SaaS platforms. Each platform required a separate login. The automation logged into all 12 every morning and extracted reports.

### What We Thought

"We need to log in every run because sessions expire after 24 hours."

### What Happened

Monday morning: 3 of 12 platforms failed to log in. Tuesday through Friday: everything worked. Every Monday for five weeks, the same 3 platforms failed.

The developer spent weeks debugging: wrong password? Cookie expiry? Account lockout? Nothing explained the Monday-only pattern.

### Root Cause

The 3 failing platforms had 7-day session expiry. The automation logged in successfully on Monday, reused the session Tuesday through Friday, and never noticed that the session persisted across days. On Monday of the next week, the 7-day session had expired. The automation got a login failure — but the error message was "session expired," not "wrong password."

The automation logged in every run regardless of session state. The login was succeeding... until the session actually expired, at which point the login failed because the stale session was still in the profile.

### Fix

Add session validation before login. Check if the current session is still valid. Only log in if it is not.

```python
async def ensure_session(page):
    if not await is_authenticated(page):
        await login(page)
```

### Lesson

> Logging in on every run does not protect against session expiry. It only protects against the FIRST session failure. Always validate session state before deciding to re-authenticate.


**Related Reading**
- Failure Playbook: [Pattern 3 — Session Expired Mid-Run](#)
- Architecture Guide: [Decision 8 — Profiles vs Sessions](#)
- Pattern Catalog: [Idempotent Consumer](#)



- **Could this have been prevented?** YES → [Decision 8 — Profiles vs Sessions](architecture-field-guide.md) and [Pattern 3 — Session Validation](failure-playbook.md)

---

## STORY 2 — The Selector That Broke Because of A/B Testing

### Situation

An e-commerce price monitor extracted product prices from a major marketplace. The selector was `.price-value`.

### What We Thought

"We have a stable CSS class. It worked for 6 months. It will continue to work."

### What Happened

The marketplace ran an A/B test. 50% of users saw the old page with `.price-value`. 50% saw a new design with `.product-price`. The automation hit both versions randomly across different runs.

Some days, prices extracted correctly. Other days, the selector returned `null`. The developer assumed network issues and added longer waits. Nothing helped because the wait time was never the problem — the class name changed 50% of the time.

### Root Cause

The selector was tied to a CSS class that was part of an A/B test variant. A/B tests are not frontend refactors — they are a permanent feature of modern web applications. Any selector that depends on a non-data-attribute is vulnerable to A/B test variations.

### Fix

Switch to a data attribute selector:
```css
[data-price]
```

Data attributes are typically not changed by A/B tests because the JavaScript that reads them would also break.

### Lesson

> A/B testing means your selector is wrong 50% of the time — even when the code is correct. Use data attributes that survive A/B test variants.


**Related Reading**
- Failure Playbook: [Recovery Decision Tree](#)
- Architecture Guide: [Part V — Architecture Evolution](#)
- Pattern Catalog: [Supervisor](#)



- **Could this have been prevented?** YES → [Pattern 4 — Selector Fallback Chains](automation-pattern-catalog.md)

---

## STORY 3 — The Chrome Update That Silently Corrupted Profiles

### Situation

A supplier intelligence pipeline ran 25 Chrome profiles, one per supplier. It worked for 8 months.

### What We Thought

"Our profiles are stable. We never touch them."

### What Happened

After a Chrome update from version 128 to 130, 3 of 25 profiles became corrupted. Chrome crashed on startup with those profiles. The automation tried to launch, failed, and moved to the next supplier. No alert fired because the per-supplier failure was below the 10% alert threshold.

Three suppliers' data went missing for 10 days before anyone noticed.

### Root Cause

Chrome profile formats are not guaranteed to be backward-compatible across major versions. A profile written by Chrome 130 may not be readable by Chrome 128 (if the deployment environment lags), and a profile written by Chrome 128 may need migration on Chrome 130. The migration usually works silently, but edge cases (corrupt IndexedDB, incompatible extension state) can cause the entire profile to fail to load.

### Fix

Add profile health check before launch:
```python
async def check_profile(profile_dir):
    try:
        browser = await launch_browser(user_data_dir=profile_dir)
        await browser.get("about:blank")
        await close_browser(browser)
        return True
    except Exception:
        return False
```

### Lesson

> Browser profiles are not eternal. After every Chrome version upgrade, verify that existing profiles can still be loaded. Design your automation to survive profile deletion — the ability to re-authenticate is more important than the profile itself.


**Related Reading**
- Failure Playbook: [Pattern 3 — Session Expired Mid-Run](#)
- Architecture Guide: [Decision 8 — Profiles vs Sessions](#)
- Pattern Catalog: [Idempotent Consumer](#)



- **Could this have been prevented?** YES → [Decision 7 — Profile per Worker](architecture-field-guide.md) and [Failure Pattern 15](failure-playbook.md)

---

## STORY 4 — The Retry Loop That DDoSed a Supplier

### Situation

A logistics automation checked shipment status from a supplier portal every 5 minutes. If the page failed to load, it retried after 1 second.

### What We Thought

"Retrying faster will get the data sooner."

### What Happened

The supplier's server had a 5-minute outage. The automation retried every second for 5 minutes — 300 requests. The supplier's load balancer interpreted the traffic spike as a DDoS attack and permanently blocked the automation's IP address.

The automation was down for 3 days while the IP was being unblocked.

### Root Cause

The retry strategy had no backoff and no cap. "Retry immediately" meant 60 requests per minute against an already-struggling server.

### Fix

```python
@retry(max_attempts=3, delay=2, backoff=2.0)
```

Maximum 3 retries. First retry after 2 seconds. Second after 4 seconds. Third after 8 seconds. Then escalate.

### Lesson

> Every retry is a request to an already-struggling server. Exponential backoff is not optional — it is a requirement for being a good citizen of the internet. Cap retries at 3. Never retry indefinitely.


**Related Reading**
- Pattern Catalog: [Retry with Backoff](#), [Circuit Breaker](#)
- Failure Playbook: [Pattern 8 — Rate Limited](#)
- Architecture Guide: [Decision 6 — Retry vs Recover vs Restart](#)



- **Could this have been prevented?** YES → [Pattern 6 — Retry with Backoff](automation-pattern-catalog.md) and [Circuit Breaker](automation-pattern-catalog.md)

---

## STORY 5 — The Dashboard That Reported Success While Storing Zero Rows

### Situation

A nightly report automation extracted 47 rows of KPI data from a SaaS dashboard, stored them, and sent a Slack notification.

### What We Thought

"Exit code 0 means the automation worked."

### What Happened

The dashboard's API changed. Instead of returning JSON data, it returned a login page. The extractor parsed the login page HTML and found zero data rows. The script completed without errors. The storage layer wrote zero rows. The Slack notification said "[✓] Report delivered — 0 records."

Nobody noticed "0 records" because the notification said "[✓]" and the exit code was 0. The monitoring dashboard showed green. The team went home.

Three days later, someone opened the report and saw it was empty.

### Root Cause

The monitoring system checked "did the script run?" not "did the script produce data?" The exit code and the Slack notification both reported technical success — and both were irrelevant to the business outcome.

### Fix

Change the monitoring from process-based to outcome-based:
```python
if record_count == 0:
    send_alert("[!] Report generated but contains 0 records")
```

Add data volume monitoring: compare today's record count to the 7-day moving average. Alert on >50% deviation.

### Lesson

> Exit code 0 does not mean "success." It means "the script executed." The only true measure of automation success is correct data in the database.


**Related Reading**
- Architecture Guide: [Decision 13 — Evidence Types](#)
- Failure Playbook: [Pattern 11 — 0 Records Extracted](#)
- Pattern Catalog: [Pipeline](#)



- **Could this have been prevented?** YES → [Decision 13 — Evidence Types](architecture-field-guide.md) and statistical monitoring

---

## STORY 6 — The Account Lockout From 5 Login Retries

### Situation

A nightly automation logged into a banking portal, extracted transaction data, and logged out. One night, the login failed.

### What We Thought

"Retry the login 5 times. One of them will work."

### What Happened

The password had been rotated. The first login attempt failed (wrong password). The automation retried. And retried. And retried. After 5 failed attempts, the bank's security policy locked the account.

The automation was down for 3 days while the IT team processed an account unlock request. The client's end-of-month reconciliation was delayed by a week.

### Root Cause

Login retries were not classified as a permanent failure type. The automation retried a permanent failure (wrong credentials) as if it were a transient failure (network timeout).

### Fix

```python
FAILURE_CLASSIFICATION = {
    "LoginError": FailureType.PERMANENT,   # Never retry
    "TimeoutError": FailureType.TRANSIENT,  # Retry with backoff
}
```

### Lesson

> Login failures are never transient. If a login fails, the credentials are wrong, the session is expired, or the account is locked. None of these are fixed by retrying. Classify login failures as permanent and escalate immediately.


**Related Reading**
- Failure Playbook: [Pattern 3 — Session Expired Mid-Run](#)
- Architecture Guide: [Decision 8 — Profiles vs Sessions](#)
- Pattern Catalog: [Idempotent Consumer](#)



- **Could this have been prevented?** YES → [Decision 6 — Failure Classification](architecture-field-guide.md) and [Failure Pattern 14](failure-playbook.md)

---

## STORY 7 — The Database That Grew 50GB in One Weekend

### Situation

An e-commerce price monitor extracted 50,000 product prices daily and stored them in SQLite.

### What We Thought

"SQLite is fine for our data volume."

### What Happened

The website added a new product category with 500,000 products. The automation extracted all of them — 10x the usual volume — without validation. The SQLite database grew from 2GB to 52GB over the weekend. The VPS disk filled up. Chrome could not write its profile. The automation crashed.

Restoring the automation required: deleting the oversized database, restoring from backup, and adding a per-run storage limit.

### Root Cause

No storage monitoring. No per-run data volume limits. The database was allowed to grow unbounded because "it always fit before."

### Fix

```python
MAX_DB_SIZE_MB = 5000
if db_size > MAX_DB_SIZE_MB:
    send_alert(f"Database size {db_size}MB exceeds limit")
    # Archive old data, then continue
```

### Lesson

> Every automation has a data volume limit. Define it before deployment. Monitor it after deployment. Alert before it is reached — not after it is exceeded.


**Related Reading**
- Architecture Guide: [Decision 13 — Evidence Types](#)
- Failure Playbook: [Pattern 11 — 0 Records Extracted](#)
- Pattern Catalog: [Pipeline](#)



- **Could this have been prevented?** YES → [Cost Table](architecture-field-guide.md) and storage monitoring in [Design Review](automation-design-review.md)

---

## STORY 8 — The CAPTCHA That Wasn't

### Situation

A travel fare monitoring automation searched for flights on a major airline website every 30 minutes.

### What We Thought

"The website is blocking us because of our IP."

### What Happened

The automation started returning empty search results. The developer checked the response: HTTP 200, page loaded, no CAPTCHA visible. Suspecting an IP block, they added a proxy rotation service. The proxy cost $200/month.

Empty results continued. The developer added more proxies. More cost. Same result.

Two weeks later, someone noticed the search form had a new hidden field: `_captchaToken`. The airline had added an invisible CAPTCHA that did not show a challenge — it simply returned empty results when the CAPTCHA score was low. The automation passed the invisible check 10% of the time, which explained the intermittent empty results.

### Root Cause

The developer assumed "no visible CAPTCHA = no anti-bot detection." Invisible CAPTCHAs existed. The detection was on the API layer, not the UI layer.

### Fix

Add a test: manually extract the same search with a known-good browser. Compare the HTML with the automation's HTML. The difference revealed the hidden CAPTCHA field.

### Lesson

> Anti-bot detection is often invisible. If an automation produces empty results, it is not always a selector bug or an IP block. Check for hidden form fields, injected scripts, and API-level detection. Proxy rotation will not fix application-layer detection.


**Related Reading**
- Pattern Catalog: [Retry with Backoff](#), [Circuit Breaker](#)
- Failure Playbook: [Pattern 8 — Rate Limited](#)
- Architecture Guide: [Decision 6 — Retry vs Recover vs Restart](#)



- **Could this have been prevented?** YES → [Decision 9 — Browser vs API](architecture-field-guide.md) and [Pattern 12 — Event Observer](automation-pattern-catalog.md)

---

## STORY 9 — The Timezone Bug That Lost a Day

### Situation

A financial data automation extracted daily exchange rates from a European central bank website and stored them with timestamps.

### What We Thought

"Our timestamps are UTC. UTC is universal."

### What Happened

The automation ran at 23:00 UTC. The European bank's website updated its exchange rates at midnight Central European Time, which was 23:00 UTC during winter — but 22:00 UTC during summer (daylight saving time).

For 6 months of the year, the automation extracted today's rates correctly. For the other 6 months, it extracted tomorrow's rates because the bank updated at 22:00 UTC while the automation ran at 23:00 UTC — one hour after the next day's rates were published.

The finance team reported "rates are always one day ahead" for 6 months before someone connected it to daylight saving time.

### Root Cause

The automation used UTC for its own timestamps but did not account for the bank's timezone-dependent update schedule.

### Fix

```python
import pytz
bank_tz = pytz.timezone("Europe/Berlin")
update_time = bank_tz.localize(datetime(2026, 1, 1, 0, 0))
utc_update_time = update_time.astimezone(pytz.UTC)
```

### Lesson

> UTC timestamps in your database do not guarantee correct timing. If the source you are scraping operates in a different timezone with daylight saving, your schedule must account for it. Test your automation's timing at both DST boundaries.


**Related Reading**
- Failure Playbook: [Recovery Decision Tree](#)
- Architecture Guide: [Part V — Architecture Evolution](#)
- Pattern Catalog: [Supervisor](#)



- **Could this have been prevented?** YES → Timezone test in [Design Review](automation-design-review.md) — test at both DST boundaries

---

## STORY 10 — The Alert That Fired 500 Times in One Night

### Situation

A monitoring dashboard checked automation health every 5 minutes. If a run failed, it sent a Slack alert.

### What We Thought

"Every failure needs an alert."

### What Happened

A transient network outage caused 12 automations to fail simultaneously. Each failure triggered a Slack alert. The monitoring checked every 5 minutes. Each check found the same 12 failures. 12 alerts × 12 checks per hour × 8 hours = 1,152 Slack notifications.

The on-call engineer's phone vibrated continuously for 8 hours. They silenced Slack notifications after the first 50 messages. A real failure at 4 AM was missed because the engineer had muted alerts from the noise.

### Root Cause

No alert deduplication. No alert throttling. No escalation policy. Every failure == every alert.

### Fix

```python
ALERT_COOLDOWN_MINUTES = 30
last_alert_time = {}

async def send_alert(message):
    if message in last_alert_time:
        elapsed = time.time() - last_alert_time[message]
        if elapsed < ALERT_COOLDOWN_MINUTES * 60:
            return  # Suppress duplicate
    last_alert_time[message] = time.time()
    await slack.send(message)
```

### Lesson

> Every alert must have a deduplication window and a maximum rate. An alert that fires 500 times is not an alert — it is noise that hides real failures. Design your alerting as if the on-call engineer has a family and needs to sleep.


**Related Reading**
- Architecture Guide: [Decision 13 — Evidence Types](#)
- Failure Playbook: [Pattern 11 — 0 Records Extracted](#)
- Pattern Catalog: [Pipeline](#)



- **Could this have been prevented?** YES → [Design Review — Alert Deduplication](automation-design-review.md) and [Failure Pattern 8](failure-playbook.md)

---

## STORY 11 — The Migration That Forgot the Profiles

### Situation

A consulting firm migrated 15 client automations from a shared VPS to Docker containers on separate servers.

### What We Thought

"Copy the code. Copy the `.env`. Deploy."

### What Happened

The code deployed successfully. The `.env` files were copied. But the profiles — which contained authentication sessions, cookies, and stored preferences — were left on the old VPS.

All 15 automations failed on first run. Each one tried to re-authenticate. 5 of them hit MFA challenges that required manual approval. 3 of them were permanently locked out because the account security policy flagged the new IP as suspicious.

The migration took 3 days instead of 3 hours.

### Root Cause

Profiles were treated as ephemeral cache, not as persistent state. The migration plan included code, configuration, and cron jobs — but not the profile directories.

### Fix

Include profiles in the deployment checklist:
```yaml
migration:
  - Copy code
  - Copy .env
  - Copy profiles/
  - Verify profile permissions
  - Test authentication
```

### Lesson

> Browser profiles are state. If your deployment process does not explicitly transfer state, your automation will lose its sessions. Add profiles to your deployment checklist alongside code and configuration.


**Related Reading**
- Architecture Guide: [Decision 13 — Evidence Types](#)
- Failure Playbook: [Pattern 11 — 0 Records Extracted](#)
- Pattern Catalog: [Pipeline](#)



- **Could this have been prevented?** YES → [Decision 7 — Profiles](architecture-field-guide.md) — include profiles in deployment checklist

---

## STORY 12 — The Endless Loop That Cost $5,000 in API Fees

### Situation

An automation extracted product listings from a marketplace that charged per API call (not a browser-based scraper — a paid API).

### What We Thought

"The API returns 100 results per page. We handle pagination."

### What Happened

The automation requested page 1, got 100 results, requested page 2, got 100 results — and kept going. The API returned 100 results for every page, even beyond the actual product count. Instead of returning an empty page at the end, it returned the last 100 products again.

The automation did not detect duplicates. It requested pages until it hit a hardcoded limit of 10,000 pages. That was 1,000,000 API calls at $0.005 each. Total cost: $5,000.

### Root Cause

The pagination code assumed the API would return an empty page at the end. It did not. The code had no deduplication check and no cost-aware stop condition.

### Fix

```python
seen_ids = set()
while page < max_pages:
    results = await api.get(page)
    if not results:
        break  # Normal end
    new_ids = {r["id"] for r in results}
    if new_ids.issubset(seen_ids):
        break  # We've seen all these before — pagination loop
    seen_ids.update(new_ids)
    page += 1
```

### Lesson

> Never trust the server to tell you when pagination is done. Implement client-side deduplication and a maximum cost threshold. If the API charges per call, your pagination loop is a financial risk.


**Related Reading**
- Pattern Catalog: [Checkpoint/Resume](#), [Saga](#)
- Failure Playbook: [Pattern 12 — Job Overlap](#)
- Architecture Guide: [Decision 4 — Cron vs Scheduler](#)



- **Could this have been prevented?** YES → [Pattern 7 — Checkpoint/Resume](automation-pattern-catalog.md) with deduplication check

---

## STORY 13 — The 1-Second Wait That Missed the Data

### Situation

An automation extracted data from a dashboard that loaded a table via XHR after the page render.

### What We Thought

"Wait 1 second after page load. The XHR will complete by then."

### What Happened

The automation ran successfully for 8 months. Then the dashboard team added a second XHR call to load a new feature. The second call took 3 seconds. The 1-second wait was no longer sufficient.

The automation extracted the table from the first XHR correctly — but the second XHR contained critical data that had been added to the report. The report was "correct" by every previous measure. It just was no longer complete.

### Root Cause

A hardcoded wait is always a guess. It worked until the page evolved beyond the guess. The developer who set the 1-second wait had moved on. Nobody knew why it was 1 second.

### Fix

Replace the wait with a condition:
```python
# Wait for a specific element that only appears after ALL XHR calls complete
await page.wait_for(".report-footer", timeout=15)
```

### Lesson

> Every `time.sleep(N)` in your code is a time bomb with an unknown fuse. The fuse is "when the page loads slower than N seconds." Always wait for a condition, not a duration. And document why that condition is the correct signal.


**Related Reading**
- Failure Playbook: [Recovery Decision Tree](#)
- Architecture Guide: [Part V — Architecture Evolution](#)
- Pattern Catalog: [Supervisor](#)



- **Could this have been prevented?** YES → [Pattern 12 — Event Observer](automation-pattern-catalog.md) — wait for a condition, not a duration

---

## STORY 14 — The Profile That Belonged to Two Clients

### Situation

An agency ran 10 client automations on one server. Each had its own profile directory.

### What We Thought

"Each client has their own profile. They are isolated."

### What Happened

Two client profiles were accidentally configured with the same directory path. The automation logged into Client A's portal, stored cookies in `profiles/client-a/`. Then it logged into Client B's portal, which happened to be the same portal with a different account. The cookies from Client A's session overwrote Client B's session.

Client B started seeing Client A's data in their reports. For three weeks.

### Root Cause

The profile paths were configured in a shared config file. A copy-paste error set both paths to `profiles/client-a/`. The error was invisible because both automations launched and ran successfully — they just used the wrong session.

### Fix

Add profile validation on startup:
```python
expected_profile = f"profiles/{client_name}/"
actual_profile = config.get("PROFILE_DIR")
assert expected_profile in actual_profile, \
    f"Profile mismatch: expected {expected_profile}, got {actual_profile}"
```

### Lesson

> Shared infrastructure requires defense-in-depth. Configuration validation, startup assertions, and runtime checks all catch different classes of errors. A startup assertion that fails fast is better than corrupted data that is discovered weeks later.


**Related Reading**
- Failure Playbook: [Pattern 3 — Session Expired Mid-Run](#)
- Architecture Guide: [Decision 8 — Profiles vs Sessions](#)
- Pattern Catalog: [Idempotent Consumer](#)



- **Could this have been prevented?** YES → [Decision 7 — Profile per Worker](architecture-field-guide.md) and startup assertions

---

## STORY 15 — The Heartbeat That Stopped

### Situation

A monitoring system checked automation health by sending a heartbeat every 5 minutes. If the heartbeat stopped, it alerted.

### What We Thought

"The heartbeat proves the automation is alive."

### What Happened

The heartbeat stopped at 2:00 AM on a Sunday. No alert fired. The monitoring system was checked at 9:00 AM Monday — the heartbeat was missing, but nobody had noticed because the monitoring dashboard was only checked during business hours.

The automation had been down for 31 hours. The client noticed before the agency did.

### Root Cause

The heartbeat was monitored, but the monitoring dashboard itself had no alerting. If the heartbeat stopped outside business hours, nobody would know until someone opened the dashboard. The monitoring system monitored the automation, but nobody monitored the monitoring system.

### Fix

Add a heartbeat for the heartbeat:
```python
# Every 5 minutes
await send_heartbeat(service="price-monitor")
# If heartbeat is missing for 15 minutes → alert on-call via PagerDuty
```

The PagerDuty alert is independent of the monitoring dashboard. It does not require anyone to open a browser.

### Lesson

> If your monitoring system does not have its own alerting, you do not have a monitoring system — you have a dashboard that you check manually. Design your monitoring to wake someone up, not just to show a green light during office hours.


**Related Reading**
- Failure Playbook: [Recovery Decision Tree](#)
- Architecture Guide: [Part V — Architecture Evolution](#)
- Pattern Catalog: [Supervisor](#)



- **Could this have been prevented?** YES → [Design Review — Monitoring](automation-design-review.md) — monitor the monitoring system

---

## STORY 16 — The Deployment That Passed All Tests and Broke Everything

### Situation

A team built a new version of an automation with improved selectors, better error handling, and faster extraction. They ran the test suite. All tests passed. They deployed to production.

### What We Thought

"All tests pass. The deployment is safe."

### What Happened

The test suite used a staging environment with test data. The production environment had real data with different formatting. The new selectors were optimized for the test data format. On real data, 30% of extractions failed silently — the data was parsed but with wrong values.

For example, the new code assumed prices were always integers. Production had prices like ₹89,999.50. The integer parser dropped the decimal. Every price was off by up to 50 paise. The error was invisible because each individual price was close to the correct value.

### Root Cause

Test data did not reflect production data shape. The tests passed because they tested the code, not the data.

### Fix

Add production-data regression tests:
```python
def test_price_parsing():
    real_prices = ["₹89,999", "₹1,299.50", "N/A", "Free"]
    expected = [89999.0, 1299.5, None, 0.0]
    for raw, expected in zip(real_prices, expected):
        assert parse_price(raw) == expected
```

### Lesson

> Tests that do not use production-like data test the code, not the system. Every automation should have tests that use real extracted data — including edge cases like missing fields, unusual formats, and error pages.


**Related Reading**
- Pattern Catalog: [Checkpoint/Resume](#), [Saga](#)
- Failure Playbook: [Pattern 12 — Job Overlap](#)
- Architecture Guide: [Decision 4 — Cron vs Scheduler](#)



- **Could this have been prevented?** YES → Production-data tests in [Design Review](automation-design-review.md) — test with real data shape

---

## STORY 17 — The 2FA That Was Enabled on a Holiday

### Situation

A client's IT department enabled two-factor authentication on their CRM as a security improvement. They did not notify the automation team.

### What We Thought

"Our session persistence means we never need to re-authenticate."

### What Happened

The session persisted for 23 hours after 2FA was enabled. The 24th hour, the session expired. The automation tried to re-login. The login page showed a 2FA challenge. The automation had no 2FA handler. It crashed.

The crash happened at 3 AM on a public holiday. No one checked the automation for 3 days.

### Root Cause

Session persistence masked the 2FA enablement for 23 hours. When the session finally expired, the automation had no graceful way to handle the new authentication requirement.

### Fix

Add authentication method detection:
```python
async def detect_auth_method(page) -> str:
    if await page.find("#totp-input"):
        return "TOTP"
    if await page.find("#sms-code"):
        return "SMS"
    return "password"
```

When an unexpected auth method is detected: capture screenshot, alert human, pause. Do not attempt to bypass.

### Lesson

> Session persistence hides authentication changes until the session expires. That is usually a good thing (you have 23 hours to fix it). But it also means you will discover the change at the worst possible moment — 3 AM on a holiday. Have a monitoring check that verifies authentication works at least once per shift.


**Related Reading**
- Failure Playbook: [Recovery Decision Tree](#)
- Architecture Guide: [Part V — Architecture Evolution](#)
- Pattern Catalog: [Supervisor](#)



- **Could this have been prevented?** YES → Auth method detection in [Failure Pattern 3](failure-playbook.md)

---

## STORY 18 — The Log File That Filled the Disk

### Situation

An automation logged every page interaction at DEBUG level. The logs were rotated weekly.

### What We Thought

"We have 50GB of disk space. Logs are tiny."

### What Happened

A malfunctioning CDP handler logged 10KB per page interaction. At 10,000 pages per day, that was 100MB of logs daily. Over 30 days, 3GB. Over 6 months, 18GB. Combined with the database (32GB), the 50GB disk filled up.

The automation failed because Chrome could not write its profile. The failure was logged. But the log could not be written because the disk was full. The error was invisible.

### Root Cause

No log size monitoring. No log rotation frequency review. The assumption that "logs are tiny" was never tested against actual data.

### Fix

```python
import logging.handlers
handler = logging.handlers.RotatingFileHandler(
    "automation.log", maxBytes=100*1024*1024, backupCount=5
)
```

### Lesson

> Logs grow unbounded until they fill the disk. Implement log rotation before deployment, not after the disk fills. Monitor log directory size alongside database size.


**Related Reading**
- Failure Playbook: [Recovery Decision Tree](#)
- Architecture Guide: [Part V — Architecture Evolution](#)
- Pattern Catalog: [Supervisor](#)



- **Could this have been prevented?** YES → Log rotation in [Design Review](automation-design-review.md) — monitor log directory size

---

## STORY 19 — The Race Condition That Only Happened at Midnight

### Situation

Two automations ran at midnight: one extracted daily sales data (00:00), another generated the daily report from that data (00:05).

### What We Thought

"Five minutes is enough time for the extraction to complete."

### What Happened

On most days, the extraction completed in 2 minutes. On the last day of the month, the extraction took 8 minutes because the supplier had 5x more data. The report generator ran at 00:05 with partial data. The monthly report was wrong.

The error was not discovered until the finance team reviewed the report at month-end close. The wrong numbers had been used for budgeting decisions for 3 weeks.

### Root Cause

The 5-minute gap was a guess that worked most of the time. It was not a contract enforced by the system. The report generator had no dependency check on whether the upstream extraction was complete.

### Fix

Add explicit dependency:
```python
extraction_complete = Path("/tmp/extraction_done.flag")
while not extraction_complete.exists():
    await asyncio.sleep(30)
generate_report()
```

### Lesson

> Time-based scheduling between dependent jobs is always a race condition. The only reliable dependency mechanism is a completion signal. If Job B depends on Job A, Job B should not start until Job A confirms completion — regardless of the time gap.


**Related Reading**
- Pattern Catalog: [Checkpoint/Resume](#), [Saga](#)
- Failure Playbook: [Pattern 12 — Job Overlap](#)
- Architecture Guide: [Decision 4 — Cron vs Scheduler](#)



- **Could this have been prevented?** YES → [Pattern 7 — Checkpoint/Resume](automation-pattern-catalog.md) — use completion signals, not time gaps

---

## STORY 20 — The Success That Was Actually a Failure

### Situation

A price monitoring automation ran for 18 months without incident. The client was happy. The team moved on to other projects.

### What We Thought

"Eighteen months of success means the automation is stable."

### What Happened

On day 545, the marketplace that the automation scraped changed their entire frontend architecture. Every selector broke. The automation extracted zero products. But the validation layer had never been tested with zero results — it accepted an empty list as valid.

The automation reported "[✓] Success — 0 records extracted." Monitoring showed green. The client's pricing team saw no competitor price changes for 3 weeks. They assumed competitors had not changed prices. They did not adjust their own pricing.

The client lost an estimated ₹5 lakh in margin over 3 weeks because they were underselling competitors whose prices had dropped.

### Root Cause

Success bias. The automation had been correct for so long that the team stopped questioning its output. Monitoring checked "did it run?" not "are the results reasonable?" Validation checked "is the format correct?" not "is the data plausible?"

### Fix

```python
# Statistical monitoring
avg_records = rolling_7_day_average("record_count")
today_records = get_today_count()
if today_records < avg_records * 0.5:
    send_alert(f"Record count dropped 50%: {today_records} vs {avg_records}")
```

### Lesson

> An automation that has never failed is not reliable — it is untested. Every silent period reduces vigilance. The most dangerous automation is the one that has worked perfectly for 18 months, because nobody remembers what failure looks like. Statistical monitoring catches what schema validation misses.


**Related Reading**
- Failure Playbook: [Recovery Decision Tree](#)
- Architecture Guide: [Part V — Architecture Evolution](#)
- Pattern Catalog: [Supervisor](#)



- **Could this have been prevented?** YES → Statistical monitoring in [Design Review](automation-design-review.md) — compare to 7-day rolling average

---

## Postmortem Pattern

Every story in this collection follows the same underlying pattern:

1. **Everyone assumed the system was working correctly.**
2. **The monitoring checked the wrong signal.**
3. **The failure was discovered by accident, not by alert.**
4. **The fix added a check that should have been there from day one.**

If your automation has never produced a "war story" for your team, it does not mean your automation is better. It means you have not looked closely enough. Add statistical monitoring. Add output validation. Question your assumptions. The war stories are coming — the only question is whether you learn from ours or create your own.

---

## Key Principles

1. **Every automation failure was predictable in hindsight.** The goal is to make it predictable before the failure, not after.

2. **Success bias is the most dangerous monitoring failure.** An automation that has never failed is not reliable — it is untested. The longer it has run without incident, the more vigilant you should be.

3. **Exit code 0 means nothing.** The only true measure of automation success is correct data in the database.

4. **Alert fatigue kills real incidents.** Design your alerting as if the on-call engineer has a family and needs to sleep.

5. **War stories are the most efficient teaching tool.** One story about a retry loop DDoSing a supplier teaches more than a chapter on backoff strategies.

> **"The most dangerous automation is the one that has never failed."**

> **"If you don't measure the outcome, you don't know if the automation is working."**
