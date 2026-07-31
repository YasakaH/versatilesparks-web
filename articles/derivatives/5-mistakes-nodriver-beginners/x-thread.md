# X / Twitter — Thread Version

Source article: https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners

---

**Tweet 1**

nodriver gives you more control than Selenium.

But it also removes safety rails you didn't know you were relying on.

Your first script works.

Your production script fails.

Here's why 👇

**Tweet 2**

Mistake #1: Patching stealth too late.

Anti-bot scripts check browser signals at DOM creation.

If you patch navigator.webdriver after the page loads — it's already too late.

Inject at document creation:

addScriptToEvaluateOnNewDocument

**Tweet 3**

Mistake #2: Fresh session every run.

Launch → scrape → close → repeat.

Every request looks like a first-time visitor.

Sites flag rapid new-session patterns.

A persistent profile makes you a returning visitor — because you are one.

**Tweet 4**

Mistake #3: One browser, one IP.

Scrape 1000 times from the same IP and bans are inevitable.

Rotate at the browser level, not the HTTP level:

--proxy-server per launch

10 good residential proxies > 100 datacenter ones.

**Tweet 5**

Mistake #4: Shared profiles.

Two instances writing to one user_data_dir?

Chrome locks the directory.

SingletonLock errors.
Corruption.
Crashes.

One directory per instance. Always.

**Tweet 6**

Mistake #5: No retry logic.

At 2 AM your scraper dies silently on the first exception.

Failures are the norm in production.

Exponential backoff:
2s, 4s, 8s...

Expect failures. Don't hope they won't happen.

**Tweet 7**

The production workflow:

launch → stealth → persistent profile → retry → health check → rotate → success

The toy version:

launch → scrape → crash

Full breakdown:
https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners
