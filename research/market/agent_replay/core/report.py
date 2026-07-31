"""Failure Report — Portable UGC artifact generator.

Generates a self-contained markdown report from one or more agent runs.
The report is designed to be pasted into GitHub issues, Discord, Reddit,
or bug trackers — turning every debugging session into distribution.
"""

from typing import Optional
from .events import Run, Event
from .diff import diff_runs, format_diff_text


def generate_report(
    run: Run,
    compare_run: Optional[Run] = None,
) -> str:
    """Generate a ready-to-paste markdown failure report.

    Args:
        run: The primary run to report on.
        compare_run: Optional second run for comparison (the killer feature).

    Returns:
        Markdown string ready for copy-paste.
    """
    lines = []
    NL = ""  # shorthand for blank line

    lines.append("## 🤖 Agent Failure Report")
    lines.append(NL)
    lines.append(f"**Agent:** `{run.agent.name}` ({run.agent.model})")
    lines.append(f"**Goal:** {run.goal}")
    lines.append(f"**Status:** {run.status}")
    lines.append(f"**Run ID:** `{run.run_id}`")
    lines.append(f"**Recorded:** {run.started_at}")
    lines.append(NL)

    # Summary stats
    total = len(run.events)
    errors_ev = [e for e in run.events if e.event_type == "error"]
    tool_calls = [e for e in run.events if e.event_type == "tool_call"]
    total_ms = sum(e.duration_ms or 0 for e in run.events)

    lines.append("### 📊 Summary")
    lines.append(NL)
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Events | {total} |")
    lines.append(f"| Tool calls | {len(tool_calls)} |")
    lines.append(f"| Errors | {len(errors_ev)} |")
    dur = f"{total_ms:.0f}ms"
    if total_ms > 1000:
        dur += f" ({total_ms/1000:.1f}s)"
    lines.append(f"| Duration | {dur} |")
    lines.append(NL)

    # Comparison (if requested)
    if compare_run is not None:
        lines.append("### 🔍 Run Comparison")
        lines.append(NL)
        lines.append(f"Comparing **{run.run_id[:8]}** vs **{compare_run.run_id[:8]}**")
        lines.append(NL)
        diff = diff_runs(run, compare_run)
        lines.append("```")
        lines.append(format_diff_text(diff))
        lines.append("```")
        lines.append(NL)

    # Timeline
    lines.append("### ⏱️ Execution Timeline")
    lines.append(NL)
    lines.append("| # | Type | Action | Duration | Error |")
    lines.append("|---|------|--------|----------|-------|")
    type_emoji = {
        "tool_call": "🔧", "llm_generation": "🧠", "decision": "⚡",
        "error": "❌", "state_change": "📦",
    }
    for i, evt in enumerate(run.events):
        emoji = type_emoji.get(evt.event_type, "•")
        dur = f"{evt.duration_ms:.0f}ms" if evt.duration_ms else "—"
        err = "✗" if evt.error else "✓"
        name = evt.name[:40] if evt.name else "—"
        lines.append(f"| {i+1} | {emoji} {evt.event_type} | {name} | {dur} | {err} |")

    if errors_ev:
        lines.append(NL)
        lines.append("### ❌ Errors")
        lines.append(NL)
        for evt in errors_ev:
            lines.append(f"- **{evt.name}**: {evt.error}")

    lines.append(NL)
    lines.append("---")
    lines.append(NL)
    lines.append("> 🛠️ [Agent Replay](https://github.com/varun-dce/agent-replay)"
                 " — Debug AI agents like you debug code.")
    lines.append(f"> `pip install agent-replay` • `agent-replay view {run.run_id}`")

    return "\n".join(lines)


def report_to_file(run, path, compare_run=None):
    """Write a failure report to a file."""
    md = generate_report(run, compare_run=compare_run)
    with open(path, "w") as f:
        f.write(md)
    return path
