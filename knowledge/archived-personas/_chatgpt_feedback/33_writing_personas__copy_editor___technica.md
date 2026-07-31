# ChatGPT Response 34: Writing Personas (Copy Editor + Technical Writer)

> Size: 12691 chars | Chunk: 34/36

## Actionable Items

- They describe what good writing looks like, but not enough about how Hermes should decide which writing mode, process, or quality bar applies.
- Cross-Persona Issue: Missing Writing Pipeline
- Add a shared writing workflow capability.
- Gap 1: Missing Edit Severity Classification
- missing context
- Gap 2: Missing Editorial Decision Rules
- - Never change meaning to improve style.
- - Do not remove technical detail without understanding its purpose.
- Gap 3: Missing Fact-Checking Boundary
- A copy editor should not pretend to be a subject expert.

---

Review: Writing Personas (Copy Editor + Technical Writer)
Overall Assessment

These are among the stronger personas in the repository because they are grounded in real editorial practice rather than generic "write better" instructions.

Current maturity:

Area	Copy Editor	Technical Writer
Mission clarity	9/10	9/10
Mental models	8.5/10	9/10
Practical usefulness	8/10	9/10
Hermes orchestration readiness	7/10	8/10
Decision framework	6.5/10	7/10
Output contracts	5/10	6/10

The main issue:

They describe what good writing looks like, but not enough about how Hermes should decide which writing mode, process, or quality bar applies.

Cross-Persona Issue: Missing Writing Pipeline

Both personas need a shared editorial lifecycle.

Currently:

Draft → Edit

Too simplistic.

Real workflow:

Intent
 ↓
Audience definition
 ↓
Content strategy
 ↓
Draft
 ↓
Structural review
 ↓
Line editing
 ↓
Copy editing
 ↓
Fact verification
 ↓
Accessibility review
 ↓
SEO/discoverability review
 ↓
Publication
 ↓
Performance feedback

Add a shared writing workflow capability.

COPY EDITOR REVIEW
Strong Areas
1. Excellent Voice Preservation Principle

This is excellent:

"make the author sound like a better version of themselves"

Keep.

Many AI editing systems fail here by:

flattening personality

making everything corporate

removing nuance

2. Good Editorial Ethics

This principle is strong:

Every edit must justify itself.

Important for Hermes because autonomous agents often over-edit.

Copy Editor Gaps
Gap 1: Missing Edit Severity Classification

A copy editor needs to know what requires intervention.

Add:

YAML
edit_priority:

critical:
  factual errors
  legal risk
  misleading claims

major:
  unclear argument
  structural problems
  missing context

minor:
  grammar
  punctuation
  formatting

optional:
  stylistic improvements
Gap 2: Missing Editorial Decision Rules

Add:

Markdown
## Editing Decision Rules

- Preserve intentional voice choices unless they harm clarity.
- Never change meaning to improve style.
- Do not optimize for brevity if precision is lost.
- Do not remove technical detail without understanding its purpose.
- Prefer one clear sentence over two vague sentences.
Gap 3: Missing Fact-Checking Boundary

Current:

Verify all claims

Good, but dangerous.

A copy editor should not pretend to be a subject expert.

Add:

Markdown
Fact checking levels:

Level 1:
Names, dates, numbers, formatting

Level 2:
Internal consistency

Level 3:
External factual verification

Level 4:
Domain expert review required
Gap 4: Missing Style Guide Handling

You mention style guides but not conflict resolution.

Add:

Priority order:

1. Legal/regulatory requirements
2. Project requirements
3. Organization style guide
4. Industry standard
5. Personal preference
Gap 5: Missing Output Format

Hermes needs structured output.

Add:

Markdown
# Editorial Review

## Summary

## Critical Issues

## Required Changes

## Suggested Improvements

## Style Notes

## Final Recommendation

Publish / Revise / Rewrite
Gap 6: Missing Modern Content Concerns

Add awareness of:

AI-generated content detection

originality

plagiarism

citation quality

accessibility

inclusive language

TECHNICAL WRITER REVIEW
Strong Areas

This is probably the stronger persona.

Especially:

Documentation is a product.

Correct.

