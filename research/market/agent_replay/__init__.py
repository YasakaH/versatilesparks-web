"""Agent Replay — Record, Replay, and Understand AI Agent Actions.

Record every agent action, tool call, and LLM decision as structured
evidence. Replay runs in a local viewer. Compare runs to find regressions.

Usage:
    from agent_replay import record, record_run

    @record("search")
    def search_products(query):
        ...
    
    with record_run(agent_name="agent", goal="Find deals") as rec:
        result = search_products("laptops")
"""

from .core.recorder import Recorder, record, record_run, get_recorder
from .core.events import Run, Event, AgentInfo
from .core.receipt import run_to_json, json_to_run, load_run, save_run
from .core.storage import save, load, list_runs, load_path, delete_run
from .core.diff import diff_runs, format_diff_text
from .core.report import generate_report, report_to_file

__version__ = "0.1.0"
