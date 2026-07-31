"""OpenAI API adapter — automatically trace GPT calls.

Captures: prompts, responses, tool calls, latency, failures.
"""

import time
from typing import Optional
from .. import get_recorder


def trace_openai(client):
    """Wrap an OpenAI client to automatically record API calls.

    Usage:
        from openai import OpenAI
        from agent_replay.openai import trace_openai

        client = trace_openai(OpenAI())
        response = client.chat.completions.create(...)
    """
    original_create = client.chat.completions.create

    def traced_create(*args, **kwargs):
        rec = get_recorder()
        if rec is None:
            return original_create(*args, **kwargs)

        start = time.time()
        input_data = {
            "model": kwargs.get("model", "unknown"),
            "messages": _summarize_messages(kwargs.get("messages", [])),
            "tools": len(kwargs.get("tools", [])),
            "temperature": kwargs.get("temperature"),
        }

        try:
            response = original_create(*args, **kwargs)

            # Extract tool calls if any
            tool_calls = []
            if response.choices and response.choices[0].message:
                msg = response.choices[0].message
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_calls = [
                        {"name": tc.function.name, "args": tc.function.arguments}
                        for tc in msg.tool_calls
                    ]

            output_data = {
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason if response.choices else None,
                "tool_calls": tool_calls,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
                    "completion_tokens": response.usage.completion_tokens if response.usage else None,
                } if response.usage else None,
            }

            duration = (time.time() - start) * 1000
            rec.record(
                name="openai_chat_completion",
                event_type="llm_generation",
                input=input_data,
                output=output_data,
                state_before={"model": kwargs.get("model")},
                state_after={"model": response.model},
                duration_ms=duration,
            )

            return response

        except Exception as e:
            duration = (time.time() - start) * 1000
            rec.record(
                name="openai_chat_completion",
                event_type="error",
                input=input_data,
                error=f"OpenAI API error: {e}",
                duration_ms=duration,
            )
            raise

    client.chat.completions.create = traced_create
    return client


def _summarize_messages(messages, max_chars=500):
    """Summarize messages for recording (don't store full prompts)."""
    summary = []
    total = 0
    for msg in messages[-5:]:  # Last 5 messages
        role = msg.get("role", "?")
        content = msg.get("content", "")
        if isinstance(content, str):
            snippet = content[:100]
        elif isinstance(content, list):
            snippet = f"[{len(content)} content parts]"
        else:
            snippet = str(content)[:100]
        summary.append({"role": role, "preview": snippet})
        total += len(str(content))
        if total > max_chars:
            summary.append({"note": f"truncated, total ~{total} chars"})
            break
    return summary
