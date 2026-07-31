# X / Twitter — Pain Observation Post

Source article: https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners

---

Your first nodriver script worked perfectly.

Your second one failed.

By production, you had:

- timeouts
- CAPTCHAs
- profile locks
- random crashes

None of these are nodriver bugs.

They're mistakes from treating nodriver like Selenium.

It's not a wrapper.

It's a CDP client.

5 mistakes new users make:

1. No stealth patching
2. Fresh session every run
3. One IP, no rotation
4. Shared profiles
5. No retry logic

The fix for each:
https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners
