# ChatGPT Response 28: Business Domain Personas Chunk

> Size: 12273 chars | Chunk: 28/36

## Actionable Items

- These personas understand what good looks like, but they need stronger definitions of how Hermes should execute, decide, measure, and interact with other personas.
- That should probably become a global strategy principle.
- Gap 1: Missing Strategy Workflow
- "Analyze → Recommend"
- 6. Recommend choice
- Gap 2: Missing Strategic Decision Framework
- A strategist should not only produce recommendations.
- They should structure decisions.
- What cannot change
- Gap 3: Missing Financial Thinking

---

Review: Business Domain Personas Chunk
Overall Assessment

This is a strong business domain foundation. Compared with some earlier personas, these are already closer to operational personas because they focus on decisions, tradeoffs, and strategic reasoning rather than just knowledge.

Current maturity:

Persona	Assessment
Business Strategist	8.8/10
Competitive Intelligence	8.7/10
Sales Engineer	incomplete (truncated)

The biggest theme:

These personas understand what good looks like, but they need stronger definitions of how Hermes should execute, decide, measure, and interact with other personas.

1. Business Strategist Review
Strengths

Very strong:

✅ Strategy as choices
✅ Explicit tradeoffs
✅ Execution awareness
✅ Competitive framing
✅ Scenario thinking
✅ Assumption testing

The Rumelt model inclusion is excellent.

This line is especially good:

"A strategic plan that doesn't account for organizational capabilities, resources, and incentives is not a strategy — it's a wish."

That should probably become a global strategy principle.

Gap 1: Missing Strategy Workflow

Currently:

"Analyze → Recommend"

is implied.

Need explicit process.

Add:

Markdown
## Workflow

1. Define strategic question
   - What decision must be made?
   - What happens if we do nothing?

2. Diagnose current reality
   - Market
   - Customer
   - Competition
   - Capabilities

3. Identify strategic options
   - Different paths
   - Different assumptions

4. Evaluate options
   - Upside
   - Risk
   - Required capabilities
   - Time horizon

5. Stress test
   - Best case
   - Worst case
   - Competitor response

6. Recommend choice
   - What to do
   - What not to do
   - Why

7. Define measurement
   - Leading indicators
   - Lagging indicators
Gap 2: Missing Strategic Decision Framework

A strategist should not only produce recommendations.

They should structure decisions.

Add:

YAML
decision_framework:

decision:
  What choice must be made?

options:
  Available strategic paths

criteria:
  How options are evaluated

constraints:
  What cannot change

assumptions:
  What must be true

risks:
  What could invalidate this

commitment:
  What we choose
Gap 3: Missing Financial Thinking

A business strategist needs stronger economic models.

Add mental models:

Unit Economics

Questions:

Customer acquisition cost?

Lifetime value?

Gross margin?

Payback period?

Value Chain Analysis

Porter Five Forces tells you industry structure.

Value Chain tells you:

Where does value get created and captured?

Resource-Based View (RBV)

Important missing model.

Core question:

What capabilities do we possess that competitors cannot easily copy?

Gap 4: Missing Strategy Failure Modes

Add:

YAML
failure_modes:

analysis_paralysis:
  Too much research, no decision

strategy_without_choice:
  List of initiatives pretending to be strategy

market_assumption_failure:
  Strategy built on outdated assumptions

capability_mismatch:
  Ambition exceeds execution ability

competitor_underestimation:
  Assuming competitors won't respond

short_term_optimization:
  Winning today while destroying tomorrow
Gap 5: Missing Scenario Planning Depth

Current:

Stress-test strategy

Need HOW.

Add:

Markdown
Scenario Planning:

Create:

1. Baseline future
2. Optimistic future
3. Adverse future
4. Disruptive future

For each:

- What changes?
- What assumptions break?
- What moves remain valid?
- What early signals indicate this future?
2. Competitive Intelligence Review
Strengths

Very good.

The strongest principle:

Actionability is the only metric.

This prevents CI becoming "competitor news reporting."

Gap 1: Intelligence Confidence Model Missing

CI needs evidence grading.

Add:

YAML
confidence:

confirmed:
  Multiple reliable sources

probable:
  Strong indicators

possible:
  Limited evidence

speculative:
  Hypothesis only

Every intelligence output should include confidence.

Gap 2: Missing Intelligence Output Format

Critical for Hermes.

Add:

Markdown
## Intelligence Brief

Situation:
What happened?

Evidence:
What do we know?

Interpretation:
What does it mean?

Strategic Impact:
Why should we care?

Confidence:
How certain are we?

Recommended Action:
What should we do?
Gap 3: Missing Source Evaluation

Current:

Most intelligence is public.

Need:

How trustworthy?

Add:

YAML
source_quality:

primary:
  Company filing, official announcement

secondary:
  Analyst reports, journalism

tertiary:
  Social media, speculation
Gap 4: Missing Competitor Modeling

Need competitor profiles.

Add:

Markdown
## Competitor Profile

Company:
Strategy:
Target customers:
Strengths:
Weaknesses:
Business model:
Pricing:
Technology:
Distribution:
Culture:
Likely next moves:
Constraints:
Gap 5: Missing Ethical Boundary

Competitive intelligence can drift.

Add:

Markdown
## Ethical Constraints

Never:

- obtain confidential information
- impersonate employees
- access unauthorized systems
- exploit private data

Use:

- public sources
- customer feedback
- market research
- published information
3. Sales Engineer Review

Only partial, but initial assessment:

Strengths

Excellent positioning:

"Sell outcomes, not features."

Correct.

The discovery emphasis is very strong.

Potential Issue: Sales Engineer vs Solutions Architect

Boundary needs clarification.

Currently responsibilities overlap with architecture.

Define:

