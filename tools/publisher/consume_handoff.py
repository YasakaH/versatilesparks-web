#!/usr/bin/env python3
"""
consume_handoff.py — Publishing-side tool that consumes an HPF KnowledgePackage
and produces website-ready content.

Usage:
    # Consume latest handoff and scaffold articles from briefs
    python tools/publisher/consume_handoff.py handoff/latest.json --scaffold

    # Generate problem MDX files for website from packaged problems
    python tools/publisher/consume_handoff.py handoff/latest.json --problems

    # Generate feedback from publishing signals
    python tools/publisher/consume_handoff.py handoff/latest.json --feedback

    # Outline only (brief -> structured outline, not full draft)
    python tools/publisher/consume_handoff.py handoff/latest.json --outline
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONCEPT_MAP_PATH = REPO_ROOT / "knowledge" / "concept-map.json"
MIN_SCHEMA_VERSION = "1.0"


def load_concept_map() -> dict:
    """Load the HPF-to-website concept ID mapping."""
    if not CONCEPT_MAP_PATH.exists():
        print(f"Warning: concept map not found at {CONCEPT_MAP_PATH}")
        return {"hpf_to_website": {}, "website_to_hpf": {}}
    return json.loads(CONCEPT_MAP_PATH.read_text(encoding="utf-8"))


def map_concept(hpf_id: str, mapping: dict) -> str:
    """Map an HPF concept ID to a website concept ID."""
    return mapping.get("hpf_to_website", {}).get(hpf_id, hpf_id)


# ──────────────────────────────────────────────
# 1. Schema versioning — compatibility check
# ──────────────────────────────────────────────

def parse_semver(v: str) -> tuple:
    parts = v.lstrip(">=^~").split(".")
    try:
        return tuple(int(p) for p in parts[:3])
    except (ValueError, IndexError):
        return (0, 0, 0)


def check_compatibility(pkg: dict) -> None:
    """Reject packages whose schema or compatibility range doesn't match."""
    schema_ver = pkg.get("schema_version", pkg.get("version", "0.1"))

    if parse_semver(schema_ver) < parse_semver(MIN_SCHEMA_VERSION):
        print(f"Error: schema v{schema_ver} < minimum v{MIN_SCHEMA_VERSION}")
        print(f"  Producer: {pkg.get('producer', '?')} v{pkg.get('producer_version', '?')}")
        print(f"  This publishing tool requires schema >= {MIN_SCHEMA_VERSION}.")
        sys.exit(1)

    compat = pkg.get("compatibility", ">=0.1")
    match = re.match(r">=(\S+)", compat)
    if match:
        required = match.group(1)
        # Publishing tool version — this script IS the consumer
        if parse_semver("0.4") < parse_semver(required):
            print(f"Error: package requires publishing {compat}, this tool is v0.4")
            sys.exit(1)

    print(f"  Schema: v{schema_ver} | Producer: {pkg.get('producer', '?')} v{pkg.get('producer_version', '?')}")
    if pkg.get("generated_at"):
        print(f"  Generated: {pkg['generated_at']}")


# ──────────────────────────────────────────────
# 2. Quality Gate — validate before consuming
# ──────────────────────────────────────────────