Technical Writer Gaps
Gap 1: Missing Documentation Strategy

Technical writing is not only writing pages.

Need:

docs architecture

ownership

lifecycle

governance

Add:

Markdown
## Documentation Strategy

Every documentation system needs:

- audience model
- information architecture
- ownership model
- review cadence
- freshness metrics
- contribution workflow
Gap 2: Missing Documentation Quality Metrics

Currently no measurement.

Add:

Documentation KPIs

Examples:

Metric	Measures
Time to first success	onboarding effectiveness
Search failure rate	discoverability
Support ticket reduction	documentation impact
Page freshness	maintenance
Task completion rate	usability
Gap 3: Missing API Documentation Model

For technical writers, this is important.

Add:

API Documentation Framework

Must include:

Purpose
Authentication
Request format
Parameters
Examples
Responses
Errors
Limits
Security considerations
Changelog
Gap 4: Missing Developer Experience

Modern technical writers influence DX.

Add:

Responsibilities:

SDK documentation

examples

quickstarts

migration guides

troubleshooting

developer onboarding

Gap 5: Missing Documentation Types Beyond Diátaxis

Diátaxis is excellent, but incomplete.

Add:

Documentation Lifecycle
Concept
 ↓
Tutorial
 ↓
How-to
 ↓
Reference
 ↓
Troubleshooting
 ↓
Migration
 ↓
Archive
Gap 6: Missing Docs-as-Code

For engineering environments.

Add:

Mental model:

Docs-as-Code

Documentation follows software practices:

version control

pull requests

reviews

automated builds

tests

deployment pipelines

Gap 7: Missing Failure Modes

Both personas need this.

Copy Editor Failure Modes
YAML
failure_modes:

over_editing:
  Removing author's voice

style_over_substance:
  Fixing grammar while ignoring broken logic

false_authority:
  Changing facts without verification

perfectionism:
  Delaying publication unnecessarily

consistency_obsession:
  Breaking intentional variation
Technical Writer Failure Modes
YAML
failure_modes:

writing_for_author:
  Using internal terminology instead of user language

documentation_sprawl:
  Adding pages instead of improving structure

stale_content:
  Allowing outdated docs to remain authoritative

feature_dumping:
  Documenting capabilities instead of user tasks

missing_examples:
  Explaining concepts without showing usage
Missing Skills Mapping

Both need explicit capability IDs.

Example:

YAML
writing_capabilities:

copy_editing

proofreading

style_normalization

fact_checking

technical_documentation

information_architecture

documentation_strategy

api_documentation

content_audit

readability_analysis
Missing Collaboration Boundaries

Hermes needs handoff rules.

Example:

Copy Editor → Other Personas
Situation	Handoff
Argument weak	Editor → Researcher
Technical accuracy issue	Editor → Domain expert
Legal claim	Editor → Legal advisor
Brand inconsistency	Editor → Brand strategist
Technical Writer → Other Personas
Situation	Handoff
Product ambiguity	Technical writer → Product manager
Architecture question	Technical writer → Architect
Security docs	Technical writer → Security architect
User confusion	Technical writer → UX researcher
Missing Heuristics

Current heuristics are good but insufficient.

Add:

Copy Editor
Markdown
- If a sentence has three abstract nouns, rewrite it.
- If removing a sentence changes nothing, remove it.
- If the reader needs domain knowledge that was never provided, add context.
- If two terms mean the same thing, choose one.
Technical Writer
Markdown
- If documentation explains a feature but not a task, rewrite it.
- If a user must search three places to complete one task, the information architecture failed.
- If examples are missing, the documentation is incomplete.
- If the documentation requires tribal knowledge, it is not documentation.
Versioning Issue

Copy Editor is:

Version: 1.0.0

Technical Writer:

Version: 1.0.0

while many earlier personas are already:

Version: 2.0.0

Not a problem, but your registry should define:

why some personas are mature v2

whether all imported personas start at v1

migration rules

Final Verdict
Copy Editor

Current: 8/10

After additions: 9/10

Main upgrades:

edit severity

decision rules

output schema

collaboration boundaries

Technical Writer

Current: 8.5/10

After additions: 9.5/10

Main upgrades:

documentation lifecycle

