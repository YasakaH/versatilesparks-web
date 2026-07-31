# Reddit — Discussion Post (r/webscraping)

No CTA. No book link. Discussion-first.

---

I moved a scraping stack to nodriver for the low-level CDP control, and I'm seeing the same failure pattern over and over — including in my own early scripts:

- getting blocked on protected pages within minutes
- sites flagging rapid new-session patterns
- random profile lock errors
- silent crashes at 2 AM

What fixed most of it wasn't more selectors or wait logic.

It was:

- injecting stealth at document creation instead of after load
- reusing a persistent profile instead of a fresh one every run
- one user_data_dir per instance
- retry with backoff instead of fail-fast

Curious how others handle session persistence in long-running browser automation — do you keep profiles alive, or recreate them per job?