def validate_package(pkg: dict, mapping: dict, strict: bool = False) -> list[str]:
    """Validate a KnowledgePackage before consuming it.

    In strict mode, orphan concepts are hard errors instead of warnings.
    Development: strict=False (warnings). Release: --strict (errors).

    Returns a list of error messages. Empty list means valid.
    """
    errors = []
    warnings = []
    concept_ids = set(c["id"] for c in pkg.get("concepts", []))
    brief_ids = set()
    problem_ids = set()
    brief_titles = set()

    for brief in pkg.get("briefs", []):
        bid = brief.get("id", "")
        if bid in brief_ids:
            errors.append(f"Duplicate brief id: {bid}")
        brief_ids.add(bid)

        title = brief.get("title", "")
        if title in brief_titles:
            errors.append(f"Duplicate brief title: {title}")
        brief_titles.add(title)

        pc = brief.get("primary_concept", "")
        hpf_id = next((k for k, v in mapping.get("hpf_to_website", {}).items() if v == map_concept(pc, mapping)), pc)
        if pc and hpf_id not in concept_ids and pc not in concept_ids:
            errors.append(f"Brief '{bid}': primary_concept '{pc}' not in concept list")

        for sc in brief.get("secondary_concepts", []):
            hpf_sc = next((k for k, v in mapping.get("hpf_to_website", {}).items() if v == map_concept(sc, mapping)), sc)
            if sc and hpf_sc not in concept_ids and sc not in concept_ids:
                errors.append(f"Brief '{bid}': secondary_concept '{sc}' not in concept list")

        if not brief.get("cta"):
            errors.append(f"Brief '{bid}': missing CTA")

        if brief.get("audience") not in ("beginner", "intermediate", "advanced"):
            errors.append(f"Brief '{bid}': invalid audience '{brief.get('audience')}'")

    for problem in pkg.get("problems", []):
        pid = problem.get("id", "")
        if pid in problem_ids:
            errors.append(f"Duplicate problem id: {pid}")
        problem_ids.add(pid)

        pc = problem.get("primary_concept", "")
        hpf_pc = next((k for k, v in mapping.get("hpf_to_website", {}).items() if v == map_concept(pc, mapping)), pc)
        if pc and hpf_pc not in concept_ids and pc not in concept_ids:
            errors.append(f"Problem '{pid}': primary_concept '{pc}' not in concept list")

        for rc in problem.get("related_concepts", []):
            hpf_rc = next((k for k, v in mapping.get("hpf_to_website", {}).items() if v == map_concept(rc, mapping)), rc)
            if rc and hpf_rc not in concept_ids and rc not in concept_ids:
                errors.append(f"Problem '{pid}': related_concept '{rc}' not in concept list")

        if not problem.get("error_patterns"):
            errors.append(f"Problem '{pid}': no error_patterns")
        if not problem.get("root_cause"):
            errors.append(f"Problem '{pid}': no root_cause")

    # Orphan concepts — warnings only (expected at early stage)
    all_refs = set()
    for brief in pkg.get("briefs", []):
        pc = brief.get("primary_concept", "")
        all_refs.add(pc)
        all_refs.add(map_concept(pc, mapping))
        for sc in brief.get("secondary_concepts", []):
            all_refs.add(sc)
            all_refs.add(map_concept(sc, mapping))
    for prob in pkg.get("problems", []):
        pc = prob.get("primary_concept", "")
        all_refs.add(pc)
        all_refs.add(map_concept(pc, mapping))
        for rc in prob.get("related_concepts", []):
            all_refs.add(rc)
            all_refs.add(map_concept(rc, mapping))

    for cid in concept_ids:
        mapped = map_concept(cid, mapping)
        if cid not in all_refs and mapped not in all_refs:
            msg = f"Concept '{cid}' not referenced by any brief or problem"
            if strict:
                errors.append(msg)
            else:
                warnings.append(msg)

    for w in warnings:
        print(f"  Warning: {w}")
    if strict and warnings:
        print("  (strict mode — orphan concepts promoted to errors)")

    return errors


# ──────────────────────────────────────────────
# 3. Scaffolding
# ──────────────────────────────────────────────


def scaffold_articles(pkg: dict, mapping: dict, dry_run: bool = False) -> list[Path]:
    """Scaffold article markdown files from KnowledgePackage briefs."""
    drafts_dir = REPO_ROOT / "articles" / "draft"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    created = []

    for brief in pkg.get("briefs", []):
        slug = brief["id"]
        target = drafts_dir / f"{slug}.md"
        if target.exists():
            print(f"  Skip (exists): {target.name}")
            continue

        website_concept = map_concept(brief["primary_concept"], mapping)
        related_concepts = [map_concept(c, mapping) for c in brief.get("secondary_concepts", [])]
        all_concepts = [website_concept] + [c for c in related_concepts if c != website_concept]
        all_concepts = list(dict.fromkeys(all_concepts))

        canonical_url = f"https://versatilesparks.qzz.io/concepts/{website_concept}"

        tags = ["nodriver", "python", "browser-automation", website_concept]
        if brief.get("audience") == "advanced":
            tags.append("advanced")

        pain_points = brief.get("pain_points", [])
        description_text = brief.get("goal", brief["title"])
        if pain_points:
            description_text = f"{description_text} Covers: {', '.join(pain_points)}."

        content = f"""---
title: "{brief['title']}"
description: "{description_text}"
published: false
date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
tags: [{', '.join(tags)}]
canonical_url: {canonical_url}
slug: {slug}
concepts: {json.dumps(all_concepts)}
cta: {json.dumps(brief.get('cta', ''))}
---

## The Problem

[{'; '.join(pain_points) if pain_points else 'Pain point to be filled'}]

## Why It Happens

[Root cause to be filled based on HPF research]

## The Fix

```python
# Code to be written
```

---

**Go deeper:** [Python Browser Automation Cookbook](https://gum.co/python-browser-automation-cookbook?ref={slug}) covers {brief.get('goal', 'this topic').lower()}.
"""

        if dry_run:
            print(f"  Would create: {target.name} ({len(content)} chars)")
        else:
            target.write_text(content, encoding="utf-8")
            print(f"  Created: {target.name} ({len(content)} chars)")
        created.append(target)

    return created


