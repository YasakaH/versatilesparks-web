# nodriver Production Checklist

One page. Distributes as: website page (future), GitHub `checklists/production-readiness.md`, Pinterest pin, lead-magnet for email capture.

---

Before deploying nodriver automation, run through this list:

## Profiles

- [ ] Persistent profile configured (`user_data_dir` set)
- [ ] One profile directory per instance (derived from task ID)
- [ ] Stale `SingletonLock` checked before launch

## Sessions

- [ ] Session validation added — verify login state *before* real work
- [ ] Re-authentication flow exists (tokens rotate, cookies expire)
- [ ] Persistent ≠ permanent — expiry is a normal event, not a surprise

## Retry & Health

- [ ] Exponential backoff on transient failures
- [ ] Browser health check before retrying
- [ ] Fail loudly on the last attempt (no swallowed errors)

## Detection

- [ ] Stealth patched at document creation (not after load)
- [ ] Proxy rotation configured where volume demands it

## Recovery

- [ ] Corruption handled: detect → backup → recreate → re-authenticate
- [ ] Graceful shutdown (`await browser.stop()`) instead of kill
- [ ] Worker monitors process exit codes

## Deployment

- [ ] Failure recovery tested at least once, not just written
- [ ] Stale profiles retired periodically (disk hygiene)

---

*Complete implementations, utilities, and Docker-ready templates: [Python Browser Automation Cookbook](https://gum.co/python-browser-automation-cookbook?ref=checklist)*
