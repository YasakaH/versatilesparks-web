# Quora — Answer Draft

Question: "Why does my web scraper keep getting blocked even though I use a headless browser?"

Note: Quora does not allow links in answers (policy). Answer is fully self-contained; no link.

---

One thing I learned building browser automation with nodriver:

Headless browsers don't hide automation signals by default.

Most blockers check the DOM at creation time:

- navigator.webdriver flag
- plugins and languages
- WebGL and canvas fingerprints

If your script launches, loads a page, and *then* tries to patch these signals — it's already too late. The anti-bot script ran before your patch did.

The fix is to inject the stealth patch before any page script executes (at document creation).

Two more things that commonly get people blocked:

1. A fresh browser session for every request — sites flag rapid new-session patterns, so reuse a persistent profile where possible.

2. A single IP making hundreds of requests — rotate proxies at the browser level, not per-HTTP-request.