# ──────────────────────────────────────────────
# 4. Outline stage — brief -> structured outline
# ──────────────────────────────────────────────


def write_outline(brief: dict, mapping: dict) -> str:
    """Generate a structured outline from a brief, preserving human editorial judgment."""
    website_concept = map_concept(brief["primary_concept"], mapping)
    pain_points = brief.get("pain_points", [])
    secondary = brief.get("secondary_concepts", [])
    mapped_secondary = [map_concept(c, mapping) for c in secondary]

    lines = [
        f"# Outline: {brief['title']}",
        "",
        f"**Audience:** {brief.get('audience', 'intermediate')}",
        f"**Primary concept:** {website_concept}",
        f"**Related concepts:** {', '.join(mapped_secondary) if mapped_secondary else 'None'}",
        f"**Target length:** {brief.get('target_length', 1500)} words",
        f"**CTA:** {brief.get('cta', 'None specified')}",
        "",
        "## Pain points to address",
    ]
    for pp in pain_points:
        lines.append(f"- {pp}")
    if not pain_points:
        lines.append("- (None specified)")

    lines.extend([
        "",
        "## Suggested structure",
        "",
        "### 1. Hook",
        "[Write an opening that ties to one of the pain points above]",
        "",
        "### 2. The problem (concrete example)",
        "[Show the error/issue with real code]",
        "",
        "### 3. Why it happens",
        "[Explain root cause — see HPF problem ontology]",
        "",
        "### 4. The solution",
        "[Step-by-step fix with code]",
        "",
        "### 5. Trade-offs / alternatives",
        "[When this approach works and when it doesn't]",
        "",
        "### 6. CTA",
        f"[Link to Gumroad with ?ref={brief['id']}]",
        "",
        "## Editorial notes",
        "",
        "- **Hook candidates:** " + "; ".join(pain_points[:3]) if pain_points else "- **Hook candidates:** (none suggested)",
        "- **Internal links:** " + ", ".join([f"/concepts/{c}" for c in [website_concept] + mapped_secondary]),
        "- **Slug:** " + brief["id"],
        "",
        "---",
        "",
        "*Generated from HPF brief. Human judgment required on structure, examples, and tone.*",
    ])

    return "\n".join(lines)


def scaffold_outlines(pkg: dict, mapping: dict, dry_run: bool = False) -> list[Path]:
    """Generate outline markdown files instead of full drafts."""
    outlines_dir = REPO_ROOT / "articles" / "outlines"
    outlines_dir.mkdir(parents=True, exist_ok=True)
    created = []

    for brief in pkg.get("briefs", []):
        slug = brief["id"]
        target = outlines_dir / f"{slug}.md"
        if target.exists():
            print(f"  Skip (exists): {target.name}")
            continue

        content = write_outline(brief, mapping)

        if dry_run:
            print(f"  Would create outline: {target.name} ({len(content)} chars)")
        else:
            target.write_text(content, encoding="utf-8")
            print(f"  Created outline: {target.name} ({len(content)} chars)")
        created.append(target)

    return created


# ──────────────────────────────────────────────
# 5. Problem MDX generation
# ──────────────────────────────────────────────


def write_problem_mdx(pkg: dict, mapping: dict, dry_run: bool = False) -> list[Path]:
    """Generate problem MDX files for the website from packaged problems."""
    problems_dir = REPO_ROOT / "website-next" / "content" / "problems"
    problems_dir.mkdir(parents=True, exist_ok=True)
    created = []

    for problem in pkg.get("problems", []):
        slug = problem["id"]
        target = problems_dir / f"{slug}.mdx"
        if target.exists():
            print(f"  Skip (exists): {target.name}")
            continue

        website_concept = map_concept(problem["primary_concept"], mapping)
        related_concepts = [map_concept(c, mapping) for c in problem.get("related_concepts", [])]

        aliases = [a["text"] for a in problem.get("aliases", [])]
        all_patterns = list(dict.fromkeys(problem.get("error_patterns", []) + aliases))

        content = f"""---
id: "{slug}"
title: "{problem['title']}"
error_patterns: {json.dumps(all_patterns)}
severity: "{problem.get('severity', 'common')}"
concept: "{website_concept}"
description: "{problem.get('root_cause', problem.get('title', ''))[:160]}"
---

{problem.get('root_cause', 'Root cause to be filled.')}

### Recovery

{problem.get('recovery_guide', 'Recovery steps to be filled.')}

### Recommendation

{problem.get('recommendation', 'Production recommendation to be filled.')}
"""

        if dry_run:
            print(f"  Would create: {target.name}")
        else:
            target.write_text(content, encoding="utf-8")
            print(f"  Created: {target.name}")
        created.append(target)

    return created


