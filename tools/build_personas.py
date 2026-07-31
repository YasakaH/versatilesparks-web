#!/usr/bin/env python3
"""
Automated Persona Builder and Evidence Collector

Purpose: Build 3-5 diverse personas using the CORE behavioural architecture,
collect structured evidence via validation logs, and prepare Operational Validation Report v1.
"""

import os
from datetime import datetime
from pathlib import Path

# Define persona templates
PERSONA_TEMPLATES = {
    "Principal Engineer": {
        "domain": "engineering",
        "purpose": "Architecture decisions, trade-offs, system design, technical leadership",
        "capabilities": ["PLANNING_FRAMEWORK", "DECISION_FRAMEWORK", "VERIFICATION_PATTERNS"],
        "scenarios": [
            "Design a caching strategy for high-traffic API",
            "Evaluate database migration from SQL to NoSQL",
            "Define observability strategy for distributed system"
        ]
    },
    "Staff Engineer": {
        "domain": "engineering",
        "purpose": "Deep technical implementation, code quality, performance optimization",
        "capabilities": ["PLANNING_FRAMEWORK", "DECISION_FRAMEWORK", "VERIFICATION_PATTERNS"],
        "scenarios": [
            "Implement rate limiting for API endpoint",
            "Optimize database query performance",
            "Refactor legacy codebase for maintainability"
        ]
    },
    "Product Manager": {
        "domain": "product",
        "purpose": "Requirements, prioritisation, stakeholder alignment, roadmap",
        "capabilities": ["PLANNING_FRAMEWORK", "DECISION_FRAMEWORK", "UNCERTAINTY_HANDLING"],
        "scenarios": [
            "Define MVP scope for new feature",
            "Prioritise backlog based on user impact",
            "Align engineering and design on user story"
        ]
    },
    "UX Designer": {
        "domain": "design",
        "purpose": "User research, interface decisions, usability, accessibility",
        "capabilities": ["PLANNING_FRAMEWORK", "DECISION_FRAMEWORK", "VERIFICATION_PATTERNS"],
        "scenarios": [
            "Design user flow for checkout process",
            "Conduct usability testing on new interface",
            "Define accessibility standards"
        ]
    },
    "Security Engineer": {
        "domain": "security",
        "purpose": "Threat modeling, risk assessment, compliance, security reviews",
        "capabilities": ["PLANNING_FRAMEWORK", "DECISION_FRAMEWORK", "UNCERTAINTY_HANDLING", "VERIFICATION_PATTERNS"],
        "scenarios": [
            "Perform threat modeling for new API",
            "Conduct security review of code changes",
            "Define compliance requirements"
        ]
    }
}

