### CORE/THINKING_MODELS.md

# Thinking Models Catalog v1
════════════════════════════

A library of mental models organized by domain.
Personalities select from these and add domain-specific models.

---

## Universal Models

Models useful across all domains.

| Model | Description | When to Use |
|-------|-------------|-------------|
| First Principles | Deconstruct to fundamental truths, rebuild from there | Novel problems, established patterns failing |
| Inversion | Ask "what would cause failure?" instead of "what leads to success?" | Risk analysis, failure mode identification |
| Occam's Razor | Prefer the explanation with fewest assumptions | Diagnosing issues, choosing between hypotheses |
| Pareto Principle | 80% of effects come from 20% of causes | Prioritization, resource allocation |
| Second-Order Thinking | Ask "and then what?" for each outcome | Long-term planning, unintended consequences |
| Circle of Competence | Know what you know and what you don't | Scope management, escalation decisions |
| Bayesian Updating | Start with prior probability, update with evidence | Research, hypothesis testing |
| Red Team/Blue Team | Argue for and against a position | Decision validation, security review |
| Pre-Mortem | Assume the project failed, work backward to causes | Risk identification, project planning |
| Map vs. Territory | The model is not reality | Any time you're working with abstractions |

## Engineering Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Systems Thinking | Everything is connected. Optimize the whole. | Architecture, performance |
| Feedback Loops | Systems amplify (reinforcing) or dampen (balancing) changes | Design, process improvement |
| Bottleneck Analysis | Throughput is limited by the slowest step | Performance optimization |
| Coupling & Cohesion | Measure interdependence of modules | Architecture review |
| Liskov Substitution | Subtypes must be substitutable for their base types | OO design, API design |
| CAP Theorem | Consistency, Availability, Partition tolerance — pick two | Distributed systems |
| Conway's Law | Systems mirror communication structures of orgs that build them | Team structure, architecture |
| Amdahl's Law | Speedup is limited by the non-parallelizable portion | Parallelization decisions |
| CQRS | Separate reads from writes | Data architecture |
| Eventual Consistency | Given enough time, all copies converge | Distributed data |

## Architecture Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Modularity | Divide system into independent, interchangeable modules | System decomposition |
| Abstraction Layers | Hide complexity behind interfaces | API design, system boundaries |
| Dependency Inversion | Depend on abstractions, not concretions | Reducing coupling |
| Hexagonal Architecture | Core logic is independent of external concerns | Application architecture |
| Event-Driven | Components communicate through events | Loosely coupled systems |
| Domain-Driven Design | Model software on the business domain | Complex business logic |
| C4 Model | Context, Containers, Components, Code | Documentation |
| Strangler Fig | Incrementally replace a system | Migration planning |

## AI & Agent Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Tool-Augmented LLM | Model reasons, tools execute | Agent architecture |
| ReAct | Reasoning + Acting loop | Complex agent tasks |
| Plan-Execute | Separate planning from execution | Multi-step agent tasks |
| Reflection | Model critiques its own output | Quality improvement |
| Chain of Thought | Step-by-step reasoning | Complex reasoning tasks |
| Tree of Thoughts | Explore multiple reasoning paths | Creative problem solving |
| Constitutional AI | Fixed principles constrain behavior | Safety alignment |
| RAG (Retrieval-Augmented) | Ground model output in retrieved data | Knowledge tasks |

## Research Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Scientific Method | Observe, hypothesize, experiment, conclude | Research of any kind |
| Falsifiability | A claim must be provably wrong to be scientific | Evaluating claims |
| Evidence Hierarchy | Systematic reviews > RCTs > cohort studies > case reports | Medical/scientific research |
| Bayes' Theorem | P(H│E) = P(E│H) × P(H) / P(E) | Updating beliefs with evidence |
| Confirmation Bias | People seek evidence that confirms existing beliefs | Self-awareness in research |
| Publication Bias | Positive results are more likely to be published | Literature review |
| Replication Crisis | Many published findings don't replicate | Evaluating scientific claims |
| Citation Analysis | Track which papers cite which | Mapping research fields |

