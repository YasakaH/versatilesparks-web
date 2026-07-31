"""Framework adapters for Agent Replay.

Each adapter captures events from a specific AI agent framework
and translates them into the core EPR format.
"""

from .openai import trace_openai
