#!/usr/bin/env python3
"""
AI Liability Value Chain — Deep Probe Engine
============================================
Systematically probes each node/edge in the AI liability value chain,
going deeper level by level until information is exhausted.
All iterations saved to files, then consolidated.
"""

import os
import json
import sys
import time
from datetime import datetime, timezone

# ── Config ──
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "liability-probes")
os.makedirs(OUT_DIR, exist_ok=True)

# ── The Value Chain Nodes to Probe ──
NODES = {
    "agent-frameworks": {
        "label": "Agent Frameworks — Trace Data Outputs",
        "queries": [
            "OpenAI Agents SDK trace output format event log underwriting",
            "LangGraph trace export format observability tool calls",
            "CrewAI trace log event data structure available",
            "Pydantic AI execution trace format structured logging",
            "MCP protocol server logging monitoring audit trail",
        ]
    },
    "observability-layer": {
        "label": "Observability Tools — Underwriting Export Capability",
        "queries": [
            "LangSmith export trace data compliance underwriting format",
            "Langfuse export execution traces API format",
            "Arize AI export agent traces monitoring",
            "Braintrust export execution logs format",
            "Datadog AI agent tracing monitoring export",
        ]
    },
    "carriers": {
        "label": "AI Liability Carriers — Underwriting + Claims Process",
        "queries": [
            "Mount AI agent insurance underwriting process data requirements",
            "Klaimee AI agent insurance risk scoring methodology",
            "Armilla AI liability underwriting claims process evidence",
            "Corgi AI insurance underwriting claims coverage",
            "Munich Re aiSure underwriting model performance",
        ]
    },
    "claims-process": {
        "label": "Claims Investigation — Manual Workflow + Cost",
        "queries": [
            "AI agent insurance claim investigation process manual hours cost",
            "AI incident forensics evidence collection framework cost",
            "Cyber insurance AI exclusion claim denial evidence requirements",
            "AI agent liability claim dispute resolution process",
            "AI agent post-incident reconstruction timeline tools",
        ]
    },
    "regulatory": {
        "label": "Regulatory — Forcing Functions for Evidence Standards",
        "queries": [
            "NAIC model bulletin AI insurance evidence requirements 2026",
            "EU AI Act high-risk AI system audit trail documentation",
            "ISO AI exclusion endorsements CG 40 47 01 26 impact",
            "Air Canada chatbot liability ruling implications evidence",
            "FINRA AI agent human checkpoint requirement 2026",
        ]
    },
    "ttl-expiry-primitive": {
        "label": "Risk Freshness — TTL-bound Attestation",
        "queries": [
            "AI agent risk scoring freshness drift detection TTL certification",
            "Continuous underwriting AI agent behavior drift monitoring",
            "Agent attestation expiry re-verification drift detection",
            "AI agent compliance certification continuous monitoring",
            "Agent behavior drift detection runtime policy enforcement",
        ]
    },
    "incidents": {
        "label": "Known Incidents — Real-world Loss Events",
        "queries": [
            "PocketOS AI agent database deletion postmortem investigation cost",
            "AI agent production data loss incident recovery time cost 2025 2026",
            "OpenClaw inbox deletion AI agent incident investigation",
            "AI coding agent destructive action incident postmortem",
            "Replit AI agent production database deletion investigation",
        ]
    },
    "infrastructure-gap": {
        "label": "Infrastructure Gap — Missing Layer Evidence",
        "queries": [
            "AI agent execution trace standard underwriting evidence format proposal",
            "OpenTelemetry AI agent traces semantic conventions insurance",
            "AI agent SBOM attestation format underwriting risk scoring",
            "Cross-framework agent trace normalization insurance pricing",
            "Standardized AI agent claims evidence packet format",
        ]
    },
}

# ── Probe Function ──
def probe_node(node_key, node_config, max_depth=5):
    """Probe a node iteratively, going deeper level by level."""
    from hermes_tools import web_search, web_extract
    
    results = []
    base_queries = node_config["queries"]
    
    for depth in range(max_depth):
        level_dir = os.path.join(OUT_DIR, node_key, f"level_{depth+1}")
        os.makedirs(level_dir, exist_ok=True)
        
        queries = base_queries if depth == 0 else []
        if depth > 0:
            # Generate deeper queries from previous results
            for prev in results[-min(3, len(results)):]:
                if "url" in prev:
                    queries.append(f"site:{prev['url'].split('/')[2] if prev['url'] else ''} {' '.join(prev.get('title','').split()[:5])}")
        
        if not queries:
            break
            
        for q_idx, query in enumerate(queries):
            try:
                res = web_search(query=query, limit=5)
                time.sleep(0.5)
                
                iter_file = os.path.join(level_dir, f"probe_{q_idx+1}.json")
                with open(iter_file, "w") as f:
                    json.dump({"query": query, "results": res}, f, indent=2, default=str)
                
                results.append({"query": query, "results": res, "file": iter_file})
                print(f"  [{node_key}] depth={depth+1} q={q_idx+1}: {query[:60]}...")
                
            except Exception as e:
                print(f"  [{node_key}] ERROR depth={depth+1} q={q_idx+1}: {e}")
    
    # Save level summary
    summary = {"node": node_key, "label": node_config["label"], "depths_probed": max_depth, "queries_run": len(results)}
    with open(os.path.join(OUT_DIR, node_key, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    return summary

# ── Main ──
if __name__ == "__main__":
    print(f"AI Liability Value Chain — Deep Probe Engine")
    print(f"Output: {OUT_DIR}")
    print(f"Nodes: {len(NODES)}")
    print()
    
    all_summaries = []
    for key, config in NODES.items():
        print(f"\n{'='*60}")
        print(f"Probing: {config['label']}")
        print(f"{'='*60}")
        summary = probe_node(key, config, max_depth=5)
        all_summaries.append(summary)
        print()
    
    # Master summary
    master = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nodes_probed": len(all_summaries),
        "summaries": all_summaries,
    }
    with open(os.path.join(OUT_DIR, "_master_summary.json"), "w") as f:
        json.dump(master, f, indent=2, default=str)
    
    print(f"\n{'='*60}")
    print(f"ALL PROBES COMPLETE — {len(NODES)} nodes, {len(all_summaries)} summaries")
    print(f"Output: {OUT_DIR}")