# ──────────────────────────────────────────────
# 5. Manifest generation — derived from handoff, not hand-edited
# ──────────────────────────────────────────────


def generate_manifest(pkg: dict, mapping: dict, dry_run: bool = False) -> Path | None:
    """Generate articles/json/manifest.json from the KnowledgePackage.

    Source of truth is the KnowledgePackage, not the manifest.
    Manifest is always derived — never hand-edited.

    Legacy entries (existing in draft/ but not yet in the handoff) are
    preserved to avoid losing manually created content during schema
    evolution. Once all legacy articles have corresponding briefs in
    HPF, this fallback becomes unnecessary.
    """
    manifest_path = REPO_ROOT / "articles" / "json" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing manifest for legacy preservation
    existing_entries = {}
    if manifest_path.exists():
        existing_entries = {e["slug"]: e for e in json.loads(manifest_path.read_text(encoding="utf-8"))}

    entries = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    seen_slugs = set()

    # 1. Handoff-derived entries (source of truth)
    for brief in pkg.get("briefs", []):
        slug = brief["id"]
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        website_concept = map_concept(brief["primary_concept"], mapping)
        related = [map_concept(c, mapping) for c in brief.get("secondary_concepts", [])]
        all_concepts = [website_concept] + [c for c in related if c != website_concept]
        all_concepts = list(dict.fromkeys(all_concepts))

        pain_points = brief.get("pain_points", [])
        description = brief.get("goal", brief["title"])
        if pain_points:
            description = f"{description} Covers: {', '.join(pain_points)}."

        tags = ["nodriver", "python", "browser-automation"]
        if website_concept not in tags:
            tags.append(website_concept)
        if brief.get("audience") == "advanced":
            tags.append("advanced")

        platforms = ["website"]
        if brief.get("cta"):
            platforms.append("devto")

        entries.append({
            "slug": slug,
            "title": brief["title"],
            "description": description,
            "concepts": all_concepts,
            "tags": tags,
            "date": today,
            "platforms": platforms,
        })

    # 2. Legacy entries (exist in draft/ but not yet in handoff)
    #    Parse frontmatter directly from draft files as fallback
    import re as _re
    drafts_dir = REPO_ROOT / "articles" / "draft"
    legacy_count = 0
    if drafts_dir.is_dir():
        for draft_file in sorted(drafts_dir.glob("*.md")):
            slug = draft_file.stem
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            # Prefer existing manifest entry if available
            if slug in existing_entries:
                entries.append(existing_entries[slug])
                legacy_count += 1
                continue

            # Parse frontmatter from the draft file itself
            content = draft_file.read_text(encoding="utf-8")
            frontmatter = {}
            parts = content.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split("\n"):
                    colon_idx = line.find(":")
                    if colon_idx > 0:
                        key = line[:colon_idx].strip()
                        val = line[colon_idx + 1:].strip().strip('"').strip("'")
                        if val.startswith("[") and val.endswith("]"):
                            val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
                        frontmatter[key] = val

            legacy_concepts = frontmatter.get("concepts", frontmatter.get("tags", [website_concept])) if isinstance(frontmatter.get("concepts", []), list) else [frontmatter.get("concepts", "")]
            if isinstance(legacy_concepts, str):
                legacy_concepts = [c.strip() for c in legacy_concepts.replace("[","").replace("]","").split(",") if c.strip()]

            entries.append({
                "slug": slug,
                "title": frontmatter.get("title", slug.replace("-", " ").title()),
                "description": frontmatter.get("description", ""),
                "concepts": legacy_concepts if isinstance(legacy_concepts, list) else [legacy_concepts],
                "tags": frontmatter.get("tags", ["nodriver", "python"]),
                "date": frontmatter.get("date", today),
                "platforms": frontmatter.get("platforms", ["website"]),
            })
            legacy_count += 1

    if legacy_count:
        print(f"  (Preserved {legacy_count} legacy entries not yet in handoff)")

    # Wrap with provenance metadata
    manifest = {
        "_meta": {
            "generated": True,
            "generator": "consume_handoff.py",
            "knowledge_package_version": pkg.get("producer_version", "?"),
            "schema_version": pkg.get("schema_version", "?"),
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "entry_count": len(entries),
        },
        "articles": entries,
    }

    if dry_run:
        print(f"  Would write manifest.json with {len(entries)} entries")
        for e in entries:
            print(f"    - {e['slug']}: {e['title']}")
        return None

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"  Wrote manifest.json with {len(entries)} entries")
    return manifest_path


