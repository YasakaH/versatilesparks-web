# Evidence Builder
# Transforms knowledge objects into mode-specific argument structures.

import re


def build(mode, objects, question):
    actual_mode = mode
    # Fallback: if compare mode but <2 objects, treat as explain with first object
    if actual_mode == "compare" and len(objects) < 2:
        actual_mode = "explain"

    builders = {
        "explain": _build_explain,
        "compare": _build_compare,
        "decide": _build_decide,
        "troubleshoot": _build_troubleshoot,
        "design": _build_design,
    }
    builder = builders.get(actual_mode, _build_explain)
    argument = builder(objects, question)

    errors = validate(actual_mode, argument)
    if errors:
        argument["_validation_errors"] = errors

    return argument, actual_mode


def _build_explain(objects, question):
    primary = objects[0] if objects else {}
    semantic = primary.get("semantic", "")
    related = [o["id"] for o in objects[1:4]] if len(objects) > 1 else []
    facts = _extract_bullets(semantic)

    if not facts:
        sentences = [s.strip() for s in semantic.split(".") if s.strip()]
        # Use all sentences as core mechanics for single-paragraph semantic
        definition = sentences[0] + "." if sentences else ""
        mechanics = sentences[1:] if len(sentences) > 1 else sentences
    else:
        definition = facts[0] if facts else ""
        mechanics = facts[1:] if len(facts) > 1 else facts

    examples = []
    narrative = _extract_narrative(primary.get("content", ""))
    if narrative:
        examples = [s.strip() for s in narrative.split(".") if s.strip()][:3]

    return {
        "target": primary.get("title", "Explanation"),
        "definition": definition,
        "core_mechanics": mechanics[:5],
        "examples": examples or ["See " + primary.get("title", "") + " knowledge object"],
        "limitations": [o.get("title", "") for o in objects[1:3]] if len(objects) > 1 else ["No limitations documented"],
    }


def _build_compare(objects, question):
    if len(objects) < 2:
        return _build_explain(objects, question)

    names = [o["title"] for o in objects[:2]]
    sem_a = objects[0].get("semantic", "")
    sem_b = objects[1].get("semantic", "")
    criteria = ["Cross-browser support", "Debugging depth", "Performance", "Ecosystem"]

    def first_sentence(text):
        parts = text.split(".")
        return (parts[0] + ".") if len(parts) > 1 and parts[0] else text[:100]

    return {
        "criteria": criteria,
        "scoring": {
            c: [
                {"name": names[0], "score": "varies", "evidence": first_sentence(sem_a)},
                {"name": names[1], "score": "varies", "evidence": first_sentence(sem_b)},
            ]
            for c in criteria
        },
        "tradeoffs": [names[0] + " vs " + names[1] + ": each optimizes for different constraints"],
        "recommendation": "Depends on whether you need " + criteria[0].lower() + " or " + criteria[1].lower(),
    }


def _build_decide(objects, question):
    primary = objects[0] if objects else {}
    semantic = primary.get("semantic", "")
    supporting = _extract_bullets(semantic)
    if not supporting:
        sentences = [s.strip() for s in semantic.split(".") if s.strip()]
        supporting = sentences[:3]
    risks = [o["id"] for o in objects[1:3]] if len(objects) > 1 else ["Unknown risks"]

    clean_q = question.strip().rstrip("?").strip().lower()
    claim = ("Should " + clean_q) if not clean_q.startswith("should") else clean_q

    return {
        "claim": claim,
        "supporting": supporting,
        "contradictory": ["Consider: " + r for r in risks],
        "risks": risks,
        "recommendation": "Based on " + str(len(supporting)) + " supporting factors and " + str(len(risks)) + " considerations",
    }


def _build_troubleshoot(objects, question):
    causes = []
    for obj in objects[:3]:
        semantic = obj.get("semantic", "")
        facts = _extract_bullets(semantic)
        causes.append({
            "cause": obj.get("title", "Unknown"),
            "probability": "high" if obj.get("score", 0) > 0.7 else "medium",
            "evidence": facts[0] if facts else semantic[:100],
            "diagnostic_steps": ["Check " + obj.get("title", obj["id"]) + " configuration"],
            "fix": "Review " + obj.get("title", obj["id"]) + " documentation",
        })

    return {
        "problem": question,
        "likely_causes": causes,
        "external_factors": ["Browser version differences", "Anti-detection mechanisms"],
    }


def _build_design(objects, question):
    options = []
    for obj in objects[:3]:
        options.append({
            "name": obj.get("title", "Option " + str(len(options) + 1)),
            "description": obj.get("semantic", "")[:150],
        })

    return {
        "problem": question,
        "approaches": options,
        "recommended": options[0]["name"] if options else "No recommendation",
        "pitfalls": ["Ignoring " + o.get("title", o["id"]) + " can cause issues" for o in objects[1:3]],
        "best_practices": ["Start simple", "Add complexity only when needed"],
    }


def validate(mode, argument):
    errors = []
    required_fields = {
        "explain": ["definition", "core_mechanics", "limitations"],
        "compare": ["criteria", "scoring", "tradeoffs"],
        "decide": ["claim", "supporting", "contradictory"],
        "troubleshoot": ["problem", "likely_causes"],
        "design": ["problem", "approaches"],
    }
    required = required_fields.get(mode, [])
    for field in required:
        if field not in argument or not argument[field]:
            errors.append("Missing required field: " + field)
    return errors


def _extract_narrative(content):
    m = re.search(r"## Narrative Layer\n(.+?)(?=\n## |\Z)", content, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else ""


def _extract_bullets(text):
    return [line.strip().lstrip("- ") for line in text.split("\n") if line.strip().startswith("-")]
