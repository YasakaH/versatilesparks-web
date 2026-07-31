# HPF Renderer
# Formats a structured Evidence Builder argument into markdown.

def format_explain(arg):
    lines = []
    lines.append("# " + arg.get("target", "Explanation"))
    lines.append("")
    lines.append("**Definition:** " + arg.get("definition", ""))
    lines.append("")
    if "core_mechanics" in arg:
        lines.append("## Core Mechanics")
        for m in arg["core_mechanics"]:
            lines.append("- " + str(m))
        lines.append("")
    if "examples" in arg:
        lines.append("## Examples")
        for e in arg["examples"]:
            lines.append("- " + str(e))
        lines.append("")
    if "limitations" in arg:
        lines.append("## Limitations")
        for l in arg["limitations"]:
            lines.append("- " + str(l))
        lines.append("")
    return "\n".join(lines)


def format_compare(arg):
    lines = []
    lines.append("# Comparison")
    lines.append("")
    if "criteria" in arg:
        lines.append("## Criteria")
        for c in arg["criteria"]:
            lines.append("- " + str(c))
        lines.append("")
    if "scoring" in arg:
        for criterion, options in arg["scoring"].items():
            lines.append("## " + criterion)
            for opt in options:
                name = opt.get("name", "")
                score = opt.get("score", "")
                evidence = opt.get("evidence", "")
                lines.append("- **" + name + ":** " + score + " - " + evidence)
        lines.append("")
    if "tradeoffs" in arg:
        lines.append("## Trade-offs")
        for t in arg["tradeoffs"]:
            lines.append("- " + str(t))
        lines.append("")
    if "recommendation" in arg:
        lines.append("**Recommendation:** " + arg["recommendation"])
        lines.append("")
    return "\n".join(lines)


def format_decide(arg):
    lines = []
    lines.append("# Decision Analysis")
    lines.append("")
    lines.append("**Claim:** " + arg.get("claim", ""))
    lines.append("")
    if "supporting" in arg:
        lines.append("## Supporting Evidence")
        for s in arg["supporting"]:
            lines.append("- " + str(s))
        lines.append("")
    if "contradictory" in arg:
        lines.append("## Contradictory Evidence")
        for c in arg["contradictory"]:
            lines.append("- " + str(c))
        lines.append("")
    if "risks" in arg:
        lines.append("## Risks")
        for r in arg["risks"]:
            lines.append("- " + str(r))
        lines.append("")
    if "recommendation" in arg:
        lines.append("**Recommendation:** " + arg["recommendation"])
        lines.append("")
    return "\n".join(lines)


def format_troubleshoot(arg):
    lines = []
    lines.append("# Troubleshooting")
    lines.append("")
    lines.append("**Problem:** " + arg.get("problem", ""))
    lines.append("")
    if "likely_causes" in arg:
        lines.append("## Likely Causes")
        for cause in arg["likely_causes"]:
            name = cause.get("cause", "")
            prob = cause.get("probability", "")
            lines.append("- **" + name + "** (probability: " + prob + ")")
            if "evidence" in cause:
                lines.append("  - Evidence: " + cause["evidence"])
            if "diagnostic_steps" in cause:
                for step in cause["diagnostic_steps"]:
                    lines.append("  - Diagnostic: " + step)
            if "fix" in cause:
                lines.append("  - Fix: " + cause["fix"])
        lines.append("")
    if "external_factors" in arg:
        lines.append("## External Factors")
        for f in arg["external_factors"]:
            lines.append("- " + str(f))
        lines.append("")
    return "\n".join(lines)


def format_design(arg):
    lines = []
    lines.append("# Design")
    lines.append("")
    lines.append("**Problem:** " + arg.get("problem", ""))
    lines.append("")
    if "approaches" in arg:
        lines.append("## Approach Options")
        for a in arg["approaches"]:
            name = a.get("name", "")
            desc = a.get("description", "")
            lines.append("- **" + name + ":** " + desc)
        lines.append("")
    if "recommended" in arg:
        lines.append("**Recommended:** " + arg["recommended"])
        lines.append("")
    if "pitfalls" in arg:
        lines.append("## Common Pitfalls")
        for p in arg["pitfalls"]:
            lines.append("- " + str(p))
        lines.append("")
    if "best_practices" in arg:
        lines.append("## Best Practices")
        for b in arg["best_practices"]:
            lines.append("- " + str(b))
        lines.append("")
    return "\n".join(lines)


FORMATTERS = {
    "explain": format_explain,
    "compare": format_compare,
    "decide": format_decide,
    "troubleshoot": format_troubleshoot,
    "design": format_design,
}


def render(mode, argument):
    formatter = FORMATTERS.get(mode, format_explain)
    return formatter(argument)