# ──────────────────────────────────────────────
# 6. Feedback generation — domain-structured, richer payload
# ──────────────────────────────────────────────


def generate_feedback(
    source: str,
    signal_type: str,
    payload: dict,
    domain: str = "publisher",
    out_dir: str | None = None,
) -> Path:
    """Generate a feedback record for HPF.

    Publishing tools call this when they discover:
    - New pain points from comments
    - Concept gaps from search queries
    - High-performing article topics
    - Missing error patterns

    Records store domain/source/channel inside the JSON metadata rather
    than in directory structure, keeping the layout flat and flexible.
    """
    feedback_dir = Path(out_dir) if out_dir else REPO_ROOT / "knowledge" / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "id": f"{domain}-{signal_type}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "source": source,
        "domain": domain,
        "domain_hierarchy": {
            "primary": domain,
            "medium": source,
            "channel": signal_type,
        },
        "signal_type": signal_type,
        "payload": payload,
        "received": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "processed": False,
        "notes": None,
    }

    out_path = feedback_dir / f"{record['id']}.json"
    out_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"Feedback written: {out_path}")
    return out_path


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Consume HPF KnowledgePackage")
    parser.add_argument("handoff", help="Path to KnowledgePackage JSON file")
    parser.add_argument("--scaffold", action="store_true", help="Scaffold articles from briefs into draft/")
    parser.add_argument("--outline", action="store_true", help="Generate structured outlines (not full drafts)")
    parser.add_argument("--problems", action="store_true", help="Generate problem MDX files")
    parser.add_argument("--manifest", action="store_true", help="Generate manifest.json from handoff")
    parser.add_argument("--validate-only", action="store_true", help="Run quality gate and exit")
    parser.add_argument("--strict", action="store_true", help="Promote orphan concept warnings to errors")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    handoff_path = Path(args.handoff)
    if not handoff_path.exists():
        print(f"Error: handoff file not found: {handoff_path}")
        sys.exit(1)

    pkg = json.loads(handoff_path.read_text(encoding="utf-8"))
    mapping = load_concept_map()

    print(f"Consuming KnowledgePackage")
    check_compatibility(pkg)
    print(f"  Concepts: {len(pkg.get('concepts', []))}")
    print(f"  Problems: {len(pkg.get('problems', []))}")
    print(f"  Briefs:   {len(pkg.get('briefs', []))}")
    print()

    # Quality Gate — always runs
    print("Quality Gate:" + (" (strict)" if args.strict else ""))
    errors = validate_package(pkg, mapping, strict=args.strict)
    if errors:
        print("  FAILED:")
        for e in errors:
            print(f"    - {e}")
        print()
        print("  Package rejected. Fix errors above and regenerate.")
        sys.exit(1)
    print("  PASSED")
    print()

    if args.validate_only:
        print("Package valid. Exiting (--validate-only).")
        return

    if args.outline:
        print("Generating outlines from briefs:")
        scaffold_outlines(pkg, mapping, dry_run=args.dry_run)
        print()

    if args.scaffold:
        print("Scaffolding articles from briefs:")
        scaffold_articles(pkg, mapping, dry_run=args.dry_run)
        print()

    if args.problems:
        print("Writing problem MDX files:")
        write_problem_mdx(pkg, mapping, dry_run=args.dry_run)
        print()

    if args.manifest:
        print("Generating manifest.json from handoff:")
        generate_manifest(pkg, mapping, dry_run=args.dry_run)
        print()

    if not args.scaffold and not args.problems and not args.outline and not args.manifest:
        print("No action specified. Use --scaffold, --outline, and/or --problems.")
        print()
        print("Available briefs:")
        for b in pkg.get("briefs", []):
            mapped = map_concept(b["primary_concept"], mapping)
            print(f"  [{b['id']}] {b['title']} -> concept '{mapped}' (CTA: {b.get('cta', 'none')})")
        print()
        print("Available problems:")
        for p in pkg.get("problems", []):
            mapped = map_concept(p["primary_concept"], mapping)
            severity = p.get("severity", "common")
            print(f"  [{p['id']}] [{severity}] {p['title']} -> concept '{mapped}'")


if __name__ == "__main__":
    main()
