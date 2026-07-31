# Thinking Models Library v1
═══════════════════════════

17 executable thinking frameworks for Hermes personalities.
Each framework includes: description, when to use, step-by-step method.

---

## 1. First Principles
**Deconstruct problems to fundamental truths, rebuild from there.**

*Use when:* Established patterns fail, you need genuine innovation, or assumptions haven't been questioned in years.

1. Identify current assumptions and beliefs about the problem
2. Deconstruct to fundamental truths — what is indisputably true?
3. Rebuild solution from those truths upward
4. Compare to conventional approach — reveal hidden assumptions

## 2. Systems Thinking
**Every problem exists in a system. Optimize the whole, not the part.**

*Use when:* Analyzing architecture, complex problems, or recurring issues.

1. Define system boundaries
2. Identify components and their relationships
3. Find feedback loops (reinforcing and balancing)
4. Identify leverage points — where small changes have big effects
5. Trace second and third-order effects of changes
6. Optimize the bottleneck, not everything equally

## 3. Bayesian Reasoning
**Start with a prior, update with evidence, state the posterior.**

*Use when:* Evaluating claims, making decisions under uncertainty, combining multiple evidence sources.

1. State prior probability (what do we believe before evidence?)
2. Consider likelihood of evidence under the hypothesis
3. Consider likelihood of evidence under alternative hypotheses
4. Update belief using Bayes' rule
5. State posterior probability and remaining uncertainty

## 4. Decision Trees
**Map decisions, outcomes, and probabilities for complex choices.**

*Use when:* Multi-step decisions with uncertainty, strategic planning.

1. List all decision points
2. For each decision, list possible actions
3. For each action, list possible outcomes with probabilities
4. Calculate expected value of each path
5. Choose path with highest expected value
6. Test sensitivity — would small probability changes change the decision?

## 5. Cost-Benefit Analysis
**Systematically compare costs and benefits of options.**

*Use when:* Resource allocation, technology choices, investment decisions.

1. List all options
2. For each option, list costs (time, money, complexity, opportunity)
3. For each option, list benefits (features, speed, maintainability)
4. Quantify where possible, describe where not
5. Compare net value
6. Consider non-quantifiable factors separately

## 6. Root Cause Analysis (5 Whys)
**Ask "why" repeatedly to find the actual root cause.**

*Use when:* Debugging failures, incident analysis, recurring problems.

1. State the symptom
2. Ask "why did this happen?" — get a cause
3. Ask "why does that cause exist?" — go deeper
4. Repeat until you reach a systemic cause (process, design, culture)
5. Fix the root cause, not the symptom

## 7. First/ Second/ Third-Order Effects
**Every action has consequences beyond the obvious.**

*Use when:* Architecture decisions, policy changes, any non-trivial decision.

1. State the action
2. First order: immediate, obvious effects
3. Second order: effects of those effects
4. Third order: effects of second order effects
5. Ask: "And then what?" until you've exhausted the chain

## 8. FMEA (Failure Mode & Effects Analysis)
**Proactively identify how things can fail and what happens.**

*Use when:* Safety-critical systems, new architectures, production changes.

1. List each component or step
2. For each, list all ways it could fail
3. For each failure, list effects
4. Rate Severity (1-10), Occurrence (1-10), Detection (1-10)
5. Calculate Risk Priority Number (S × O × D)
6. Address highest RPN items

## 9. Occam's Razor
**Prefer the explanation with the fewest assumptions.**

*Use when:* Diagnosing problems, choosing between hypotheses.

1. List all plausible explanations
2. Count assumptions required for each
3. Prefer the one with fewest assumptions
4. But remember: the simplest explanation is not always correct — just the best starting point

## 10. Hanlon's Razor
**Never attribute to malice what can be explained by incompetence.**

*Use when:* Interpreting others' actions, debugging team issues.

1. Before assuming bad intent, consider: could this be ignorance, error, or miscommunication?
2. If so, address the knowledge gap, not the perceived malice
3. Reserve malice attribution for cases where incompetence cannot explain it

## 11. Pareto Principle (80/20)
**80% of effects come from 20% of causes.**

*Use when:* Prioritization, optimization, resource allocation.

1. List all potential causes or inputs
2. Identify the 20% that produces 80% of the result
3. Focus effort there
4. Only address the remaining 80% if the top 20% is fully optimized

## 12. Game Theory
**Strategic decision-making when outcomes depend on others' choices.**

*Use when:* Competitive analysis, negotiations, multi-agent coordination.

1. Identify players and their options
2. Map payoffs for each combination of choices
3. Find Nash equilibria (stable outcomes where no player benefits from changing alone)
4. Identify dominant strategies (best regardless of what others do)
5. Use the analysis to inform your strategy

## 13. Queueing Theory
**Systems with arrival and service processes have predictable behavior.**

*Use when:* Performance analysis, capacity planning, process optimization.

1. Model arrival rate (λ) and service rate (μ)
2. Application of Little's Law: L = λW (queue length = arrival rate × wait time)
3. Utilization ρ = λ/μ (must be < 1 for stability)
4. As ρ approaches 1, queue length approaches infinity
5. Identify and reduce variability to improve performance

## 14. Lean Thinking
**Eliminate waste, deliver value continuously.**

*Use when:* Process improvement, workflow design, cost reduction.

1. Identify value from the customer's perspective
2. Map the value stream and identify waste
3. Make value flow without interruptions
4. Pull — produce only what the next step needs
5. Pursue perfection continuously

## 15. Cynefin Framework
**Classify problems to choose the right approach.**

*Use when:* Decision-making, problem classification, methodology selection.

1. **Clear** — cause and effect obvious. Apply best practices.
2. **Complicated** — cause and effect exist but require expertise. Analyze, then respond.
3. **Complex** — cause and effect only visible in retrospect. Probe, sense, respond.
4. **Chaotic** — no discernible cause and effect. Act, sense, respond.
5. **Disorder** — unclear which domain applies. Decompose to move into a known domain.

## 16. Wardley Mapping
**Map the value chain and evolution of components.**

*Use when:* Strategic planning, technology selection, identifying investment opportunities.

1. Identify the user need
2. Map the value chain (what's needed to meet that need)
3. For each component, assess evolution stage (Genesis → Custom → Product → Commodity)
4. Identify anchors (differentiators) and commodities (buy, don't build)
5. Develop strategy based on evolution position

## 17. Scientific Method
**Systematic observation, measurement, and experimentation.**

*Use when:* Any research or investigation where conclusions matter.

1. Observe and describe a phenomenon
2. Formulate a hypothesis (falsifiable)
3. Design experiment that can disprove the hypothesis
4. Run experiment and collect data
5. Analyze data — does it support or contradict the hypothesis?
6. If supporting: refine and expand. If contradicting: revise hypothesis.
7. Report results, methodology, and limitations
