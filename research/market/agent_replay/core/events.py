"""Agent Replay — Core Event Model.

The entire system reduces to capturing discrete events
that answer: "Why did my agent do that?"
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional
import uuid


@dataclass
class AgentInfo:
    """Information about the agent that performed the action."""
    name: str = "unknown"
    model: str = "unknown"
    version: str = ""


@dataclass
class Event:
    """A single recorded event in an agent execution.

    This is the atomic unit of Agent Replay. Every tool call,
    LLM generation, decision point, and failure produces one Event.
    """
    run_id: str = ""
    timestamp: str = ""
    sequence: int = 0

    event_type: str = "unknown"  # tool_call, llm_generation, decision, error, state_change

    # What
    name: str = ""
    input: Any = None
    output: Any = None

    # Context
    state_before: dict = field(default_factory=dict)
    state_after: dict = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: Optional[float] = None

    # Identity
    agent: AgentInfo = field(default_factory=AgentInfo)

    # Evidence artifacts (file paths, hashes, screenshots)
    artifacts: list[str] = field(default_factory=list)

    # For diffs — which parent event this is derived from
    parent_event: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["agent"] = asdict(self.agent) if isinstance(self.agent, AgentInfo) else self.agent
        return d

    @classmethod
    def create(cls, **kwargs) -> "Event":
        evt = cls(**kwargs)
        if not evt.run_id:
            evt.run_id = uuid.uuid4().hex[:12]
        if not evt.timestamp:
            evt.timestamp = datetime.now(timezone.utc).isoformat()
        return evt


@dataclass
class Run:
    """A complete agent run — a sequence of events."""
    run_id: str = ""
    agent: AgentInfo = field(default_factory=AgentInfo)
    goal: str = ""
    started_at: str = ""
    completed_at: str = ""
    events: list[Event] = field(default_factory=list)
    status: str = "running"  # running, completed, failed
    summary: Optional[str] = None

    def add_event(self, event: Event) -> Event:
        event.run_id = self.run_id
        event.sequence = len(self.events)
        event.agent = self.agent
        self.events.append(event)
        return event

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "agent": asdict(self.agent),
            "goal": self.goal,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "events": [e.to_dict() for e in self.events],
            "event_count": len(self.events),
            "summary": self.summary,
        }

    @classmethod
    def create(cls, agent_name="", model="", goal="") -> "Run":
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            run_id=uuid.uuid4().hex[:12],
            agent=AgentInfo(name=agent_name, model=model),
            goal=goal,
            started_at=now,
        )