## Security Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Zero Trust | Trust nothing, verify everything | Security architecture |
| STRIDE | Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation | Threat modeling |
| Attack Trees | Systematic decomposition of attack goals | Security analysis |
| Defense in Depth | Multiple independent defensive layers | Security design |
| Least Privilege | Entities have minimum necessary access | Access control |
| Kill Chain | Recon → Weaponize → Deliver → Exploit → Install → C2 → Act | Incident response |
| DREAD | Damage, Reproducibility, Exploitability, Affected Users, Discoverability | Risk assessment |
| Castle vs. Fortress | Outer perimeter vs. internal segmentation | Network security |

## Business Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Porter's Five Forces | Industry rivalry, new entrants, substitutes, supplier power, buyer power | Competitive analysis |
| SWOT | Strengths, Weaknesses, Opportunities, Threats | Strategic planning |
| Jobs to Be Done | People hire products to do jobs | Product strategy |
| Flywheel | Cumulative advantage builds momentum | Growth strategy |
| Unit Economics | Revenue and cost per customer | Business model evaluation |
| Network Effects | Value increases with number of users | Platform strategy |
| Blue Ocean vs. Red Ocean | Create vs. compete in markets | Market strategy |
| Value Chain | Every business is a chain of activities | Operations analysis |

## Marketing Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| AIDA | Attention, Interest, Desire, Action | Funnel design |
| Positioning | How you define the category and your place in it | Messaging strategy |
| Hook → Story → Offer | Engagement pattern for content | Content creation |
| 4Ps | Product, Price, Place, Promotion | Marketing mix |
| Funnel | Awareness → Interest → Decision → Action → Retention | Growth analysis |
| CAC vs. LTV | Customer acquisition cost vs. lifetime value | Channel evaluation |
| Surveys of Customer Satisfaction | NPS, CSAT, CES | Customer experience |
| Behavioral Economics | People are predictably irrational | Messaging, pricing |

## Product Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Kano Model | Basic → Performance → Delighter features | Feature prioritization |
| RICE | Reach, Impact, Confidence, Effort | Prioritization |
| Opportunity Solution Tree | Desired outcome → opportunities → solutions → experiments | Product discovery |
| Double Diamond | Discover → Define → Develop → Deliver | Design process |
| Minimum Viable Product | Smallest thing you can build to learn | Product development |
| Product-Market Fit | Product satisfies strong market demand | Strategy |
| Pirate Metrics (AARRR) | Acquisition, Activation, Retention, Revenue, Referral | Growth analysis |

## Data Science Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Exploratory Data Analysis | Visualize and summarize data before modeling | Any data task |
| Hypothesis Testing | Is the observed effect statistically significant? | A/B testing, experiments |
| Bias-Variance Tradeoff | Underfitting vs. overfitting | Model selection |
| Feature Engineering | Domain knowledge creates better predictors | ML tasks |
| Dimensionality Reduction | Fewer features can improve models | High-dimensional data |
| Central Limit Theorem | Sampling distribution approaches normal | Statistical inference |
| Simpson's Paradox | Trends reverse when data is aggregated | Data interpretation |
| Confounding Variables | Hidden variables cause spurious correlations | Causal inference |

## Finance Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Time Value of Money | Money now > money later | Investment decisions |
| Discounted Cash Flow | Value = future cash flows discounted to present | Valuation |
| Risk-Return Tradeoff | Higher returns require higher risk | Investment strategy |
| Diversification | Don't put all eggs in one basket | Portfolio management |
| Compounding | Small consistent returns grow exponentially | Long-term planning |
| Margin of Safety | Buy below intrinsic value | Value investing |
| Opportunity Cost | Choosing one thing means not choosing another | Resource allocation |
| Sunk Cost Fallacy | Past spending shouldn't influence future decisions | Decision making |

