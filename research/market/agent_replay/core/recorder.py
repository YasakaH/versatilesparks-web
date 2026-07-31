"""Core Recorder — Captures events during agent execution.

The recorder wraps agent function calls, LLM invocations, and tool
executions to produce a structured Run with Events.
"""

import functools
import time
import traceback
from typing import Any, Callable, Optional
from .events import Event, Run


class Recorder:
    """Captures events for one agent run.

    Usage:
        recorder = Recorder("my-agent", model="gpt-4")
        recorder.start("Process refund")
        # ... agent does things, each recorded via record_event() or @record
        recorder.finish()
    """

    def __init__(self, agent_name: str = "", model: str = ""):
        self.run = Run.create(agent_name=agent_name, model=model)
        self._active = True

    def start(self, goal: str = ""):
        """Begin recording a run."""
        self.run.goal = goal
        self.run.status = "running"
        return self

    def record(self, name: str, event_type: str = "tool_call",
               input: Any = None, output: Any = None,
               state_before: dict = None, state_after: dict = None,
               error: Optional[str] = None, duration_ms: float = None,
               artifacts: list[str] = None) -> Event:
        """Record a single event."""
        evt = Event.create(
            event_type=event_type,
            name=name,
            input=input,
            output=output,
            state_before=state_before or {},
            state_after=state_after or {},
            error=error,
            duration_ms=duration_ms,
            artifacts=artifacts or [],
        )
        self.run.add_event(evt)
        return evt

    def error_event(self, name: str, error: str, input: Any = None):
        """Record a failure event."""
        return self.record(name=name, event_type="error", input=input, error=error)

    def finish(self, status: str = "completed", summary: str = ""):
        """End recording."""
        self.run.completed_at = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat()
        self.run.status = status
        self.run.summary = summary or f"{len(self.run.events)} events recorded"
        self._active = False
        return self.run

    def wrap(self, name: str = ""):
        """Decorator: wrap a function call with recording.

        @recorder.wrap("process_payment")
        def process_payment(order_id):
            ...
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                event_name = name or func.__name__
                start = time.time()
                state_before = {"args": str(args)[:200], "kwargs": str(kwargs)[:200]}
                try:
                    result = func(*args, **kwargs)
                    duration = (time.time() - start) * 1000
                    self.record(
                        name=event_name,
                        event_type="tool_call",
                        input={"args": str(args)[:200], "kwargs": str(kwargs)[:200]},
                        output=str(result)[:500],
                        state_before=state_before,
                        duration_ms=duration,
                    )
                    return result
                except Exception as e:
                    duration = (time.time() - start) * 1000
                    self.record(
                        name=event_name,
                        event_type="error",
                        input={"args": str(args)[:200], "kwargs": str(kwargs)[:200]},
                        error=f"{type(e).__name__}: {e}",
                        state_before=state_before,
                        duration_ms=duration,
                    )
                    raise
            return wrapper
        return decorator


# Global default recorder for the @record decorator
_default_recorder: Optional[Recorder] = None


def get_recorder() -> Optional[Recorder]:
    """Get the active recorder, or None if outside a recording context."""
    return _default_recorder


def record(func_or_name=None):
    """Decorator or wrapper to record a function call.

    Usage:
        @record
        def my_function(...):
            ...

        @record("custom_name")
        def my_function(...):
            ...
    """
    if callable(func_or_name):
        # @record without arguments
        @functools.wraps(func_or_name)
        def wrapper(*args, **kwargs):
            rec = get_recorder()
            if rec is None:
                return func_or_name(*args, **kwargs)
            return rec.wrap(func_or_name.__name__)(func_or_name)(*args, **kwargs)
        return wrapper
    else:
        # @record("name")
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                rec = get_recorder()
                if rec is None:
                    return func(*args, **kwargs)
                name = func_or_name or func.__name__
                return rec.wrap(name)(func)(*args, **kwargs)
            return wrapper
        return decorator


class record_run:
    """Context manager + decorator for recording an agent run.

    Usage:
        with record_run(agent_name="support-agent", goal="Refund customer") as rec:
            result = my_agent()
            # Everything is recorded automatically
    """

    def __init__(self, agent_name: str = "", model: str = "", goal: str = ""):
        self.recorder = Recorder(agent_name=agent_name, model=model)
        self.recorder.start(goal=goal)
        self._previous_recorder = None

    def __enter__(self) -> Recorder:
        global _default_recorder
        self._previous_recorder = _default_recorder
        _default_recorder = self.recorder
        return self.recorder

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _default_recorder
        _default_recorder = self._previous_recorder
        if exc_type:
            self.recorder.finish(status="failed", summary=str(exc_val))
        else:
            self.recorder.finish()
