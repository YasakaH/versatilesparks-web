"""Execution Proof Receipt (EPR) — Standard serialization format."""

import json
from datetime import datetime, timezone
from typing import Any, Optional
from .events import Run, Event, AgentInfo

EPR_VERSION = "0.1.0"


def serialize_run(run: Run) -> dict:
    return {
        "epr_version": EPR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run": run.to_dict(),
    }


def run_to_json(run: Run, indent: int = 2) -> str:
    return json.dumps(serialize_run(run), indent=indent, default=str)


def json_to_run(data: dict) -> Run:
    run_data = data.get("run", data)
    run = Run(
        run_id=run_data.get("run_id", ""),
        agent=AgentInfo(**run_data.get("agent", {})),
        goal=run_data.get("goal", ""),
        started_at=run_data.get("started_at", ""),
        completed_at=run_data.get("completed_at", ""),
        status=run_data.get("status", "unknown"),
        summary=run_data.get("summary"),
    )
    for evt_data in run_data.get("events", []):
        evt = Event(
            run_id=evt_data.get("run_id", run.run_id),
            timestamp=evt_data.get("timestamp", ""),
            sequence=evt_data.get("sequence", 0),
            event_type=evt_data.get("event_type", "unknown"),
            name=evt_data.get("name", ""),
            input=evt_data.get("input"),
            output=evt_data.get("output"),
            state_before=evt_data.get("state_before", {}),
            state_after=evt_data.get("state_after", {}),
            error=evt_data.get("error"),
            duration_ms=evt_data.get("duration_ms"),
            agent=AgentInfo(**evt_data.get("agent", {})),
            artifacts=evt_data.get("artifacts", []),
            parent_event=evt_data.get("parent_event"),
        )
        run.events.append(evt)
    return run


def load_run(path: str) -> Run:
    with open(path, "r") as f:
        data = json.load(f)
    return json_to_run(data)


def save_run(run: Run, path: str):
    with open(path, "w") as f:
        f.write(run_to_json(run))