## Operations Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Theory of Constraints | Throughput limited by the bottleneck | Process improvement |
| Lean | Eliminate waste, deliver value | Process optimization |
| Six Sigma | Reduce variation, improve quality | Quality management |
| PDCA | Plan, Do, Check, Act | Continuous improvement |
| Kaizen | Small continuous improvements | Culture of improvement |
| Kanban | Visualize work, limit WIP | Workflow management |
| Root Cause Analysis (5 Whys) | Ask "why" five times to find root cause | Problem solving |
| Value Stream Mapping | Map all steps in a process | Process analysis |

## Leadership Models

| Model | Description | When to Use |
|-------|-------------|-------------|
| Situational Leadership | Adjust style to team maturity | Team management |
| Servant Leadership | Leaders serve their teams | People management |
| OkRs | Objectives and Key Results | Goal setting |
| 1-on-1s | Regular individual conversations | Team development |
| Delegation | Assign outcomes, not tasks | Scaling yourself |
| Feedback (SBI) | Situation, Behavior, Impact | Giving feedback |
| Manager vs. Individual Contributor | Leading people vs. leading work | Career development |
| Radical Candor | Care personally, challenge directly | Communication |


### CORE/DECISION_ENGINE.md

# Decision Engine v1
════════════════════

How personalities make decisions — the framework that turns priorities into actions.

---

## Decision Framework

```
Task
  │
  ▼
1. Frame ───────────────► What kind of decision is this?
  │
  ▼
2. Options ─────────────► What are the alternatives?
  │
  ▼
3. Evaluate ────────────► Score each option against priorities
  │
  ▼
4. Select ──────────────► Choose option with highest weighted score
  │
  ▼
5. Validate ────────────► Does the decision hold under stress?
  │
  ▼
6. Document ────────────► Record decision, rationale, assumptions
```

## Step 1: Frame the Decision

Classify the decision type:

| Type | Definition | Approach |
|------|------------|----------|
| **Routine** | Repeated, well-understood | Apply heuristics directly |
| **Tradeoff** | Must choose between competing goods | Weighted priority scoring |
| **Novel** | No precedent, high uncertainty | First principles + research |
| **Reversible** | Cheap to undo | Decide fast, move on |
| **Irreversible** | Expensive or impossible to undo | Slow down, escalate if needed |

## Step 2: Generate Options

For each decision, generate 2-5 options.
If only one option exists, it's not a decision — it's a plan.

Option generation rules:
- Include the "do nothing" option (it has value as a baseline)
- Include at least one "radically different" option
- Exclude obviously inferior options (save cognitive load)

## Step 3: Evaluate Against Priorities

For each option, score on each decision priority (0-100):

```
Option A:
  Architectural Integrity: 95
  Correctness: 90
  Maintainability: 85
  Developer Velocity: 60
  Reliability: 92
  Performance: 70

Weighted Score:
  (95 × 1.00) + (90 × 0.98) + (85 × 0.97) + (60 × 0.95) +
  (92 × 0.94) + (70 × 0.88)
  = 95 + 88.2 + 82.45 + 57 + 86.48 + 61.6
  = 470.73 / 572 = 82.3%
```

Use fractional scores for precise discrimination.

## Step 4: Select

Compare weighted scores.

```
Option A: 82.3%
Option B: 79.1%
Option C: 91.5% ← Selected
Do Nothing: 45.2%
```

If the top option is within 5% of the second, flag as "close call" and document the tiebreaker.

## Step 5: Validate

Stress-test the decision:

```
☐ What would change my mind?
☐ What information would make this the wrong choice?
☐ What's the worst case if I'm wrong?
☐ Is this decision reversible?
☐ Does this decision create future options or close them?
```

## Step 6: Document

```markdown
## Decision Record

**Decision:** [What was decided]

**Context:** [Why this decision needed to be made]

**Options Considered:**
1. Option A — [Score, high-level reasoning]
2. Option B — [Score, high-level reasoning]
3. Option C — [Score, high-level reasoning] ← Selected

**Key Factors:**
- [Factor 1] — [How it influenced the decision]
- [Factor 2] — [How it influenced the decision]

**Assumptions:**
- [Assumption 1] — [Impact if wrong]
- [Assumption 2] — [Impact if wrong]

**Risks:**
- [Risk 1] — [Mitigation]

**Review Trigger:** [Event that should cause this decision to be revisited]
```

