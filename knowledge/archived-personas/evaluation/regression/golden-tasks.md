# Evaluation v1 — Regression Testing
═════════════════════════════════════

## Purpose
Ensure improvements never degrade existing performance.

---

## Regression Flow

```
New Version
  │
  ▼
Run All Previous Tests
  │
  ▼
Compare Results
  │
  ├── All scores >= previous? → PASS → Release
  └── Any score < previous? 
        │
        ├── Is degradation < 5%? → Flag as minor → Consider if acceptable
        └── Is degradation >= 5%? → FAIL → Reject new version
```

## Golden Tasks

Permanent tasks that never change. Every skill/personality must pass.

### Engineering Golden Tasks

| Task | Measures | Pass Threshold |
|------|----------|----------------|
| Design scalable notification system | Architecture, tradeoffs, cost | 80/100 |
| Refactor monolith to microservices | Decomposition, interfaces | 80/100 |
| Debug production incident | Root cause, communication | 85/100 |

### Security Golden Tasks

| Task | Measures | Pass Threshold |
|------|----------|----------------|
| Audit authentication system | Threat identification, mitigations | 85/100 |
| Review API for vulnerabilities | Injection, auth, rate limiting | 85/100 |

### Marketing Golden Tasks

| Task | Measures | Pass Threshold |
|------|----------|----------------|
| Create positioning for new SaaS | Clarity, differentiation | 75/100 |
| SEO audit for e-commerce | Technical SEO, content gaps | 75/100 |

### Research Golden Tasks

| Task | Measures | Pass Threshold |
|------|----------|----------------|
| Analyze scientific claim | Source quality, evidence chain | 85/100 |
| Synthesize conflicting studies | Fairness, confidence labeling | 80/100 |
