#!/usr/bin/env python3
"""
Verifiable Execution — Buyer Intelligence Engine
====================================================
Iteratively analyzes wedge candidates to answer:
1. What's the smallest product demonstrating verifiable execution in one industry?
2. Who owns the budget, and what are they already paying?
3. Why can we become the system of record?

Saves each iteration → buyer-intelligence-outputs/
Final consolidated file → one file with all iterations.
"""

import sys, os, datetime, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "buyer-intelligence-outputs")
os.makedirs(OUT_DIR, exist_ok=True)

STATUS_FILE = os.path.join(OUT_DIR, "buyer_status.json")

# ──────────────────────────────────────────────────────────────
# Wedge Candidates (from case database)
# ──────────────────────────────────────────────────────────────

WEDGES = [
    {
        "id": "healthcare_claims",
        "name": "Healthcare Claims Verification",
        "description": "Verify that every Medicare/insurance claim is backed by verifiable clinical evidence — not just EHR documentation.",
        "tagline": "Prove the care before you bill.",
        "pain": "$5.1B/year in improper Medicare payments. $6.5B DOJ fraud takedown. 34% medication error rate.",
        "target_buyer": "Hospital CFO / Compliance Officer / Revenue Cycle VP",
        "current_budget": "$2-12M/yr for compliance & audit IT (part of $50M+ hospital IT spend)",
        "current_vendor": "Epic (EHR), manual audit teams, DOJ data fusion center (government built own!)",
        "current_alternative": "Manual chart audits (20% of claims sampled), reactive DOJ enforcement, post-hoc analytics",
        "switching_cost": "HIGH — Epic lock-in, HIPAA compliance, clinician workflow disruption",
        "buying_trigger": "DOJ data mining finds pattern → ZPIC audit → repayment demand → scramble for evidence",
        "why_incumbents_wont": "Epic profits from ambiguity. Hospitals avoid evidence that creates liability. DOJ builds its OWN tools because vendors won't.",
        "smallest_product": "Post-claim verification API: submit claim ID → get back evidence score (was this claim supported by verifiable clinical actions?)",
    },
    {
        "id": "procurement_invoice",
        "name": "Procurement Invoice Verification",
        "description": "Verify that every invoice corresponds to a real, authorized transaction with a verified supplier.",
        "tagline": "Don't pay a fake invoice twice.",
        "pain": "$3B/year BEC fraud. 21,442 supplier fraud cases. $2.4M phantom supplier (4 years). 60-day detection lag.",
        "target_buyer": "AP Director / Procurement VP / CFO",
        "current_budget": "$500K-2M/yr for AP automation & fraud prevention",
        "current_vendor": "Coupa, SAP Ariba, manual AP teams, email-based verification",
        "current_alternative": "3-way match (PO/receipt/invoice), manual callbacks, post-hoc forensic audit, insurance claims",
        "switching_cost": "MEDIUM — Coupa/SAP lock-in, but verification layer sits beside ERP, doesn't replace it",
        "buying_trigger": "BEC wire fraud hits the company → VP of Finance demands change → AP tool budget approved within 30 days",
        "why_incumbents_wont": "Coupa/SAP profit from being the system of record. A neutral verification layer reduces their lock-in. They want to own the truth, not verify it.",
        "smallest_product": "Invoice verification API: submit invoice → verify supplier identity, check bank account against registry, score fraud risk, return confidence.",
    },
    {
        "id": "logistics_handoff",
        "name": "Logistics Handoff Verification",
        "description": "Verify every cargo handoff with biometric identity, geofence evidence, and immutable timestamp.",
        "tagline": "Prove it was delivered. Not just 'delivered' in the system.",
        "pain": "$725M cargo theft in 2025. $2.8M single fraudulent pickup. Chameleon carriers. 72hr detection lag.",
        "target_buyer": "Logistics Director / Supply Chain VP / Loss Prevention Manager",
        "current_budget": "$1-5M/yr for cargo insurance, loss prevention, tracking software",
        "current_vendor": "Project44, FourKites, Samsara, FMCSA database, paper BOLs",
        "current_alternative": "Paper BOL signed by driver. GPS tracking. FMCSA database lookup. Insurance claims. All reactive.",
        "switching_cost": "MEDIUM — carriers don't want this (reduces their plausible deniability). Shipper wants it but must convince/replace carriers.",
        "buying_trigger": "Major theft or fraudulent pickup → insurance rates spike → CFO demands proof-of-delivery system",
        "why_incumbents_wont": "Project44/FourKites aggregate carrier data — they can't verify it without alienating the carriers who supply it. Carriers profit from ambiguity.",
        "smallest_product": "Handoff verification API: driver biometric + GPS + timestamp + cargo photo → immutable evidence record returned to shipper instantly.",
    },
    {
        "id": "browser_automation",
        "name": "Browser Automation Verification",
        "description": "Prove that each automated browser action actually happened, with evidence of the page state before and after.",
        "tagline": "Your script says it worked. The page says otherwise.",
        "pain": "Browser-Use #5067 (crash recovery), #5048 (CDP disconnect), #5132 (callback never fires). All tools have these gaps.",
        "target_buyer": "Engineering Manager / Head of Automation / CTO (tool-adjacent)",
        "current_budget": "$500-5K/mo for browser automation infra (Playwright, Browserbase, Browserless)",
        "current_vendor": "Playwright, Puppeteer, Selenium, Browserbase, Browserless, BrowserStack",
        "current_alternative": "Screenshots before/after each action (build your own), manual verification, retry loops, timeouts",
        "switching_cost": "LOW — developer tools have low lock-in. Switch to nodriver-based SDK with evidence layer as a package install.",
        "buying_trigger": "Automation script fails silently in production → data goes missing → CTO discovers 3 days later → mandates verification",
        "why_incumbents_wont": "Playwright/Puppeteer are open-source. Browserbase sells infra, not verification. None have incentives to add anti-detection + evidence + crash recovery.",
        "smallest_product": "Python decorator: @verified — wraps any Playwright/nodriver action with before/after evidence capture, crash detection, auto-replay.",
    },
    {
        "id": "rpa_workflow",
        "name": "RPA Execution Verification",
        "description": "Prove that every RPA bot step executed correctly with evidence of each screen state and data transformation.",
        "tagline": "Your bot ran. Did it actually DO anything?",
        "pain": "45% of enterprises report WEEKLY RPA bot breakage. 40% of incidents are state-reset failures. Avg recovery: 4 hours.",
        "target_buyer": "Head of Automation / Center of Excellence Director / CIO",
        "current_budget": "$500K-5M/yr for RPA licenses + bot maintenance + human oversight",
        "current_vendor": "UiPath, Automation Anywhere, Blue Prism, Microsoft Power Automate",
        "current_alternative": "Manual bot monitoring, screen recording replay, UiPath's built-in logging (shows 'steps' but not evidence), chaos when bot breaks",
        "switching_cost": "MEDIUM — RPA platform lock-in is real, but verification layer is additive (SDK/integration), not a replacement",
        "buying_trigger": "Regulatory audit finds RPA bot processed 10K transactions with zero verifiable audit trail → compliance officer demands evidence layer",
        "why_incumbents_wont": "UiPath sells licenses. Adding real verification would expose how often bots fail. Their business model depends on hiding bot fragility behind 'success' metrics.",
        "smallest_product": "RPA audit plugin: sits beside UiPath/AA, captures screen state + data hash before/after each action, produces compliance-ready evidence report.",
    },
    {
        "id": "ai_agent",
        "name": "AI Agent Execution Verification",
        "description": "Prove what an AI agent actually did, how it reached its conclusion, and whether each action was intended.",
        "tagline": "Your AI agent 'solved the problem.' Did it, though?",
        "pain": "Prompt injection winning. Agent hallucination. No verifiable chain of thought. Benchmarks are 'theater.' 0 evidence of real-world actions.",
        "target_buyer": "Head of AI / CTO / Compliance Officer (enterprise deploying AI agents)",
        "current_budget": "$200K-2M/yr for AI agent infra + monitoring + human-in-the-loop oversight",
        "current_vendor": "LangChain, AutoGPT, CrewAI, browser-use, OpenAI Agents SDK, Anthropic Claude",
        "current_alternative": "Manual review of agent actions, prompt engineering, human-in-the-loop gating, custom logging (all unreliable)",
        "switching_cost": "LOW — agent frameworks are early, no dominant player, no lock-in yet",
        "buying_trigger": "AI agent makes unauthorized purchase, deletes production data, or violates compliance → executive order: 'every agent action must be verifiable'",
        "why_incumbents_wont": "OpenAI/Anthropic sell model usage, not execution verification. LangChain sells orchestration. None want to expose agent failure rates.",
        "smallest_product": "Agent action recorder: decorator/wrapper for any LLM tool call — captures prompt, response, tool output, state before/after, confidence score, human-readable audit trail.",
    },
    {
        "id": "enterprise_it",
        "name": "Enterprise IT Automation Verification",
        "description": "Prove that scheduled scripts, CI/CD pipelines, and infrastructure automation actually did what they were supposed to do.",
        "tagline": "Ansible says 'ok=10 changed=5.' What actually changed?",
        "pain": "No output artifact. Exit code = 0 but nothing happened. 18-month undetected cron failures. CI/CD deploys wrong version silently.",
        "target_buyer": "DevOps Director / Head of IT Operations / CISO",
        "current_budget": "$1-5M/yr for monitoring + observability (Datadog, Splunk, PagerDuty)",
        "current_vendor": "Datadog, Splunk, PagerDuty, Ansible AWX, Jenkins, GitHub Actions",
        "current_alternative": "Log aggregation, dashboard alerts, manual runbook verification, post-hoc log spelunking",
        "switching_cost": "MEDIUM — Datadog/Splunk are entrenched, but verification layer is additive OTel extension, not a rip-and-replace",
        "buying_trigger": "Critical deployment breaks silently → 6-hour outage → post-mortem finds automation reported success → CTO mandates execution verification on all pipelines",
        "why_incumbents_wont": "Datadog sells monitoring (metrics/logs/traces), not execution verification. They show you data; they don't tell you if it's correct. Adding verification would expose how much of their monitoring is noise.",
        "smallest_product": "CI/CD verification plugin: wraps each pipeline step with evidence capture (input hash, output hash, diff, exit code + context, confirmation of intended state).",
    },
]

# ──────────────────────────────────────────────────────────────
# Competitor Mapping
# ──────────────────────────────────────────────────────────────

COMPETITORS = [
    {"name": "Datadog", "desc": "Monitoring & observability (metrics, logs, traces)", "focus": "SHOWING data, not VERIFYING it", "threat_to_us": "LOW — they'd need to rebuild from first principles"},
    {"name": "Splunk", "desc": "Log aggregation & SIEM", "focus": "Post-hoc log analysis, not real-time verification", "threat_to_us": "LOW — reactive, not proactive"},
    {"name": "Microsoft (Power Automate)", "desc": "Low-code automation platform", "focus": "Building automations, not verifying them", "threat_to_us": "MEDIUM — could add, but incentives wrong"},
    {"name": "Epic Systems", "desc": "EHR market leader (85% hospitals)", "focus": "Being the system of record", "threat_to_us": "LOW — actively blocks interoperability"},
    {"name": "Coupa / SAP Ariba", "desc": "Procurement & AP", "focus": "Buyer-side system of record", "threat_to_us": "LOW — profit from asymmetry"},
    {"name": "UiPath / AA", "desc": "RPA platforms", "focus": "Selling bot licenses, not verifying them", "threat_to_us": "LOW — exposing bot failure hurts their model"},
    {"name": "OpenAI / Anthropic", "desc": "AI model providers", "focus": "Selling model usage", "threat_to_us": "LOW — verification would show hallucination rates"},
    {"name": "Project44 / FourKites", "desc": "Supply chain visibility", "focus": "Aggregating carrier data", "threat_to_us": "LOW — can't verify without alienating data sources"},
    {"name": "Browserbase / Browserless", "desc": "Headless browser infra", "focus": "Running browsers, not verifying actions", "threat_to_us": "LOW — verification would expose infra issues"},
    {"name": "Cloudflare", "desc": "Web infra & security", "focus": "Bot detection, not execution verification", "threat_to_us": "LOW — adjacent but different problem"},
]

# ──────────────────────────────────────────────────────────────
# Scoring Engine
# ──────────────────────────────────────────────────────────────

def score_wedge(w):
    """Score a wedge on 5 criteria. Each 0-100."""
    scores = {}
    rationale = {}
    
    # 1. Buyer clarity (does a specific person own this budget?)
    buyers = w.get("target_buyer", "").lower()
    if "/" in w.get("target_buyer", ""):
        scores["buyer_clarity"] = 70  # multiple possible buyers = unclear
        rationale["buyer_clarity"] = f"Multiple possible buyers ({w['target_buyer']})"
    elif "CFO" in buyers or "VP" in buyers or "Director" in buyers:
        scores["buyer_clarity"] = 90
        rationale["buyer_clarity"] = f"Clear buyer: {w['target_buyer']}"
    else:
        scores["buyer_clarity"] = 50
        rationale["buyer_clarity"] = f"Unclear buyer: {w['target_buyer']}"
    
    # 2. Budget availability (does money exist for this?)
    budget = w.get("current_budget", "").lower()
    if "$5M" in budget or "$10M" in budget:
        scores["budget"] = 90
    elif "$1M" in budget or "$2M" in budget:
        scores["budget"] = 80
    elif "$500" in budget:
        scores["budget"] = 60  # might be too small
    else:
        scores["budget"] = 50
    rationale["budget"] = f"Budget: {w['current_budget']}"
    
    # 3. Switching cost (can we get in without replacing existing systems?)
    sw = w.get("switching_cost", "").lower()
    if "low" in sw:
        scores["switching_cost"] = 90
        rationale["switching_cost"] = "Low switching cost — additive integration"
    elif "medium" in sw:
        scores["switching_cost"] = 60
        rationale["switching_cost"] = w.get("switching_cost", "")
    else:
        scores["switching_cost"] = 30
        rationale["switching_cost"] = w.get("switching_cost", "")
    
    # 4. Buying trigger (is there a clear event that forces purchase?)
    trigger = w.get("buying_trigger", "").lower()
    if "cf" in w.get("target_buyer", "").lower() or "audit" in trigger or "regulatory" in trigger:
        scores["buying_trigger"] = 85
        rationale["buying_trigger"] = "Fear-based trigger (regulatory/financial loss)"
    elif "insurance" in trigger or "theft" in trigger or "fraud" in trigger:
        scores["buying_trigger"] = 80
        rationale["buying_trigger"] = "Loss-based trigger (theft/fraud)"
    elif "production" in trigger or "outage" in trigger:
        scores["buying_trigger"] = 70
        rationale["buying_trigger"] = "Technical trigger (outage)"
    else:
        scores["buying_trigger"] = 50
        rationale["buying_trigger"] = "Weak trigger"
    
    # 5. Incumbent weakness (are current vendors structurally unable to compete?)
    incumbents = w.get("why_incumbents_wont", "").lower()
    if "profit from ambiguity" in incumbents or "profit from" in incumbents:
        scores["incumbent_weakness"] = 95
        rationale["incumbent_weakness"] = "Incumbents structurally profit from ambiguity"
    elif "expose" in incumbents or "alienat" in incumbents:
        scores["incumbent_weakness"] = 85
        rationale["incumbent_weakness"] = "Incumbents can't verify without hurting their model"
    elif "lock-in" in incumbents:
        scores["incumbent_weakness"] = 60
        rationale["incumbent_weakness"] = "Incumbents lock-in but could add verification"
    else:
        scores["incumbent_weakness"] = 40
        rationale["incumbent_weakness"] = "Incumbents could build this"
    
    total = sum(scores.values()) / 5.0
    return total, scores, rationale

