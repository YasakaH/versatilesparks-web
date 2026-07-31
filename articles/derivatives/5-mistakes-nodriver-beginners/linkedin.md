# LinkedIn — Engineering Lesson Post

Source article: https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners

---

A lesson from browser automation:

Switching from a high-level framework to a low-level one changes more than your code.

It changes the failure modes you're responsible for.

nodriver removes Selenium's abstraction layer.

You get direct CDP control — but you also lose the safety rails:

- no automatic session management
- no stealth patching
- no retry behavior
- no profile isolation

The same five mistakes show up in every team I see migrating:

1. Patching anti-detection signals after the page already loaded
2. Starting a brand-new session on every run
3. Scraping from a single IP
4. Sharing one browser profile across workers
5. No retry or recovery logic

Production automation isn't "open browser → scrape → close."

It's a workflow with state, health checks, and recovery.

The difference between a demo and production is rarely the first successful run.

It's whether it survives the 100th run.

I documented the five mistakes and their fixes here:
https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners
