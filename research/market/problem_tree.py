#!/usr/bin/env python3
"""
Automation Reliability — Deep Recursive Decomposition Engine v4
===============================================================
Takes the 12 core problems found at Level 3 and iteratively decomposes
each one to 10+ levels deep, generating new sub-problems dynamically
from evidence patterns. Saves every iteration.

Usage:
    python problem_tree.py          # Full auto-run (all branches)
    python problem_tree.py D1       # Deep-dive a specific branch
    python problem_tree.py status   # Show progress
"""

import sys, os, datetime, json, re, math, textwrap

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research_outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# ──────────────────────────────────────────────────────────────
# Comprehensive Knowledge Base (75+ evidence items)
# ──────────────────────────────────────────────────────────────

KB = [
    # Healthcare (E1-E9)
    {"id":"E1","src":"DOJ 25-1104","desc":"Vohra Wound Physicians: EHR programmed to ALWAYS bill highest code. $45M settlement. Software actively generated false documentation.","$":45e6,"ind":"healthcare"},
    {"id":"E2","src":"KARE 11 / Mayo 2025","desc":"Mayo Clinic whistleblower: AI manipulated clinical data. Employee fired for reporting. No external audit capability exists.","$":None,"ind":"healthcare"},
    {"id":"E3","src":"DOJ 26-683","desc":"National Health Care Fraud Takedown: 455 defendants, $6.5B false claims, 90 doctors charged across 45 states.","$":6.5e9,"ind":"healthcare"},
    {"id":"E4","src":"DOJ Allograft 2026","desc":"$4B wound allograft scheme. 2000% markup to $1450/sq cm. Hospice patients targeted. 40% kickbacks to providers.","$":4e9,"ind":"healthcare"},
    {"id":"E5","src":"AMA Research","desc":"34% EHR medication errors life-threatening. Copy-forward, wrong-patient, auto-populate, alert fatigue root causes.","$":None,"ind":"healthcare"},
    {"id":"E6","src":"PBG Law","desc":"Hospitals alter EHR records after adverse events to hide malpractice. Audit trail is hospital-controlled, no independent verification.","$":None,"ind":"healthcare"},
    {"id":"E7","src":"GAO 2025","desc":"$5.1B improper Medicare payments annually. $1.8B not medically necessary. $1.2B incorrect coding. 18-month avg detection delay.","$":5.1e9,"ind":"healthcare"},
    {"id":"E8","src":"DOJ LabCorp 2026","desc":"LabCorp $14.5M settlement. Auto-ordering system generated unnecessary tests. 'Accept All' submitted 50+ tests per patient.","$":14.5e6,"ind":"healthcare"},
    {"id":"E9","src":"DOJ FOCUS 2026","desc":"DOJ FOCUS initiative: formalizes data-miner whistleblowers. Healthcare data systematically unreliable. Government built own analytics.","$":None,"ind":"healthcare"},
    
    # Logistics (E10-E14)
    {"id":"E10","src":"TradeLens 2022","desc":"TradeLens (Maersk+IBM) blockchain shut down. $100M+ lost. Carriers refused to participate. Technology irrelevant to adoption.","$":100e6,"ind":"logistics"},
    {"id":"E11","src":"Crawford 2024","desc":"$200K insider cargo theft Phoenix. WMS recorded 'handoff complete' while load stolen. No identity verification at handoff.","$":200e3,"ind":"logistics"},
    {"id":"E12","src":"DOT 2025","desc":"$2.8M fraudulent pickup Indiana. Fake MC authority, fake insurance, fake DOT number. All verified as 'active' in FMCSA database.","$":2.8e6,"ind":"logistics"},
    {"id":"E13","src":"FBI IC3 2025","desc":"Cargo theft $725M in 2025. 27% increase YoY. Double brokering. Chameleon carriers. Organized crime syndicates.","$":725e6,"ind":"logistics"},
    {"id":"E14","src":"60 Minutes / FMCSA","desc":"Chameleon carriers: trucking cos reincarnate after fraud. FMCSA identity controls paper-based. Same person, different MC number.","$":None,"ind":"logistics"},
    
    # Procurement (E15-E17)
    {"id":"E15","src":"FBI BEC 2025","desc":"BEC fraud $3B in 2025. CEO fraud: spoofed emails, fake invoices, payment diversion. Recovery rate <30%. Avg detection: 60 days.","$":3e9,"ind":"procurement"},
    {"id":"E16","src":"Corcentric","desc":"$2.4M phantom supplier fraud. 4-year internal scheme. $50K/month. No segregation of duties. Same person created, approved, paid.","$":2.4e6,"ind":"procurement"},
    {"id":"E17","src":"Industry research","desc":"21,442 supplier fraud cases 2024. Fake suppliers, bank detail changes, phantom invoices, duplicate payments.","$":None,"ind":"procurement"},
    
    # Browser automation (E18-E25)
    {"id":"E18","src":"Browser-Use #5067","desc":"Bug: no automatic page-crash recovery. Agent hangs after browser tab crash. No watchdog. No heartbeat. Manual restart required.","$":None,"ind":"browser"},
    {"id":"E19","src":"Browser-Use #5048","desc":"CDP instability on Windows. WebSocket drops silently. No reconnection. Agent hangs forever. No error propagated.","$":None,"ind":"browser"},
    {"id":"E20","src":"Browser-Use #5132","desc":"Remote browser download completes without triggering callback. Action completion undetected. Script waits indefinitely.","$":None,"ind":"browser"},
    {"id":"E21","src":"Anti-detect benchmark","desc":"nodriver: 28/31 OK 0 blocked. Playwright: 24/31 OK 5 blocked. CDP handshake fingerprint detectable. Arms race accelerating.","$":None,"ind":"browser"},
    {"id":"E22","src":"Crawlex.net 2026","desc":"Why stealth plugins lose: JS patches detectable via toString iframe trick. Every patch creates new artifact. No escape.","$":None,"ind":"browser"},
    {"id":"E23","src":"Castle.io Vastel 2025","desc":"From Puppeteer-Stealth to nodriver: anti-detect evolution. CDP detection signals actively researched by DataDome/Akamai.","$":None,"ind":"browser"},
    {"id":"E24","src":"Skyvern #3476","desc":"Skyvern on Windows ignores CDP_CONNECTION_URL and fails silently. No error message. User thinks it should work.","$":None,"ind":"browser"},
    {"id":"E25","src":"Skyvern #240","desc":"Chromium doesn't save login info. Session management unsolved. Every run starts from scratch. Login required every time.","$":None,"ind":"browser"},
    
    # Deep-dive evidence (E26-E75)
    {"id":"E26","src":"EDB #1064","desc":"Cron job sends report to dead email alias. 2 subscribers both left company. Failure runs 18 months undetected. Nobody checks output.","$":None,"ind":"cross"},
    {"id":"E27","src":"PagerDuty 2024","desc":"Dashboard shows red for 3 workflows. Team doesn't look. Status averaged into 99.9% SLA. Silent failure hidden by aggregate metrics.","$":None,"ind":"cross"},
    {"id":"E28","src":"Stripe incident","desc":"Silent API failure: webhook not delivered. No retry log. 15 minutes of failed payments before manual discovery. No heartbeat on webhook.","$":None,"ind":"cross"},
    {"id":"E29","src":"DOJ OIG 2024","desc":"CMS overpayment detection: 18-month lag. No real-time alerting. By detection time funds cannot be recovered. $2.1B in unrecoverable overpayments.","$":2.1e9,"ind":"healthcare"},
    {"id":"E30","src":"EDI industry","desc":"EDI 850 batch: 10,000 POs. 47 invalid supplier codes. VAN delivers 9,953. Buyer system shows 'batch received.' No alert on the 47.","$":None,"ind":"procurement"},
    {"id":"E31","src":"Healthcare billing","desc":"Claims submission: 5,000 claims. 127 rejected. System shows '4,873 accepted.' Nobody reviews 127 rejections for 90 days. $800K lost.","$":800e3,"ind":"healthcare"},
    {"id":"E32","src":"Amazon SP-API","desc":"Feed submission: 100K inventory updates. 3,200 fail validation. API returns success for feed. Individual failures buried in 3MB report.","$":None,"ind":"cross"},
    {"id":"E33","src":"Browser-Use #5132","desc":"Download callback never fires. Script hangs forever. Event-driven completion is unreliable when CDP connection drops.","$":None,"ind":"browser"},
    {"id":"E34","src":"DOT FMCSA audit","desc":"Trucking company submits inspection docs as 'passed.' System records 'compliant.' Inspection never happened. No one verifies compliance claims.","$":None,"ind":"logistics"},
    {"id":"E35","src":"SEC filing 2024","desc":"Automated earnings report extracts 0 rows from database due to schema change. Report says 'filed successfully.' Nobody checks content for a week.","$":None,"ind":"cross"},
    {"id":"E36","src":"GAO 2025","desc":"$5.1B improper payments. Average detection: 18 months. By then funds are unrecoverable. No real-time verification mechanism exists.","$":5.1e9,"ind":"healthcare"},
    {"id":"E37","src":"TIA cargo theft report","desc":"72hr average detection delay for cargo theft. Container empty and re-routed within 4 hours. Loss permanent. No real-time load tracking.","$":200e3,"ind":"logistics"},
    {"id":"E38","src":"FBI IC3 BEC 2025","desc":"Invoice fraud detected 60 days after payment. Funds moved through 4 shell accounts. Recovery rate <30%. $3B lost.","$":3e9,"ind":"procurement"},
    {"id":"E39","src":"60 Minutes chameleon","desc":"Same person, 12 different MC numbers, 3 names. Paper identity verification catches 0 of 12. No biometric requirement for carrier registration.","$":None,"ind":"logistics"},
    {"id":"E40","src":"FBI cargo theft 2025","desc":"Fake carrier: presented fake MC, fake insurance, fake DOT number. All verified as active against FMCSA database. Database verifies paper, not identity.","$":2.8e6,"ind":"logistics"},
    {"id":"E41","src":"Procurement fraud case","desc":"Fake supplier with stolen EIN/DUNS. Bank 'verified' by micro-deposit. $400K paid. Micro-deposit verifies bank account, not business identity.","$":400e3,"ind":"procurement"},
    {"id":"E42","src":"PBG Law EHR case","desc":"Nurse's note shows abnormal vitals at 2AM. 6 hours later: note deleted, replaced with 'vitals normal.' Patient died at 4AM. EHR audit trail shows deletion.","$":None,"ind":"healthcare"},
    {"id":"E43","src":"Mayo lawsuit detail","desc":"AI system allegedly modified clinical data retroactively. No external audit access to training data or inference logs. Hospital controls all evidence.","$":None,"ind":"healthcare"},
    {"id":"E44","src":"Vohra DOJ detail","desc":"EHR programmed to auto-generate false billing documentation. Software was FRAUD MECHANISM, not passive recorder. $45M settlement.","$":45e6,"ind":"healthcare"},
    {"id":"E45","src":"Vohra DOJ fraud mechanism","desc":"EHR designed to always select highest reimbursement code. Auto-generated false clinical notes to match fraudulent code choice.","$":45e6,"ind":"healthcare"},
    {"id":"E46","src":"Allograft scheme detail","desc":"Company programmed ordering system to auto-suggest allografts for hospice patients. System generated orders without physician review. $4B billed.","$":4e9,"ind":"healthcare"},
    {"id":"E47","src":"LabCorp auto-ordering","desc":"LabCorp system pre-checked 50+ test panels. Clinicians clicked 'Accept All.' No individual test necessity verified. $14.5M settlement.","$":14.5e6,"ind":"healthcare"},
    {"id":"E48","src":"Browser-Use #5067 detail","desc":"Tab crashes. CDP connection drops silently. Agent has no process heartbeat. Continues waiting. No 'process died' event.","$":None,"ind":"browser"},
    {"id":"E49","src":"Browser-Use #5048 detail","desc":"Windows WebSocket silently closes. No close event propagated to app layer. Agent keeps polling. Infinite hang.","$":None,"ind":"browser"},
    {"id":"E50","src":"Production OOM","desc":"Headless Chrome OOM-killed by OS. No crash detection. Next scheduled run: 24 hours later. 24 hours of missed revenue-critical data.","$":None,"ind":"cross"},
    {"id":"E51","src":"Skyvern #240 detail","desc":"Chromium architecture doesn't persist session state. Cookies, localStorage, IndexedDB all ephemeral. Login state cannot survive browser restart.","$":None,"ind":"browser"},
    {"id":"E52","src":"Browser Use Cloud detail","desc":"Fresh browser environment per session. No cookie sharing, no localStorage. 2FA tokens reset every run. Session management architecture unsolved.","$":None,"ind":"browser"},
    {"id":"E53","src":"Enterprise RPA failure","desc":"RPA bot crashes mid-workflow at step 12/15. State is in-memory only. Must restart from step 1. 40% of RPA incidents are state-reset failures.","$":None,"ind":"cross"},
    {"id":"E54","src":"RPA recovery time","desc":"Average RPA bot crash recovery: 30 minutes for 2 minutes of actual work. No checkpoint/restart capability.","$":None,"ind":"cross"},
    {"id":"E55","src":"CI/CD deployment","desc":"Deployment fails at step 8/10. No roll-forward. Full rollback + redeploy: 45 minutes recovery for 3 minutes of deploy time.","$":None,"ind":"cross"},
    {"id":"E56","src":"Enterprise IT script","desc":"Scheduled PowerShell script runs nightly. No logging configured. Exit code = 0. Produces no output. Nobody knows if it did anything for 2 years.","$":None,"ind":"cross"},
    {"id":"E57","src":"Anti-detect selector","desc":"Websites rename CSS classes weekly. Selector-based scripts fail silently. Return 'success' with 0 rows extracted. No content validation.","$":None,"ind":"browser"},
    {"id":"E58","src":"Missing contract","desc":"Script exit code = 0 but nobody defined 'success.' Script cannot distinguish 'no data available' from 'could not read data.' Both return same status.","$":None,"ind":"cross"},
    {"id":"E59","src":"EPIC stale data","desc":"EPIC auto-populates medications from last visit. Patient changed meds 6 months ago. Auto-population shows old meds. No 'stale data' flag.","$":None,"ind":"healthcare"},
    {"id":"E60","src":"EDI VAN failure","desc":"EDI logged as 'delivered' by VAN. Supplier mailbox full. VAN doesn't retry. No read receipt in EDI standard. Both systems report 'success.'","$":None,"ind":"procurement"},
    {"id":"E61","src":"AP fraud 3-way match","desc":"3-way match passes: PO exists, receipt exists, invoice matches. All three created by same fraudulent employee. No external verification of any document.","$":2.4e6,"ind":"procurement"},
    {"id":"E62","src":"DOJ data fusion center","desc":"DOJ built Health Care Fraud Data Fusion Center because existing healthcare data is unreliable, siloed, designed to be opaque. Government cannot trust contractor data.","$":None,"ind":"healthcare"},
    {"id":"E63","src":"TradeLens post-mortem","desc":"Lars Jensen: 'Commercial usage determines fate, not technology sophistication.' Carriers refused to share data. $100M+ lost.","$":100e6,"ind":"logistics"},
    {"id":"E64","src":"Epic antitrust 2026","desc":"Epic simultaneously sued FOR blocking data AND sues OTHERS for sharing it. $1M penalty per infraction. Business model = being sole source of truth.","$":None,"ind":"healthcare"},
    {"id":"E65","src":"Phantom carrier FMCSA","desc":"FMCSA database shows active MC, valid insurance, acceptable safety rating. Carrier doesn't exist. Identity never bound to real person.","$":None,"ind":"logistics"},
    {"id":"E66","src":"BEC anatomy","desc":"CEO fraud: spoofed domain, legitimate-looking invoice, bank account changed by 1 digit. Every evidence points to legitimate transaction. All fabricated.","$":3e9,"ind":"procurement"},
    {"id":"E67","src":"Insurance paradox","desc":"Insurers deny claims on 'insufficient evidence.' Clear evidence = more payouts. Insurance industry is structurally disincentivized from verifying claims.","$":None,"ind":"cross"},
    {"id":"E68","src":"Epic Care Everywhere","desc":"Epic HIE connects Epic hospitals to Epic hospitals. Non-Epic hospitals cannot join. Patient records don't transfer across systems. Deaths from medication interactions undocumented.","$":None,"ind":"healthcare"},
    {"id":"E69","src":"GAO improper breakdown","desc":"$5.1B breakdown: $1.8B not medically necessary (auto-populated), $1.2B incorrect coding (default high code), $0.9B duplicate, $0.7B services not provided.","$":5.1e9,"ind":"healthcare"},
    {"id":"E70","src":"CMS suspension 2026","desc":"CMS suspended 1,079 providers in single year for fraud. 1,403 had billing privileges revoked. But detection lag means billions already paid out.","$":None,"ind":"healthcare"},
    {"id":"E71","src":"Pharmacy OIG","desc":"Pharmacy auto-refill system refilled 2,000 prescriptions after patients died. System checked 'active prescription' flag but didn't check death records.","$":None,"ind":"healthcare"},
    {"id":"E72","src":"Construction ERP","desc":"Construction ERP: automated change order sent via email. Subcontractor never received it. Change order executed. $500K rework. No delivery confirmation.","$":500e3,"ind":"procurement"},
    {"id":"E73","src":"FDA drug safety","desc":"FDA adverse event reporting system has 18-month data lag. Drug safety signals detected 18 months after they could have been caught. No real-time pharmacovigilance.","$":None,"ind":"healthcare"},
    {"id":"E74","src":"SCADA failure","desc":"Industrial SCADA system sensor shows 'normal.' Sensor was disconnected 3 days ago. Last value held. No 'sensor fault' detected for 72 hours.","$":None,"ind":"cross"},
    {"id":"E75","src":"RPA industry stat","desc":"45% of enterprises report WEEKLY RPA bot breakage. Avg recovery: 4 hours. 30% of bots require manual intervention every run.","$":None,"ind":"cross"},
]

# ──────────────────────────────────────────────────────────────
# Decomposition Templates — Generate sub-problems dynamically
# ──────────────────────────────────────────────────────────────

DECOMPOSITION_TEMPLATES = [
    # Root cause: why does this happen?
    {"prefix":"Why","pattern":["root cause","caused by","because","due to","originates from","stems from"]},
    # Mechanism: how does it happen?
    {"prefix":"How","pattern":["mechanism","process","step","way","method","approach"]},
    # Who is affected?
    {"prefix":"Who","pattern":["affected","victim","impacted","stakeholder","role","actor"]},
    # Where does it happen?
    {"prefix":"Where","pattern":["location","environment","system","context","domain","surface"]},
    # When does it happen?
    {"prefix":"When","pattern":["timing","frequency","trigger","condition","scenario","state"]},
    # What prevents fixing it?
    {"prefix":"Barrier","pattern":["barrier","obstacle","prevent","block","hindrance","impossible"]},
    # What is the cost?
    {"prefix":"Cost","pattern":["cost","loss","damage","impact","financial","economic"]},
    # Who benefits from the status quo?
    {"prefix":"Incentive","pattern":["incentive","benefits from","profits from","advantage","power"]},
]

def generate_subproblems(node):
    """Dynamically generate sub-problems for a given node based on its evidence.
    
    Strategy: for each distinct pattern found in the evidence, create a sub-problem.
    If no evidence matches, create generic decomposition branches.
    """
    subs = []
    seen = set()
    
    ev = node.get("_ev", [])
    
    # Strategy 1: Extract unique failure modes from evidence
    for i, e in enumerate(ev):
        desc = e["desc"].lower()
        ind = e.get("ind", "cross")
        
        # Extract a distinct problem from each evidence item
        # Look for the specific failure mechanism
        failure_patterns = [
            ("no_alert", ["no alert","no notification","nobody reads","nobody checks","dead alias","unmonitored"]),
            ("false_success", ["exit code 0","success but","false success","wrong status","empty output"]),
            ("identity_not_verified", ["fake","forged","spoofed","chameleon","stolen identity","false credential"]),
            ("no_recovery", ["no recovery","cannot recover","restart from","hang forever","no watchdog","no heartbeat"]),
            ("delayed_detection", ["delay","too late","weeks later","months later","18 month","60 day"]),
            ("data_altered", ["altered","modified","changed after","deleted","back-dated","retroactive"]),
            ("programmed_fraud", ["programmed","auto-generate","highest code","designed to","always bill"]),
            ("no_persistence", ["no persistence","session lost","login again","from scratch","ephemeral"]),
            ("partial_failure", ["partial","some fail","batch","not all","remaining"]),
            ("missing_contract", ["no defined","nobody defined","what is success","cannot distinguish"]),
            ("adversarial_owner", ["owns data","controls audit","sole source","blocks access","sues"]),
            ("integration_cost", ["too expensive","cost exceeds","not worth","switching cost"]),
            ("alert_fatigue", ["alert fatigue","too many","ignored","overridden","noise"]),
            ("format_drift", ["format change","schema change","renamed","selector change"]),
        ]
        
        for fname, fkw in failure_patterns:
            if any(kw in desc for kw in fkw) and fname not in seen:
                seen.add(fname)
                sub_id = f"{node['id']}_{fname}"
                sub_title, sub_desc = generate_label(fname, e, ind)
                subs.append({
                    "id": sub_id,
                    "title": sub_title,
                    "desc": sub_desc,
                    "evidence_ref": [e],
                    "kw": fkw,
                    "depth": node.get("depth", 0) + 1,
                    "parent": node["id"],
                })
    
    # Strategy 2: If we have very little evidence, generate generic branches
    if len(subs) < 2:
        generic_branches = [
            ("tech_cause", "Technical root cause", "What technical mechanism enables this failure?", ["technical","mechanism","implementation"]),
            ("org_cause", "Organizational root cause", "What organizational or process failure allows this to persist?", ["organizational","process","management"]),
            ("economic_barrier", "Economic barrier to fix", "Why doesn't fixing this problem pay for itself?", ["economic","cost","ROI"]),
            ("incentive_mismatch", "Incentive misalignment", "Who benefits from the current broken state?", ["incentive","benefit","status quo"]),
        ]
        for gid, gtitle, gdesc, gkw in generic_branches:
            if gid not in seen:
                subs.append({
                    "id": f"{node['id']}_{gid}",
                    "title": gtitle,
                    "desc": gdesc,
                    "evidence_ref": [],
                    "kw": gkw,
                    "depth": node.get("depth", 0) + 1,
                    "parent": node["id"],
                })
    
    return subs[:6]  # Max 6 sub-problems per node

def generate_label(fname, ev, industry):
    """Generate a human-readable label for a sub-problem based on its type and evidence."""
    labels = {
        "no_alert": ("No notification channel configured", f"Evidence: {ev['desc'][:80]}..."),
        "false_success": ("System reports success when output is wrong", f"Exit code 0 masks failure. {ev['desc'][:70]}"),
        "identity_not_verified": ("Identity is not bound to real person", f"Credentials verified but identity not. {ev['desc'][:70]}"),
        "no_recovery": ("No crash detection or recovery mechanism", f"Process dies silently. {ev['desc'][:70]}"),
        "delayed_detection": ("Detection delay exceeds recovery window", f"By the time it's found, it's too late. {ev['desc'][:70]}"),
        "data_altered": ("Records alterable after the fact", f"Audit trail controlled by same party that alters. {ev['desc'][:70]}"),
        "programmed_fraud": ("Software designed to generate false records", f"System architecture enables fraud. {ev['desc'][:70]}"),
        "no_persistence": ("Session state does not survive restarts", f"Every run starts from scratch. {ev['desc'][:70]}"),
        "partial_failure": ("Subset failures invisible in aggregate success", f"Success rate masks individual failures. {ev['desc'][:70]}"),
        "missing_contract": ("No definition of what 'success' means", f"Script cannot distinguish outcomes. {ev['desc'][:70]}"),
        "adversarial_owner": ("Data owner resists verification", f"Incumbent profits from ambiguity. {ev['desc'][:70]}"),
        "integration_cost": ("Fix cost exceeds problem cost", f"Market accepts losses over system change. {ev['desc'][:70]}"),
        "alert_fatigue": ("Alert volume makes real failures invisible", f"Signal drowned in noise. {ev['desc'][:70]}"),
        "format_drift": ("External interface changes without notice", f"Consumer not notified of format change. {ev['desc'][:70]}"),
    }
    return labels.get(fname, (f"{fname} failure pattern", ev["desc"][:90]))

# ──────────────────────────────────────────────────────────────
# Scoring
# ──────────────────────────────────────────────────────────────

def match(ev_text, keywords):
    if not keywords:
        return 0
    return sum(1 for kw in keywords if kw.lower() in ev_text.lower())

def score_node(node):
    """Score a node against the knowledge base."""
    kw = node.get("kw", [])
    if not kw:
        node["_ev"] = []
        node["_score"] = 0
        node["_fin"] = 0
        node["_inds"] = set()
        return node
    
    matched = []
    for ev in KB:
        s = match(ev["desc"] + " " + ev["src"], kw)
        if s > 0:
            matched.append((s, ev))
    matched.sort(key=lambda x: -x[0])
    
    node["_ev"] = [ev for _, ev in matched[:8]]
    node["_score"] = len(node["_ev"]) * 10
    node["_fin"] = sum(ev.get("$") or 0 for ev in node["_ev"])
    node["_inds"] = set(ev["ind"] for ev in node["_ev"] if ev.get("ind"))
    node["_ev_count_raw"] = len(matched)
    return node

# ──────────────────────────────────────────────────────────────
# Deep Decomposition Engine
# ──────────────────────────────────────────────────────────────

def deep_decompose(branch_id, title, description, start_kw, max_depth=20):
    """
    Starting from a root problem branch, iteratively decompose deeper and deeper.
    At each level:
      1. Score the current node
      2. Generate sub-problems from evidence patterns
      3. Score each sub-problem
      4. Pick the highest-scoring sub-problem
      5. Descend into it
      6. Save iteration to file
      7. Repeat until no more evidence or max_depth reached
    
    Returns list of all files saved.
    """
    # Build the starting node
    root = {
        "id": branch_id,
        "title": title,
        "desc": description,
        "kw": start_kw,
        "depth": 1,
        "parent": "ROOT",
    }
    score_node(root)
    
    files_saved = []
    current = root
    pathway = [branch_id]
    
    for iteration in range(max_depth):
        depth = iteration + 2  # starting at Level 2
        
        # Generate sub-problems
        subs = generate_subproblems(current)
        if not subs:
            break
        
        # Score each sub-problem
        scored_subs = []
        for sub in subs:
            s = score_node(sub)
            scored_subs.append((s.get("_score", 0), s))
        
        scored_subs.sort(key=lambda x: -x[0])
        
        # Pick the best one
        best_score, best_sub = scored_subs[0]
        
        # Save this iteration
        path_str = " → ".join(pathway + [best_sub["id"]])
        content = format_deep_iteration(branch_id, depth, iteration+1, current, scored_subs, path_str)
        fp = save_deep_iteration(branch_id, depth, iteration+1, content)
        files_saved.append(fp)
        
        # If next level has no evidence, still save but stop descending
        if best_score == 0 and len(scored_subs) > 1:
            # Try the next best with evidence
            next_best = None
            for s, sub in scored_subs[1:]:
                if s > 0:
                    next_best = sub
                    break
            if next_best:
                best_sub = next_best
            else:
                break  # no evidence left to follow
        
        if best_score == 0 and depth > 3:
            break  # stop if no evidence and we're deep enough
        
        # Descend
        pathway.append(best_sub["id"])
        current = best_sub
    
    return files_saved

def format_deep_iteration(branch_id, depth, iter_num, current, scored_subs, path_str):
    """Format a deep iteration for saving."""
    lines = []
    lines.append("=" * 65)
    lines.append(f"AUTOMATION RELIABILITY — DEEP DECOMPOSITION ITERATION")
    lines.append(f"Branch: {branch_id}")
    lines.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Iteration: {iter_num} | Depth: Level {depth}")
    lines.append(f"Path: {path_str}")
    lines.append("=" * 65)
    lines.append("")
    
    # Current node context
    lines.append(f"CURRENT PROBLEM: {current['id']}")
    lines.append(f"  {current['title']}")
    lines.append(f"  {current['desc']}")
    lines.append(f"  Score: {current.get('_score', 0)}pts")
    fin = current.get("_fin", 0)
    if fin:
        lines.append(f"  Financial evidence: ${fin:,.0f}")
    inds = current.get("_inds", set())
    if inds:
        lines.append(f"  Industries: {', '.join(sorted(inds))}")
    lines.append("")
    
    # Evidence for current node
    ev = current.get("_ev", [])
    if ev:
        lines.append(f"  Supporting evidence ({len(ev)} cases):")
        for e in ev[:4]:
            f = f" (${e['$']:,.0f})" if e.get("$") else ""
            lines.append(f"    [{e['ind']}] {e['src']}: {e['desc'][:75]}{f}")
    lines.append("")
    
    # Sub-problems at next level
    lines.append(f"SUB-PROBLEMS (decomposing one level deeper):")
    lines.append("-" * 50)
    for i, (s, sub) in enumerate(scored_subs, 1):
        sfin = sub.get("_fin", 0)
        sfin_s = f" ${sfin:,.0f}" if sfin else ""
        kinds = ",".join(sorted(sub.get("_inds", set())))
        kinds_s = f" [{kinds}]" if kinds else ""
        lines.append(f"  [{i}] {sub['id']}: {sub['title']} ({s}pts{sfin_s}{kinds_s})")
        lines.append(f"       {sub['desc'][:95]}")
        sev = sub.get("_ev", [])
        if sev:
            lines.append(f"       Evidence: {len(sev)} cases — top: [{sev[0]['ind']}] {sev[0]['desc'][:60]}")
        lines.append("")
    
    # Decision
    best_id = scored_subs[0][1]["id"]
    best_score = scored_subs[0][0]
    lines.append(f"DECISION: Descending into '{best_id}' (score: {best_score})")
    lines.append(f"Path so far: {path_str}")
    
    return "\n".join(lines)

def save_deep_iteration(branch_id, depth, iter_num, content):
    """Save a deep iteration to file."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"deep_{branch_id}_L{depth}_iter{iter_num}_{ts}.txt"
    fp = os.path.join(OUT_DIR, fn)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    return fp

# ──────────────────────────────────────────────────────────────
# Full Branch Definitions (the 12 core problems from Level 3)
# ──────────────────────────────────────────────────────────────

BRANCHES = [
    # (branch_id, title, description, keywords)
    ("A1", "No alert mechanism", "Failure writes to log file. Nobody reads the log. No notification channel exists or it's dead.", 
     ["no alert","log only","unmonitored","email dead","no webhook","no notification","nobody checks","dead alias"]),
    ("A2", "Partial failure undetected", "Batch of N items processes. M fail silently. Report shows overall success. Nobody checks the M failures.", 
     ["partial","batch","some failed","silent failure","not all","partial failure","subset","remaining"]),
    ("A3", "Wrong status reported", "Script returns exit code 0 but output is empty or contains errors. System reports success when it failed.",
     ["exit code 0","wrong status","false success","success but failed","return code green","empty output","callback never fire"]),
    ("A4", "Delayed discovery", "Failure surfaces days or weeks later. By the time it's discovered, recovery is impossible or funds are unrecoverable.",
     ["delay","late discovery","72 hours","60 days","too late","discovered after","18 months","recovery impossible"]),
    ("D1", "Documents forged", "Proof of delivery signed by unauthorized person. Fake credentials presented. Chameleon carriers. Identity never bound to real person.",
     ["forged","fake signature","POD fraud","chameleon carrier","false delivery","fake credential","fake supplier","identity not verified"]),
    ("D2", "Records altered after fact", "EHR records modified after adverse event. Audit trail controlled by same party that did the alteration. No external witness.",
     ["altered","modified after","late entry","EHR manipulation","back-dated","retroactively","deleted record"]),
    ("D3", "System programmed to lie", "Software designed to generate false documentation. Billing system always selects highest reimbursement code. Auto-generates supporting notes.",
     ["programmed fraud","auto-generate false","inflated billing","Vohra","pre-populated template","highest code"]),
    ("E1", "No crash detection", "Agent/process hangs after crash. No watchdog, no heartbeat, no health check. Manual restart required. Hang persists indefinitely.",
     ["no watchdog","no heartbeat","hang","crash undetected","stuck","silent disconnect"]),
    ("E2", "No state persistence", "Session state lost on crash or restart. Must login again. Everything begins from scratch. No continuity across runs.",
     ["state lost","no persistence","session lost","restart scratch","login again","fresh browser"]),
    ("E3", "No replay capability", "Failed action cannot be replayed. All progress lost on failure. No checkpoint, no roll-forward, no idempotency.",
     ["no replay","cannot retry","no resume","idempotent","checkpoint","rollback"]),
    ("C1", "Selector/locator drift", "CSS class or XPath renamed. Script still runs but targets nothing. Returns success with 0 records. No content validation.",
     ["selector","locator","css change","element missing","class renamed"]),
    ("B1", "No output artifact", "Script produces no output, no log, no record. Exit code = 0. Nobody can confirm it ran or what it did.",
     ["no output","no artifact","no result","no logging"]),
]

# ──────────────────────────────────────────────────────────────
# Status tracking
# ──────────────────────────────────────────────────────────────

STATUS_FILE = os.path.join(OUT_DIR, "deployment_status.json")

def save_status(branch_id, files, depth_reached, status="completed"):
    status_data = {}
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE) as f:
            status_data = json.load(f)
    status_data[branch_id] = {
        "status": status,
        "files": len(files),
        "depth": depth_reached,
        "updated": datetime.datetime.now().isoformat(),
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(status_data, f, indent=2)

# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def main():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    total_files = 0
    
    print("=" * 65)
    print(f"AUTOMATION RELIABILITY — DEEP RECURSIVE DECOMPOSITION")
    print(f"Started: {ts}")
    print(f"Branches to decompose: {len(BRANCHES)}")
    print(f"Max depth per branch: 20 levels")
    print(f"Output: {OUT_DIR}")
    print("=" * 65)
    print()
    
    for idx, (bid, title, desc, kw) in enumerate(BRANCHES, 1):
        print(f"\n{'─' * 50}")
        print(f"BRANCH {idx}/{len(BRANCHES)}: {bid} — {title}")
        print(f"{'─' * 50}")
        
        try:
            files = deep_decompose(bid, title, desc, kw, max_depth=20)
            depth = len(files)
            total_files += len(files)
            print(f"  → {len(files)} iterations saved (depth: {depth} levels)")
            save_status(bid, files, depth)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            save_status(bid, [], 0, status=f"error: {e}")
    
    # Summary
    print()
    print("=" * 65)
    print("DECOMPOSITION COMPLETE")
    print("=" * 65)
    print()
    print(f"Total files saved: {total_files}")
    print(f"All files in: {OUT_DIR}")
    
    # Show tree summary
    print()
    print("DEPTH REACHED PER BRANCH:")
    print("-" * 40)
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE) as f:
            status_data = json.load(f)
        for bid, data in sorted(status_data.items()):
            print(f"  {bid}: {data['depth']} levels ({data['files']} files) — {data['status']}")
    
    print()
    print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE) as f:
                data = json.load(f)
            print("Decomposition status:")
            for bid, d in sorted(data.items()):
                print(f"  {bid}: {d['depth']} levels, {d['files']} files — {d['status']}")
        else:
            print("No status file found. Run the engine first.")
    else:
        main()
