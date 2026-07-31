"""Agent Replay CLI — View, compare, and share agent run reports.

Usage:
    agent-replay list                # List all recorded runs
    agent-replay view <run_id>       # Open web viewer for a run
    agent-replay diff <a> <b>        # Compare two runs
    agent-replay report <run_id>     # Generate a failure report
    agent-replay report <a> <b>      # Generate a comparison report
    agent-replay info <run_id>       # Show run metadata
"""

import json
import sys
import os
import http.server
import socketserver
import webbrowser
import threading
from datetime import datetime

# Add parent to path so we can import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_replay import (
    list_runs, load, load_path, diff_runs, format_diff_text,
    generate_report, report_to_file,
)


def cmd_list(args):
    """List all recorded runs."""
    runs = list_runs()
    if not runs:
        print("No runs recorded yet.")
        print("Run a recorded agent, then run: agent-replay list")
        return

    print(f"{'RUN ID':<14} {'AGENT':<20} {'STATUS':<10} {'EVENTS':<8} {'GOAL'}")
    print("-" * 80)
    for r in runs:
        name = r.get("agent_name", "")[:18]
        status = r.get("status", "")[:8]
        events = r.get("event_count", 0)
        goal = r.get("goal", "")[:35]
        rid = r.get("run_id", "????")
        print(f"{rid:<14} {name:<20} {status:<10} {events:<8} {goal}")
    print(f"\n{len(runs)} runs total")


def cmd_view(args):
    """Open the web viewer for a run."""
    if not args:
        print("Usage: agent-replay view <run_id>")
        print("Run 'agent-replay list' to see available runs.")
        return

    run_id = args[0]
    run = load(run_id)
    if run is None:
        run = load_path(run_id)
    if run is None:
        print(f"Run '{run_id}' not found.")
        return

    port = 3456
    from agent_replay.viewer.serve import serve_run
    serve_run(run, port=port)


def cmd_diff(args):
    """Compare two runs."""
    if len(args) < 2:
        print("Usage: agent-replay diff <run_a> <run_b>")
        return

    run_a = load(args[0]) or load_path(args[0])
    run_b = load(args[1]) or load_path(args[1])

    if run_a is None:
        print(f"Run '{args[0]}' not found.")
        return
    if run_b is None:
        print(f"Run '{args[1]}' not found.")
        return

    diff = diff_runs(run_a, run_b)
    print(format_diff_text(diff))


def cmd_report(args):
    """Generate a portable markdown failure report.

    Usage:
        agent-replay report <run_id>           # Single-run report
        agent-replay report <a> <b>            # Comparison report
        agent-replay report <a> <b> --save     # Save to file
    """
    if not args:
        print("Usage: agent-replay report <run_id> [<run_id_b>] [--save]")
        return

    save_to_file = "--save" in args
    ids = [a for a in args if not a.startswith("--")]

    run_a = load(ids[0]) or load_path(ids[0])
    if run_a is None:
        print(f"Run '{ids[0]}' not found.")
        return

    run_b = None
    if len(ids) >= 2:
        run_b = load(ids[1]) or load_path(ids[1])
        if run_b is None:
            print(f"Run '{ids[1]}' not found.")
            return

    md = generate_report(run_a, compare_run=run_b)
    print(md)

    if save_to_file:
        fname = f"agent-failure-report-{run_a.run_id[:8]}.md"
        with open(fname, "w") as f:
            f.write(md)
        print(f"\nReport saved to: {fname}")


def cmd_info(args):
    """Show run metadata."""
    if not args:
        print("Usage: agent-replay info <run_id>")
        return

    run = load(args[0]) or load_path(args[0])
    if run is None:
        print(f"Run '{args[0]}' not found.")
        return

    print(f"Run ID:       {run.run_id}")
    print(f"Agent:        {run.agent.name} ({run.agent.model})")
    print(f"Goal:         {run.goal}")
    print(f"Started:      {run.started_at}")
    print(f"Completed:    {run.completed_at}")
    print(f"Status:       {run.status}")
    print(f"Events:       {len(run.events)}")
    print(f"Errors:       {sum(1 for e in run.events if e.event_type == 'error')}")
    print(f"Summary:      {run.summary}")


def main():
    if len(sys.argv) < 2:
        print("Agent Replay — Debug AI agents like you debug code.")
        print()
        print("Usage:")
        print("  agent-replay list                  List runs")
        print("  agent-replay view <run_id>         View a run")
        print("  agent-replay diff <a> <b>          Compare two runs")
        print("  agent-replay report <run_id>       Generate failure report")
        print("  agent-replay report <a> <b>        Generate comparison report")
        print("  agent-replay info <run_id>         Show run details")
        print()
        print("Record runs programmatically:")
        print("  from agent_replay import record_run, record")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "list": cmd_list,
        "view": cmd_view,
        "diff": cmd_diff,
        "report": cmd_report,
        "info": cmd_info,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        print("Available: list, view, diff, report, info")


if __name__ == "__main__":
    main()