# ──────────────────────────────────────────────────────────────
# Iteration Output
# ──────────────────────────────────────────────────────────────

def format_wedge_iteration(w, total_score, scores, rationale, depth, path_str):
    lines = []
    lines.append("=" * 65)
    lines.append(f"VERIFIABLE EXECUTION — BUYER INTELLIGENCE ITERATION")
    lines.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Path: {path_str}")
    lines.append(f"Depth: Level {depth}")
    lines.append("=" * 65)
    lines.append("")
    
    # Wedge overview
    lines.append(f"WEDGE: {w['id']} — {w['name']}")
    lines.append(f"  {w['description']}")
    lines.append(f"  Tagline: {w['tagline']}")
    lines.append(f"  Pain: {w['pain']}")
    lines.append("")
    
    # Scores
    lines.append("SCORES (0-100):")
    lines.append("-" * 40)
    for k, v in sorted(scores.items()):
        bar = "█" * (v // 10) + "░" * (10 - v // 10)
        lines.append(f"  {k:20s}: {v:3d} {bar}")
    lines.append(f"  {'OVERALL':20s}: {total_score:.0f}")
    lines.append("")
    lines.append("RATIONALES:")
    for k, r in rationale.items():
        lines.append(f"  {k}: {r}")
    lines.append("")
    
    # Buyer profile
    lines.append("BUYER PROFILE:")
    lines.append("-" * 40)
    lines.append(f"  Target buyer: {w['target_buyer']}")
    lines.append(f"  Budget: {w['current_budget']}")
    lines.append(f"  Current vendor: {w['current_vendor']}")
    lines.append(f"  Current alternative: {w['current_alternative']}")
    lines.append(f"  Switching cost: {w['switching_cost']}")
    lines.append(f"  Buying trigger: {w['buying_trigger']}")
    lines.append("")
    
    # Incumbent analysis
    lines.append("WHY INCUMBENTS WON'T BUILD THIS:")
    lines.append("-" * 40)
    lines.append(f"  {w['why_incumbents_wont']}")
    lines.append("")
    
    # Smallest product
    lines.append("SMALLEST PRODUCT:")
    lines.append("-" * 40)
    lines.append(f"  {w['smallest_product']}")
    lines.append("")
    
    # Deeper questions (next level)
    lines.append("NEXT LEVEL QUESTIONS:")
    lines.append("-" * 40)
    lines.append("  Q1: What is the exact annual budget line item for this problem?")
    lines.append("  Q2: What is the procurement process — who signs the PO?")
    lines.append("  Q3: How long from trigger to purchase decision?")
    lines.append("  Q4: What is the referenceable customer profile?")
    lines.append("  Q5: What is the competitive alternative the buyer explicitly chooses today?")
    
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────
# Deep dive — iterate on a wedge
# ──────────────────────────────────────────────────────────────

def deep_dive_wedge(w, depth=1, max_depth=10):
    """Iteratively go deeper on a wedge, saving each iteration."""
    files = []
    path_parts = [w['id']]
    
    for iteration in range(max_depth):
        d = depth + iteration
        path_str = " → ".join(path_parts)
        
        total_score, scores, rationale = score_wedge(w)
        
        content = format_wedge_iteration(w, total_score, scores, rationale, d, path_str)
        
        # Save
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"buyer_{w['id']}_L{d}_iter{iteration+1}_{ts}.txt"
        fp = os.path.join(OUT_DIR, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(fp)
        
        # Deeper: each iteration adds more depth to the buyer profile
        buyer_depth = [
            f"  Interview target: {w['target_buyer']} at companies with $500M+ revenue in regulated industries",
            f"  Budget holder: VP-level or C-suite; procurement cycle 30-90 days",
            f"  Current workaround cost: calculate fully-loaded cost of current alternative",
            f"  Reference customer profile: company that experienced {w['pain'][:60]}... in last 12 months",
            f"  Channel: direct sales for enterprise ($50K+ ACV), self-serve for mid-market ($5-15K ACV)",
            f"  Pricing model: per-action or per-workflow — aligned with value of evidence, not infrastructure cost",
            f"  Competitive response: incumbent ignores, builds limply, or acquires — we stay 2-3 years ahead",
            f"  Product evolution: wedge → adjacent wedge → horizontal verification layer",
            f"  Network effect: more verified actions → better baselines → smarter anomaly detection",
            f"  Moat: failure corpus + verification patterns + integrations into every automation surface",
        ]
        
        if iteration < len(buyer_depth):
            lines = content.split("\n")
            lines.append(f"")
            lines.append(f"BUYER DEPTH — Iteration {iteration+2}:")
            lines.append("-" * 40)
            lines.append(buyer_depth[iteration])
            content = "\n".join(lines)
            fp2 = os.path.join(OUT_DIR, fn.replace(".txt", "_v2.txt"))
            with open(fp2, "w", encoding="utf-8") as f:
                f.write(content)
            # Overwrite original
            with open(fp, "w", encoding="utf-8") as f:
                f.write(content)
        
        path_parts.append(f"L{d+1}")
    
    return files

# ──────────────────────────────────────────────────────────────
# Competitor deep dive
# ──────────────────────────────────────────────────────────────

def competitor_iteration(comp, depth=1):
    lines = []
    lines.append("=" * 65)
    lines.append(f"COMPETITOR ANALYSIS — {comp['name']}")
    lines.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 65)
    lines.append("")
    lines.append(f"  What they do: {comp['desc']}")
    lines.append(f"  Their focus: {comp['focus']}")
    lines.append(f"  Threat to us: {comp['threat_to_us']}")
    lines.append("")
    
    # Why they won't build verification
    lines.append("WHY THEY WON'T BUILD VERIFIABLE EXECUTION:")
    lines.append("-" * 40)
    
    reasons = {
        "Datadog": "They sell monitoring — metrics, logs, traces. Verification is a DIFFERENT PRODUCT category. It requires asserting truth, not just displaying data. Their entire architecture is built around passive observation, not active verification. Rewriting for verification would be a rebuild, not a feature.",
        "Splunk": "Splunk is a log search engine. It's reactive (look up what happened). Verification is proactive (confirm it happened correctly). Splunk's query model can't express 'did this action have the intended effect?'",
        "Microsoft (Power Automate)": "Microsoft sells licenses, not reliability. Power Automate is designed to be EASY, not VERIFIABLE. Adding real evidence would surface how often flows fail — which kills adoption. The incentive is to hide failure behind 'success' metrics.",
        "Epic Systems": "Epic IS the problem. Their business model depends on being the sole source of truth for hospital data. A neutral verification layer would allow patients, insurers, and regulators to verify clinical data without going through Epic. They will actively block this — as shown by their lawsuits against interoperability vendors.",
        "Coupa / SAP Ariba": "Coupa sells to BUYERS. It's designed to optimize procurement for the buyer, not to create neutral truth between buyer and supplier. A verification layer would let suppliers dispute rejected invoices — reducing buyer leverage. Coupa will never build this.",
        "UiPath / AA": "RPA vendors sell licenses based on 'bots deployed.' They have zero incentive to expose bot failure rates. Real verification would show 45% of enterprises have weekly breakage — kills their narrative. Their logging shows 'steps executed,' not 'steps that had the intended effect.'",
        "OpenAI / Anthropic": "They sell model tokens. Verification of agent actions would expose hallucination rates, tool-calling failures, and prompt injection. Every verified failure is a reason not to use their model. They will not build this.",
        "Project44 / FourKites": "They aggregate data from carriers. Carriers provide the data. If they added verification that exposed carrier failures, carriers would stop sharing data. Their entire business depends on carriers' willingness to participate. They can't verify without destroying their supply.",
        "Browserbase / Browserless": "They sell browser infrastructure (running Chrome in the cloud). Adding verification would expose connection drops, crash rates, and CDP instability. Their customers would demand SLA credits. Better to keep the noise hidden.",
        "Cloudflare": "Cloudflare detects bots. They're on the OPPOSITE side — they help websites block automation. Building a verification layer for automation would be directly counter to their bot-fighting business. They won't help the people they're blocking.",
    }
    lines.append(f"  {reasons.get(comp['name'], 'Structural disincentive against verification.')}")
    
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────
# Consolidation
# ──────────────────────────────────────────────────────────────

def consolidate(files, wedges, comps):
    """Consolidate all iteration files into one master document."""
    lines = []
    lines.append("=" * 70)
    lines.append("VERIFIABLE EXECUTION — CONSOLIDATED BUYER INTELLIGENCE")
    lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Wedges analyzed: {len(wedges)}")
    lines.append(f"Competitors mapped: {len(comps)}")
    lines.append(f"Iteration files: {len(files)}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("")
    
    # Wedge rankings
    scored_wedges = []
    for w in wedges:
        s, _, _ = score_wedge(w)
        scored_wedges.append((s, w))
    scored_wedges.sort(key=lambda x: -x[0])
    
    lines.append("WEDGE RANKINGS (by buyer intelligence score):")
    lines.append("-" * 50)
    for i, (s, w) in enumerate(scored_wedges, 1):
        lines.append(f"  {i}. {w['id']:30s} {s:.0f}/100 — {w['name']}")
    lines.append("")
    
    lines.append("WEDGE ANALYSIS:")
    lines.append("=" * 70)
    lines.append("")
    for s, w in scored_wedges:
        lines.append("-" * 50)
        lines.append(f"{w['id'].upper()}: {w['name']} (Score: {s:.0f}/100)")
        lines.append("-" * 50)
        lines.append(f"  Description: {w['description']}")
        lines.append(f"  Target buyer: {w['target_buyer']}")
        lines.append(f"  Budget: {w['current_budget']}")
        lines.append(f"  Current vendor: {w['current_vendor']}")
        lines.append(f"  Switching cost: {w['switching_cost']}")
        lines.append(f"  Buying trigger: {w['buying_trigger']}")
        lines.append(f"  Smallest product: {w['smallest_product']}")
        lines.append(f"  Why incumbents won't: {w['why_incumbents_wont']}")
        lines.append("")
    
    lines.append("=" * 70)
    lines.append("COMPETITOR ANALYSIS: WHY VENDORS WON'T BUILD THIS")
    lines.append("=" * 70)
    lines.append("")
    for comp in COMPETITORS:
        lines.append(competitor_iteration(comp))
        lines.append("")
    
    # All iteration files
    lines.append("=" * 70)
    lines.append(f"ALL ITERATION FILES ({len(files)} total)")
    lines.append("=" * 70)
    lines.append("")
    
    for fp in files:
        fn = os.path.basename(fp)
        lines.append(f"  • {fn}")
    
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("VERIFIABLE EXECUTION — BUYER INTELLIGENCE ENGINE")
    print(f"Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Wedges: {len(WEDGES)} | Deep dive iterations per wedge: 10")
    print("=" * 65)
    print()
    
    all_files = []
    status = {}
    
    for idx, w in enumerate(WEDGES, 1):
        print(f"[{idx}/{len(WEDGES)}] {w['id']} — {w['name']}...")
        
        # Run competitor analysis for relevant competitors
        comp_files = []
        for comp in COMPETITORS:
            comp_content = competitor_iteration(comp)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = comp['name'].lower().replace(" ", "_").replace("/", "_")
            cf = os.path.join(OUT_DIR, f"competitor_{safe_name}_{ts}.txt")
            with open(cf, "w", encoding="utf-8") as f:
                f.write(comp_content)
            comp_files.append(cf)
            all_files.append(cf)
        
        # Deep dive the wedge
        wedge_files = deep_dive_wedge(w, max_depth=10)
        all_files.extend(wedge_files)
        
        # Save wedge score summary
        total_score, scores, rationale = score_wedge(w)
        status[w['id']] = {
            "score": total_score,
            "files": len(wedge_files),
            "status": "completed",
        }
        print(f"  → {len(wedge_files)} iterations, score: {total_score:.0f}/100")
    
    # Save status
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)
    
    # Save consolidated file
    consolidated_content = consolidate(all_files, WEDGES, COMPETITORS)
    cons_path = os.path.join(OUT_DIR, "consolidated text file.txt")
    with open(cons_path, "w", encoding="utf-8") as f:
        f.write(consolidated_content)
    
    # Summary
    print()
    print("=" * 65)
    print("BUYER INTELLIGENCE COMPLETE")
    print("=" * 65)
    print()
    print(f"Total files: {len(all_files)}")
    print(f"Consolidated: {cons_path}")
    print(f"Size: {os.path.getsize(cons_path) / 1024:.0f} KB")
    print()
    
    # Rankings
    print("WEDGE RANKINGS:")
    scored = [(s, w) for s, w in [(score_wedge(w)[0], w) for w in WEDGES]]
    scored.sort(key=lambda x: -x[0])
    for i, (s, w) in enumerate(scored, 1):
        print(f"  {i}. {w['id']:30s} {s:.0f}/100 — {w['name']}")
    
    print()
    print(f"Output: {OUT_DIR}")

if __name__ == "__main__":
    main()