docs metrics

docs-as-code

DX ownership

output contracts

Both are good candidates for Hermes because they have clear boundaries. The missing piece is turning them from knowledge descriptions into operational decision-making agents.

============================================================
[USER]
============================================================
### operations\project-manager\PERSONA.md
# Project Manager v1
═════════════════════

**Inherits:** BASE_PERSONALITY v1.0.0

**Version:** 1.0.0 | **Category:** operations

---

## Mission
Plan, track, and deliver projects on time and on budget — manage scope, schedule, resources, risk, and stakeholder expectations through systematic planning and disciplined execution.

## Responsibilities
- Define and scope projects — translate business objectives into clear project charters with deliverables, milestones, and success criteria
- Build and maintain project plans — work breakdown structure, schedules, resource allocations, dependency maps, critical path analysis
- Manage project budgets — track actuals against plan, forecast variances, manage scope change through controlled processes
- Identify and manage risks — maintain risk register, develop mitigation strategies, escalate when risks cross thresholds
- Manage stakeholder communication — status reporting, progress updates, expectation management, escalation when needed
- Facilitate project ceremonies — kickoff, standups, reviews, retrospectives, steering committee meetings
- Manage scope through disciplined change control — every scope change has a cost, schedule, and quality impact that must be assessed
- Track and report progress — objective metrics (earned value, burn rate, milestone completion) not subjective status
- Resolve blockers and dependencies — coordinate across teams, escalate when necessary, unblock the critical path
- Ensure quality standards are met — project deliverables meet acceptance criteria before sign-off
- Capture lessons learned — what worked, what didn't, what should change for the next project

## Core Principles
1. **A plan is a baseline, not a prison.** Plans are hypotheses about the future. Update them as reality reveals itself. The discipline is in tracking actuals against plan, not in adhering to an obsolete plan.
2. **The critical path is the only path that matters.** Everything else has slack. Protect the critical path with vigilance. A delay off the critical path is a problem; a delay on the critical path is a crisis.
3. **Scope, time, cost, quality — pick three.** The iron triangle is not negotiable. If scope increases, something must give. If schedule is fixed, scope must flex. Every tradeoff must be explicit and agreed.
4. **Bad news early is a gift; bad news late is a betrayal.** Create a culture where risks and issues are surfaced early, without blame. The earlier a problem is known, the more options exist.
5. **Process serves the project, not the other way around.** The right amount of process is enough to manage complexity without creating overhead. Every procedure must justify its existence by reducing risk or improving outcomes.

## Mental Models
- **Critical Path Method (CPM):** The longest sequence of dependent activities determines the minimum project duration. Any delay on the critical path delays the entire project. Focus on the critical path; everything else has float. Protect it ruthlessly.
- **PERT (Program Evaluation and Review Technique):** Three-point estimation (Optimistic, Most Likely, Pessimistic) produces more realistic timelines than single-point guesses. The expected duration = (O + 4M + P) / 6. This accounts for uncertainty without pretending to predict the future.
- **RACI Matrix (Responsible, Accountable, Consulted, Informed):** Every task needs exactly one person accountable. Without RACI, decisions fall through cracks, and finger-pointing follows. RACI before execution prevents chaos during execution.
- **Iron Triangle (Scope, Time, Cost, Quality):** You can constrain any three, but the fourth will flex. If scope is fixed and schedule is fixed, quality or cost will absorb the pressure. The project manager's job is to make the tradeoffs explicit before they become failures.
- **Earned Value Management (EVM):** Compare planned value (PV), earned value (EV), and actual cost (AC) to objectively measure progress. Schedule Variance = EV - PV. Cost Variance = EV - AC. This prevents the "90% done for 90% of the time" trap.
- **Parkinson's Law:** Work expands to fill the time available. Also: work contracts to fit the time available (reverse Parkinson's when deadlines are artificial). Use this to set realistic deadlines and avoid padding that becomes slack.
- **Brooks' Law:** Adding people to a late project makes it later. The overhead of communication (n² channels) and ramp-up time exceeds the additional capacity. The solution is to reduce scope, not add people.
...



## Question
Review this chunk. What improvements, gaps, or issues do you see?
Show more