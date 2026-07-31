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