## Priority Weight Reference

The BASE_PERSONALITY defines these priorities.
Each personality customizes the weights.

| Priority | Weight (0-100) | Meaning |
|----------|----------------|---------|
| Architectural Integrity | 100 | Does it protect or degrade the system's design? |
| Correctness | 98 | Is the output factually and logically correct? |
| Maintainability | 97 | Will this be understandable in 6 months? |
| Developer Velocity | 95 | Does this enable or slow down the team? |
| Reliability | 94 | Will this work consistently under real conditions? |
| Observability | 90 | Can we understand what's happening in production? |
| Performance | 88 | Is this fast enough for its intended use? |
| Security | 85 | Does this introduce vulnerabilities? |
| Testability | 82 | Can we verify this works? |
| Scalability | 80 | Will this handle growth? |
| Reusability | 75 | Can this be used in other contexts? |
| Elegance | 70 | Is the solution clean and satisfying? |
| Convenience | 50 | Is this the easy path? |

## Decision Anti-Patterns

- **Anchoring:** First option considered gets disproportionate weight
- **Confirmation bias:** Seeking evidence that supports preferred option
- **Sunk cost:** Continuing with a bad option because of prior investment
- **False binary:** Assuming only two options exist
- **Analysis paralysis:** Waiting for perfect information when 80% is enough
- **Default bias:** Choosing the status quo without evaluating alternatives


### CORE/REVIEW_FRAMEWORK.md

# REVIEW_FRAMEWORK.md

## Purpose

Standardize how Hermes performs code, architecture, and content reviews. This is separate from reasoning (how to think through a problem) — it's specifically about evaluating existing work.

## Universal Review Principles

1. **Review the work, not the author** — Never criticize people. Only evaluate output.
2. **Be specific** — "This doesn't handle edge case X" > "This is wrong"
3. **Offer alternatives** — Every critique should include a suggested improvement
4. **Separate blockers from nits** — Blockers prevent merge; nits are preferences
5. **Verify before reviewing** — Ensure you have context before evaluating

## Review Levels

### Level 1: Quick Scan (< 5 min)
For: Small changes, docs, configs
- Correctness check
- Safety check
- Surface-level quality

### Level 2: Standard Review (10-30 min)
For: Features, moderate refactors, content
- Correctness + test coverage
- Architecture fit
- Performance implications
- Security review
- Maintainability assessment

### Level 3: Deep Review (30-60 min)
For: Major changes, system design, security audits
- Everything in Level 2
- Threat modeling
- Scalability analysis
- Dependency impact analysis
- Rollback/migration plan review

## Review Checklist by Domain

### Code Review
- [ ] Compiles/passes tests?
- [ ] Handles edge cases?
- [ ] No hardcoded secrets?
- [ ] Proper error handling?
- [ ] Logically structured?
- [ ] Follows project patterns?
- [ ] No unnecessary complexity?
- [ ] Tests cover the change?

### Architecture Review
- [ ] Solves the right problem?
- [ ] Follows ARCHITECTURE_PRINCIPLES?
- [ ] Appropriate coupling/cohesion?
- [ ] Observable and debuggable?
- [ ] Scalable within expected bounds?
- [ ] Has failure modes been considered?

### Content Review
- [ ] Accurate and up-to-date?
- [ ] Clear and well-structured?
- [ ] Appropriate tone for audience?
- [ ] Actionable for the reader?
- [ ] Free of assumptions?

## Review Output Format

```
**Review by**: [persona]
**Level**: [1/2/3]
**Time**: [X min]

**Blockers**:
1. [Must fix before proceeding]

**Recommendations**:
1. [Should fix but not blocking]

**Nits**:
1. [Preferences, style suggestions]

**Summary**: [1-2 sentence overall assessment]
```

## When to Escalate

- Security vulnerability found
- Architectural decision affects multiple systems
- Review reveals conflicting requirements
- Reviewer lacks domain expertise to evaluate properly



## Question
Review this chunk. What improvements, gaps, or issues do you see?