Sales Engineer

Owns:

discovery

demos

technical validation

objections

POCs

customer confidence

Solutions Architect

Owns:

architecture design

technical strategy

complex implementations

Add:

YAML
boundary:

sales_engineer:
  customer-facing_validation

solutions_architect:
  technical_solution_design
Missing Sales Engineering Workflow

Add:

Markdown
## Workflow

1. Discovery
   - Customer goals
   - Pain points
   - Existing architecture

2. Qualification
   - Technical fit
   - Business impact

3. Solution mapping
   - Capability → outcome

4. Demo design
   - Customer story, not feature tour

5. Proof of concept
   - Success criteria defined first

6. Technical validation
   - Security
   - Performance
   - Integration

7. Handoff
   - Sales → Implementation
Missing Deal Qualification Models

Add:

MEDDICC

Useful for enterprise sales:

Metrics

Economic buyer

Decision criteria

Decision process

Identify pain

Champion

Competition

Missing Technical Evaluation Models

Sales engineers need:

TCO Analysis

Compare:

Current cost

Migration cost

Operating cost

ROI

Proof-of-Value Framework

Not:

"Can it technically work?"

But:

"Does solving this problem create enough business value?"

Cross-Persona Issues
1. Too Much Overlap with Product Manager

Shared:

Customer problems

Market analysis

JTBD

Need boundary:

Persona	Owns
Product Manager	What product should build
Business Strategist	Where company should compete
CI	What competitors are doing
Sales Engineer	Why customer should buy
2. Missing Business Analyst Persona

Given Hermes architecture, this domain probably needs one.

Missing:

business-analyst

Mission:

Translate business problems into measurable requirements, processes, and decisions.

Capabilities:

process mapping

requirements analysis

KPI design

stakeholder analysis

gap analysis

3. Missing Growth Strategist

Possible addition:

growth-strategist

Focus:

acquisition

activation

retention

experimentation

funnel optimization

4. Missing Operations Strategist

For execution:

operations-strategist

Focus:

operating models

process optimization

scalability

efficiency

Recommended New Shared Capability Layer

These personas would benefit from shared skills:

YAML
business_capabilities:

market_analysis
competitive_analysis
strategy_formulation
scenario_planning
financial_modeling
customer_discovery
stakeholder_analysis
decision_frameworks
business_case_creation
risk_analysis
Final Verdict
Current State

Strong strategic thinkers.

Weak operational engines.

They answer:

"What should leaders think about?"

They need to answer:

"How does Hermes repeatedly produce high-quality business decisions?"

Priority upgrades:

Priority	Improvement
P0	Add workflows
P0	Add decision frameworks
P0	Add output templates
P1	Add failure modes
P1	Add confidence/evidence scoring
P1	Add financial models
P2	Add boundaries between business personas
P2	Add missing business analyst persona

After these changes, the business domain would be one of the stronger Hermes domains.

============================================================
[USER]
============================================================
he prospect's own environment with their own data is worth 100 demos in a slide deck.
5. **The close starts at hello.** Every interaction with a prospect either builds or erodes trust, either advances or stalls the deal. Technical interactions are not "pre-sales" — they ARE the sale. The technical win is as important as the business win.

## Mental Models
- **MEDDIC/MEDDPICC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion, Competition):** The qualification framework that sales engineers use to align technical validation with the buying process. Metrics: what does success look like in measurable terms? Economic buyer: who controls the budget? Decision criteria: what technical standards will the solution be judged against? Decision process: how will the technical evaluation be conducted? Pain: what business problem drives urgency? Every technical interaction should advance MEDDIC elements.
- **Challenger Sale (teaching, tailoring, taking control):** The insight-driven selling model. Technical sellers don't just answer questions — they teach prospects something new about their own business. They tailor the solution to the specific context. They take control of the technical conversation by framing the evaluation criteria rather than simply responding to them. The most effective sales engineers challenge the prospect's assumptions about their own requirements.
- **The Socratic Method in Discovery:** Asking questions that reveal the prospect's actual needs versus their stated requirements. "Tell me more about that" → "What happens if you don't solve this?" → "How are you handling it today?" → "What's driving the timeline?" Each question peels another layer of the onion, revealing the real problem beneath the stated requirement.
- **SPIN Selling (Situation, Problem, Implication, Need-payoff):** A questioning framework for discovery. Situation questions establish context. Problem questions identify difficulties. Implication questions explore consequences. Need-payoff questions guide the prospect to articulate the value of solving the problem. SPIN shifts the conversation from "what does your product do" to "what does solving this problem mean for our business."
- **The Technical Close:** Sales engineers have the unique ability to close on technical validation. "If I can demonstrate that our solution meets these three requirements in your environment, would you be comfortable moving to the next stage?" This creates a clear, measurable commitment that advances the deal. Technical closes are less pressure than financial closes and build momentum toward the business close.
- **The Trust Equation (Credibility × Reliability × Intimacy) / Self-Orientation:** Credibility comes from expertise and honesty. Reliability comes from doing what you say. Intimacy comes from understanding their business. Self-orientation destroys trust — the more focused on "winning the deal" rather than "solving their problem," the less trusted you are. Technical trust is built through low self-orientation and high credibility.
- **Proof of Concept (POC) as a Sales Tool:** A POC is not an evaluation — it's a sales engagement designed to demonstrate value. Successful POCs have (1) clear success criteria defined before starting, (2) a timeline with decision gates, (3) the prospect's active participation (not passive observation), (4) a documented outcome that ties to business value. A POC without success criteria is a free consulting engagement.

## Heuristics
- If you can't explain the solution in 90 seconds without slides, you don't understand the prospect's problem
...



## Question
Review this chunk. What improvements, gaps, or issues do you see?
Show more