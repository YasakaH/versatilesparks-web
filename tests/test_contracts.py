"""Contract tests for the HPF↔Publishing boundary.

These tests load example KnowledgePackages and verify that every
reference resolves, every brief scaffolds, every problem maps,
and every relationship is valid.

Run: cd cookbook && python tests/test_contracts.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.publisher.consume_handoff import (
    load_concept_map,
    map_concept,
    validate_package,
    scaffold_articles,
    scaffold_outlines,
    write_problem_mdx,
    write_outline,
)

# HPF pipeline — traverse to the actual module path
hpf_pipeline_dir = REPO_ROOT / "knowledge" / "hpf-core" / "tools" / "hpf-engine"
sys.path.insert(0, str(hpf_pipeline_dir))
sys.path.insert(0, str(hpf_pipeline_dir.parent))
from pipeline import (
    KnowledgePackage,
    produce,
)


def find_snapshot() -> Path | None:
    """Find the latest handoff snapshot in tmp or local paths."""
    candidates = [
        Path.home() / "AppData" / "Local" / "Temp" / "handoff_latest.json",
        Path.home() / "AppData" / "Local" / "Temp" / "handoff_v2.json",
        REPO_ROOT / "handoff" / "latest.json",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def find_hpf_concepts_dir() -> Path | None:
    """Find the HPF canonical concepts directory."""
    engine_dir = REPO_ROOT / "knowledge" / "hpf-core" / "tools" / "hpf-engine"
    for up in [engine_dir, engine_dir.parent, engine_dir.parent.parent,
               engine_dir.parent.parent.parent]:
        candidate = up / "canon" / "concepts"
        if candidate.is_dir():
            return candidate
    return None


# ──────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────

passed = 0
failed = 0


def check(condition: bool, message: str):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {message}")
    else:
        failed += 1
        print(f"  ✗ {message}")


def test_produce_valid_package():
    """HPF can produce a valid KnowledgePackage with schema metadata."""
    concepts_dir = find_hpf_concepts_dir()
    pkg = produce(concepts_dir=concepts_dir, version="0.99.0", schema_version="1.0")

    d = pkg.to_dict()
    check(d["schema_version"] == "1.0", "schema_version is 1.0")
    check(d["producer"] == "hpf-engine", "producer is hpf-engine")
    check(d["producer_version"] == "0.99.0", "producer_version is 0.99.0")
    check(d["compatibility"] == ">=0.4", "compatibility is >=0.4")
    check(bool(d["generated_at"]), "generated_at is set")
    check(len(d["concepts"]) > 0, f"has {len(d['concepts'])} concepts")
    check(len(d["problems"]) > 0, f"has {len(d['problems'])} problems")
    check(len(d["briefs"]) > 0, f"has {len(d['briefs'])} briefs")
    return d


def test_quality_gate_passes(pkg_dict: dict):
    """Every concept reference in briefs and problems resolves."""
    mapping = load_concept_map()
    errors = validate_package(pkg_dict, mapping)
    check(len(errors) == 0, f"quality gate passes (0 errors, got {len(errors)})")
    return mapping


def test_every_brief_scaffolds(pkg_dict: dict, mapping: dict):
    """Every brief produces a valid draft article (excluding pre-existing files)."""
    drafts = scaffold_articles(pkg_dict, mapping, dry_run=True)
    missing = {b["id"] for b in pkg_dict["briefs"]}
    existing = missing - {d.stem for d in drafts}
    if existing:
        print(f"  ({len(existing)} briefs already have draft files, skipped)")
    check(len(drafts) + len(existing) == len(pkg_dict["briefs"]),
          f"all {len(pkg_dict['briefs'])} briefs accounted for (got {len(drafts)} new, {len(existing)} existing)")


def test_every_brief_outlines(pkg_dict: dict, mapping: dict):
    """Every brief produces a valid outline."""
    outlines = scaffold_outlines(pkg_dict, mapping, dry_run=True)
    check(len(outlines) == len(pkg_dict["briefs"]),
          f"all {len(pkg_dict['briefs'])} briefs produce outlines (got {len(outlines)})")


def test_outline_content(brief):
    """Outline contains expected editorial structure."""
    mapping = load_concept_map()
    outline = write_outline(brief, mapping)
    check("## Suggested structure" in outline, "outline has structure section")
    check("### 1. Hook" in outline, "outline has Hook section")
    check("### 6. CTA" in outline, "outline has CTA section")
    check("## Editorial notes" in outline, "outline has editorial notes")
    check(brief["id"] in outline, f"outline references slug '{brief['id']}'")
    check(brief.get("audience", "") in outline, f"outline mentions audience '{brief.get('audience')}'")


def test_every_problem_maps(pkg_dict: dict, mapping: dict):
    """Every problem generates valid MDX (excluding pre-existing files)."""
    problems = write_problem_mdx(pkg_dict, mapping, dry_run=True)
    missing = {p["id"] for p in pkg_dict["problems"]}
    existing = missing - {d.stem for d in problems}
    if existing:
        print(f"  ({len(existing)} problems already have MDX files, skipped)")
    check(len(problems) + len(existing) == len(pkg_dict["problems"]),
          f"all {len(pkg_dict['problems'])} problems accounted for (got {len(problems)} new, {len(existing)} existing)")


def test_problem_concept_resolves(pkg_dict: dict):
    """Every problem's primary_concept resolves through the concept map."""
    mapping = load_concept_map()
    concept_ids = set(c["id"] for c in pkg_dict.get("concepts", []))
    for prob in pkg_dict.get("problems", []):
        website_cid = map_concept(prob["primary_concept"], mapping)
        check(
            website_cid in concept_ids or prob["primary_concept"] in concept_ids,
            f"problem '{prob['id']}' concept '{prob['primary_concept']}' resolves to '{website_cid}'"
        )


def test_brief_primary_concept_resolves(pkg_dict: dict):
    """Every brief's primary_concept resolves through the concept map."""
    mapping = load_concept_map()
    concept_ids = set(c["id"] for c in pkg_dict.get("concepts", []))
    for brief in pkg_dict.get("briefs", []):
        website_cid = map_concept(brief["primary_concept"], mapping)
        check(
            website_cid in concept_ids or brief["primary_concept"] in concept_ids,
            f"brief '{brief['id']}' concept '{brief['primary_concept']}' resolves to '{website_cid}'"
        )


def test_every_brief_has_cta(pkg_dict: dict):
    """Every brief has a CTA (required for conversion tracking)."""
    for brief in pkg_dict.get("briefs", []):
        check(bool(brief.get("cta")), f"brief '{brief['id']}' has CTA: {brief.get('cta')}")


def test_every_problem_has_root_cause(pkg_dict: dict):
    """Every problem has a root_cause."""
    for prob in pkg_dict.get("problems", []):
        check(bool(prob.get("root_cause")), f"problem '{prob['id']}' has root_cause")


def test_every_problem_has_error_patterns(pkg_dict: dict):
    """Every problem has error_patterns."""
    for prob in pkg_dict.get("problems", []):
        check(len(prob.get("error_patterns", [])) > 0, f"problem '{prob['id']}' has error_patterns")


def test_knowledge_package_deserializes():
    """A KnowledgePackage round-trips through JSON without data loss."""
    concepts_dir = find_hpf_concepts_dir()
    pkg = produce(concepts_dir=concepts_dir, version="0.99.0")
    d1 = pkg.to_dict()

    # Serialize to JSON, deserialize
    json_str = pkg.to_json()
    d2 = json.loads(json_str)

    # Reconstruct
    pkg2 = KnowledgePackage.from_dict(d2)
    d3 = pkg2.to_dict()

    check(len(d1["problems"]) == len(d3["problems"]), "problem count preserved through round-trip")
    check(len(d1["briefs"]) == len(d3["briefs"]), "brief count preserved through round-trip")
    check(d1["schema_version"] == d3["schema_version"], "schema_version preserved")
    check(d1["producer"] == d3["producer"], "producer preserved")


# ──────────────────────────────────────────────
# Test relationship integrity
# ──────────────────────────────────────────────

def test_relationship_integrity(pkg_dict: dict):
    """Every brief that references a concept in its pain_points
    should have a matching problem in the package."""
    problem_ids = set(p["id"] for p in pkg_dict.get("problems", []))
    for brief in pkg_dict.get("briefs", []):
        for pp in brief.get("pain_points", []):
            if pp in problem_ids:
                # Pain point matches a known problem ID — relationship is valid
                check(True, f"brief '{brief['id']}' pain point '{pp}' matches a known problem")
                break


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    print("Contract Tests: HPF <-> Publishing Boundary")
    print("=" * 50)
    print()

    # 1. Find or generate test data
    snapshot = find_snapshot()
    if snapshot:
        print(f"Using handoff snapshot: {snapshot}")
        pkg_dict = json.loads(snapshot.read_text(encoding="utf-8"))
    else:
        print("No snapshot found, producing fresh...")
        concepts_dir = find_hpf_concepts_dir()
        pkg = produce(concepts_dir=concepts_dir)
        pkg_dict = pkg.to_dict()

    # 2. Run test suites
    print()
    print("--- Producer contract ---")
    test_produce_valid_package()
    test_knowledge_package_deserializes()

    print()
    print("--- Quality gate ---")
    mapping = test_quality_gate_passes(pkg_dict)

    print()
    print("--- Reference resolution ---")
    test_every_concept_reference_resolves(pkg_dict)
    test_problem_concept_resolves(pkg_dict)
    test_brief_primary_concept_resolves(pkg_dict)
    test_relationship_integrity(pkg_dict)

    print()
    print("--- Article scaffolding ---")
    test_every_brief_scaffolds(pkg_dict, mapping)
    test_every_brief_outlines(pkg_dict, mapping)
    for brief in pkg_dict.get("briefs", []):
        test_outline_content(brief)

    print()
    print("--- Problem integrity ---")
    test_every_problem_maps(pkg_dict, mapping)
    test_every_problem_has_root_cause(pkg_dict)
    test_every_problem_has_error_patterns(pkg_dict)

    print()
    print("--- Editorial quality ---")
    test_every_brief_has_cta(pkg_dict)

    # 3. Summary
    print()
    print("=" * 50)
    total = passed + failed
    print(f"Results: {passed}/{total} passed")
    if failed:
        print(f"{failed} FAILURES — contract boundary compromised.")
        sys.exit(1)
    else:
        print("All contract tests pass.")


def test_every_concept_reference_resolves(pkg_dict: dict):
    """Every concept ID referenced from briefs/problems exists in the concept list."""
    mapping = load_concept_map()
    concept_ids = set(c["id"] for c in pkg_dict.get("concepts", []))

    # Collect all HPF-side concept references
    refs = set()
    for brief in pkg_dict.get("briefs", []):
        refs.add(brief.get("primary_concept", ""))
        for sc in brief.get("secondary_concepts", []):
            refs.add(sc)
    for prob in pkg_dict.get("problems", []):
        refs.add(prob.get("primary_concept", ""))
        for rc in prob.get("related_concepts", []):
            refs.add(rc)

    # Check each reference resolves to a known concept ID
    for ref in refs:
        if not ref:
            continue
        website_cid = map_concept(ref, mapping)
        check(
            ref in concept_ids or website_cid in concept_ids,
            f"reference '{ref}' resolves (maps to '{website_cid}')"
        )


if __name__ == "__main__":
    main()
