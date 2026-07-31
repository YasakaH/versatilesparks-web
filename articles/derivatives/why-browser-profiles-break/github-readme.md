# GitHub — Repo README Draft

Target repo: `YasakaH/nodriver-production-patterns` (or `python-browser-automation`)

Note: repo does not exist yet. Do not create until user approves repo name and visibility.

---

# nodriver Production Patterns

A collection of patterns for building reliable Python browser automation with [nodriver](https://github.com/ultrafunkamsterdam/nodriver).

Covers:

- ✓ persistent browser profiles
- ✓ session validation
- ✓ retry strategies
- ✓ browser recovery
- ✓ profile isolation

## Structure

```
patterns/
├── retry-with-backoff.md
├── browser-profile-management.md
├── session-health-check.md
├── selector-strategy.md

examples/
├── login/
├── downloads/
├── sessions/

checklists/
└── production-readiness.md
```

## Getting started

```python
import nodriver

browser = await nodriver.start(user_data_dir="./profiles/job-1")
```

## License

MIT

## Related

The complete production implementation is available in:

Python Browser Automation Cookbook
https://gum.co/python-browser-automation-cookbook
