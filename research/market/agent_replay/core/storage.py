"""Local file-based storage for agent runs.

All runs are stored as individual JSON files under ~/.agent-replay/runs/.
No database. No accounts. No cloud.
"""

import json
import os
from datetime import datetime
from typing import Optional
from .events import Run
from .receipt import save_run, load_run

DEFAULT_DIR = os.path.expanduser("~/.agent-replay/runs")


def _ensure_dir(path: str = None):
    path = path or DEFAULT_DIR
    os.makedirs(path, exist_ok=True)
    return path


def _run_path(run_id: str, base_dir: str = None) -> str:
    base = base_dir or DEFAULT_DIR
    return os.path.join(base, f"run_{run_id}.json")


def save(run: Run, base_dir: str = None) -> str:
    """Save a run to disk. Returns the file path."""
    path = _run_path(run.run_id, base_dir)
    _ensure_dir(os.path.dirname(path))
    # Ensure completed_at is set
    if not run.completed_at:
        run.completed_at = datetime.now().isoformat()
    save_run(run, path)
    return path


def load(run_id: str, base_dir: str = None) -> Optional[Run]:
    """Load a run by run_id."""
    path = _run_path(run_id, base_dir)
    if not os.path.exists(path):
        return None
    return load_run(path)


def load_path(filepath: str) -> Optional[Run]:
    """Load a run from a specific file path."""
    if not os.path.exists(filepath):
        return None
    return load_run(filepath)


def list_runs(base_dir: str = None) -> list[dict]:
    """List all saved runs with metadata (no event bodies)."""
    base = base_dir or DEFAULT_DIR
    runs = []
    if not os.path.exists(base):
        return runs
    for fname in sorted(os.listdir(base), reverse=True):
        if fname.startswith("run_") and fname.endswith(".json"):
            try:
                with open(os.path.join(base, fname)) as f:
                    data = json.load(f)
                run_data = data.get("run", data)
                runs.append({
                    "run_id": run_data.get("run_id", fname),
                    "agent_name": run_data.get("agent", {}).get("name", ""),
                    "goal": run_data.get("goal", ""),
                    "started_at": run_data.get("started_at", ""),
                    "status": run_data.get("status", ""),
                    "event_count": run_data.get("event_count", 0),
                    "file": fname,
                })
            except (json.JSONDecodeError, KeyError):
                runs.append({"run_id": fname, "error": "corrupt"})
    return runs


def delete_run(run_id: str, base_dir: str = None) -> bool:
    """Delete a saved run."""
    path = _run_path(run_id, base_dir)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
