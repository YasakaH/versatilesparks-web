"""Run comparison (diff) engine.

The killer feature: compare two agent runs to find:
- Different tool selections
- Different decision paths
- State changes
- Performance regressions

This is "git diff for AI agents."
"""

from typing import Optional
from .events import Run, Event


def diff_runs(run_a: Run, run_b: Run) -> dict:
    """Compare two runs and return structured differences."""
    result = {
        "run_a_id": run_a.run_id,
        "run_b_id": run_b.run_id,
        "overall": "same",
        "differences": [],
        "stats": {},
    }

    # Compare event counts
    if len(run_a.events) != len(run_b.events):
        result["differences"].append({
            "type": "event_count",
            "a": len(run_a.events),
            "b": len(run_b.events),
            "description": f"Different number of events: {len(run_a.events)} vs {len(run_b.events)}",
        })

    # Compare event by event
    min_events = min(len(run_a.events), len(run_b.events))
    for i in range(min_events):
        evt_a = run_a.events[i]
        evt_b = run_b.events[i]
        event_diffs = _diff_events(evt_a, evt_b, i)
        result["differences"].extend(event_diffs)

    # Summary stats
    result["stats"] = {
        "a_events": len(run_a.events),
        "b_events": len(run_b.events),
        "a_errors": sum(1 for e in run_a.events if e.event_type == "error"),
        "b_errors": sum(1 for e in run_b.events if e.event_type == "error"),
        "a_duration_ms": sum(e.duration_ms or 0 for e in run_a.events),
        "b_duration_ms": sum(e.duration_ms or 0 for e in run_b.events),
        "changes": len(result["differences"]),
    }

    if result["differences"]:
        result["overall"] = "different"

    return result


def _diff_events(a: Event, b: Event, index: int) -> list[dict]:
    """Compare two events at the same sequence position."""
    diffs = []

    if a.event_type != b.event_type:
        diffs.append({
            "type": "event_type",
            "sequence": index,
            "a": a.event_type,
            "b": b.event_type,
            "description": f"Step {index + 1}: event type changed from '{a.event_type}' to '{b.event_type}'",
        })
        return diffs  # Stop comparing; types are different

    if a.name != b.name:
        diffs.append({
            "type": "tool_name",
            "sequence": index,
            "a": a.name,
            "b": b.name,
            "description": f"Step {index + 1}: tool changed from '{a.name}' to '{b.name}'",
        })

    if bool(a.error) != bool(b.error):
        diffs.append({
            "type": "error_presence",
            "sequence": index,
            "a": a.error,
            "b": b.error,
            "description": f"Step {index + 1}: error presence differs",
        })
    elif a.error and b.error and a.error != b.error:
        diffs.append({
            "type": "error_message",
            "sequence": index,
            "a": a.error,
            "b": b.error,
            "description": f"Step {index + 1}: error message differs",
        })

    if a.duration_ms and b.duration_ms:
        ratio = a.duration_ms / b.duration_ms if b.duration_ms > 0 else 0
        if ratio > 2.0 or ratio < 0.5:
            diffs.append({
                "type": "duration",
                "sequence": index,
                "a_ms": a.duration_ms,
                "b_ms": b.duration_ms,
                "description": f"Step {index + 1}: duration changed {a.duration_ms:.0f}ms → {b.duration_ms:.0f}ms ({ratio:.1f}x)",
            })

    return diffs


def format_diff_text(diff: dict) -> str:
    """Format a diff result as human-readable text."""
    lines = []
    lines.append(f"Run Comparison: {diff['run_a_id']} vs {diff['run_b_id']}")
    lines.append(f"Result: {diff['overall']}")
    lines.append("")

    if diff["differences"]:
        lines.append(f"Changes detected: {len(diff['differences'])}")
        lines.append("-" * 40)
        for d in diff["differences"]:
            lines.append(f"  • {d.get('description', 'Unknown change')}")
        lines.append("")

    stats = diff.get("stats", {})
    lines.append("Stats:")
    lines.append(f"  Events:  {stats.get('a_events', 0)} → {stats.get('b_events', 0)}")
    lines.append(f"  Errors:  {stats.get('a_errors', 0)} → {stats.get('b_errors', 0)}")
    lines.append(f"  Duration: {stats.get('a_duration_ms', 0):.0f}ms → {stats.get('b_duration_ms', 0):.0f}ms")
    lines.append(f"  Changes: {stats.get('changes', 0)}")

    return "\n".join(lines)