class PersonaBuilder:
    def __init__(self, base_dir="E:/Hermes Projects/personas"):
        self.base_dir = Path(base_dir)
        self.validation_logs_dir = self.base_dir / "validation-logs"
        self.validation_logs_dir.mkdir(exist_ok=True)
        
    def build_persona(self, persona_name, domain, purpose, capabilities, scenarios):
        """Build a persona definition and create validation log"""
        persona_dir = self.base_dir / domain / persona_name.replace(" ", "-").lower()
        persona_dir.mkdir(parents=True, exist_ok=True)
        
        # Create persona definition
        persona_def = f"""# {persona_name}

## Domain
{domain}

## Purpose
{purpose}

## Core Capabilities Used
{' '.join(capabilities)}

## Scenarios to Test
{chr(10).join([f'- {s}' for s in scenarios])}

## Validation Status
- [ ] Persona built
- [ ] Scenarios executed
- [ ] Evidence collected
- [ ] Review completed
"""
        
        with open(persona_dir / "persona-definition.md", "w") as f:
            f.write(persona_def)
        
        # Create validation log
        log_path = self.validation_logs_dir / f"{persona_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.md"
        
        log_content = f"""# Persona Validation Log: {persona_name}

## Persona Details
- **Domain:** {domain}
- **Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Persona ID:** {persona_name.lower().replace(' ', '-')}

### Scenario Executed
**Task:** [Fill in after execution]
**Context:** [Fill in after execution]

### Lifecycle Stages Observed
- [ ] Understand
- [ ] Plan
- [ ] Validate
- [ ] Execute
- [ ] Verify
- [ ] Reflect

### Capability Documents Referenced
| Document | Purpose | Friction Level (1-5) | Notes |
|----------|---------|----------------------|-------|
| PLANNING_FRAMEWORK.md | Task decomposition, estimation |  |  |
| DECISION_FRAMEWORK.md | Option selection, prioritisation |  |  |
| UNCERTAINTY_HANDLING.md | Confidence calibration |  |  |
| VERIFICATION_PATTERNS.md | Correctness validation |  |  |
| CONTINUOUS_IMPROVEMENT.md | Adaptation and learning |  |  |
| EXECUTION_WORKFLOW.md | Orchestration |  |  |

### Observations
**Friction Points:**
- [ ] Hesitation at lifecycle stage: 
- [ ] Required additional guidance: 
- [ ] Repeated failure at stage: 
- [ ] Document not referenced but needed: 

**Performance Bottlenecks:**
- [ ] Stage consuming most reasoning effort: 
- [ ] Most-used capability document: 
- [ ] Least-used capability document: 

### Classification
| Finding | Classification | Resolution | Evidence |
|---------|----------------|------------|----------|
|  | Architecture / Behaviour / Evidence / Usability | None / Refine doc / Add capability / Architectural change |  |

### Next Steps
- [ ] Document refinement needed
- [ ] Candidate behavioural improvement
- [ ] Candidate architectural change
- [ ] No action required

---
**Reviewer:** Automation System
**Persona ID:** {persona_name.lower().replace(' ', '-')}
"""
        
        with open(log_path, "w") as f:
            f.write(log_content)
        
        return persona_dir, log_path
    
    def build_all_personas(self, count=5):
        """Build specified number of personas across domains"""
        personas_to_build = list(PERSONA_TEMPLATES.keys())[:count]
        results = []
        
        for persona_name in personas_to_build:
            template = PERSONA_TEMPLATES[persona_name]
            persona_dir, log_path = self.build_persona(
                persona_name=persona_name,
                domain=template["domain"],
                purpose=template["purpose"],
                capabilities=template["capabilities"],
                scenarios=template["scenarios"]
            )
            results.append({
                "persona": persona_name,
                "domain": template["domain"],
                "directory": str(persona_dir),
                "log": str(log_path)
            })
        
        return results
    
    def generate_operational_validation_report(self, persona_results):
        """Generate Operational Validation Report v1"""
        report_path = self.base_dir / "Operational-Validation-Report-v1.md"
        
        # Count domains and capabilities
        domains = set(r["domain"] for r in persona_results)
        capabilities_used = set()
        scenarios_executed = []
        
        for result in persona_results:
            # Parse capabilities from persona definition
            persona_dir = Path(result["directory"])
            if (persona_dir / "persona-definition.md").exists():
                with open(persona_dir / "persona-definition.md") as f:
                    content = f.read()
                    # Extract capabilities (simplified)
                    if "PLANNING_FRAMEWORK" in content:
                        capabilities_used.add("PLANNING_FRAMEWORK")
                    if "DECISION_FRAMEWORK" in content:
                        capabilities_used.add("DECISION_FRAMEWORK")
                    if "UNCERTAINTY_HANDLING" in content:
                        capabilities_used.add("UNCERTAINTY_HANDLING")
                    if "VERIFICATION_PATTERNS" in content:
                        capabilities_used.add("VERIFICATION_PATTERNS")
            scenarios_executed.extend(PERSONA_TEMPLATES[result["persona"]]["scenarios"])
        
        # Generate report
        report = f"""# Operational Validation Report v1

## Executive Summary

**Report Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Personas Evaluated:** {len(persona_results)}  
**Domains Covered:** {len(domains)}  
**Capabilities Exercised:** {len(capabilities_used)}  

### Key Metrics

| Metric | Value |
|--------|-------|
| Total personas built | {len(persona_results)} |
| Domains represented | {len(domains)} |
| Capabilities exercised | {len(capabilities_used)} |
| Scenarios available | {len(scenarios_executed)} |
| Validation logs created | {len(list(self.validation_logs_dir.glob('*.md')))} |

### Personas Built

{' '.join([f'- {r["persona"]} ({r["domain"]})' for r in persona_results])}

### Capabilities Exercised

{' '.join([f'- {cap}' for cap in sorted(capabilities_used)])}

### Domains Covered

{' '.join([f'- {domain}' for domain in sorted(domains)])}

### Next Steps

1. Execute scenarios for each persona using the CORE behavioural architecture
2. Fill validation logs with actual observations
3. Synthesise findings after 10+ persona evaluations
4. Apply evidence threshold before considering architectural changes

---

**Report Generated By:** Automated Persona Builder  
**Next Review:** After collecting evidence from real usage
"""
        
        with open(report_path, "w") as f:
            f.write(report)
        
        return report_path

if __name__ == "__main__":
    builder = PersonaBuilder()
    results = builder.build_all_personas(count=5)
    report_path = builder.generate_operational_validation_report(results)
    
    print("✅ Persona builder completed successfully")
    print(f"✅ Personas built: {len(results)}")
    print(f"✅ Report generated: {report_path}")
    for result in results:
        print(f"  - {result['persona']} ({result['domain']})")