# Chapter Review Specification

The Chapter Review is the final section before "Next Chapter." It contains three sub-components.

## 1. Chapter Summary

One paragraph. Lead with the engineering principle, not a list of APIs or recipes.

**Good:** "A browser environment is part of your application. Changing the environment changes the automation. The goal is predictability, not stealth."

**Bad:** "In this chapter, we learned about browser environments, fingerprints, profiles, timezone settings, and compatibility checks."

## 2. Production Checklist

Bullet list of concrete, verifiable items.

V1: 5-8 items
V2: 8-12 items

```markdown
## Production Checklist

Before moving on:
- [ ] Environment snapshot captured (ENVIRONMENT-SNAPSHOT)
- [ ] Retry taxonomy configured (RETRY-TAXONOMY)
- [ ] Structured logging enabled (LOGGING-SYSTEM)
```

Each checklist item should reference the relevant Stable ID in parentheses.

## 3. Chapter Connections

```markdown
## Chapter Connections

- **Depends on:** [Stable IDs of prerequisite recipes from earlier chapters]
- **Uses:** [common/*.py module paths]
- **Leads to:** [Chapter names that depend on this one]
```

### Examples

V1 connection:
```
Depends on: BROWSER-LAUNCH, TAB-MANAGEMENT
Uses: common/browser.py
Leads to: Chapter 3 (Reliability), Chapter 5 (Authentication)
```

V2 connection:
```
Depends on: BROWSER-LAUNCH, WAIT-STRATEGIES, RETRY-TAXONOMY
Uses: common/browser.py, common/config.py
Leads to: Chapter 11 (Complex Interaction), Chapter 12 (Production Systems)
```

## Order

```text
Chapter Summary
Production Checklist
Chapter Connections
Next Chapter
```
