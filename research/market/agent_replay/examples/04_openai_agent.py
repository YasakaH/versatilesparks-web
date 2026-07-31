"""04 — OpenAI agent with automatic tracing.

Demonstrates: trace_openai() wrapper that captures prompts, responses, and tool calls.

Requires: pip install openai
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_replay import record_run
from agent_replay.adapters import trace_openai


def search_knowledge_base(query):
    """Simulate a tool the agent calls."""
    db = {
        "pricing": "Our pricing starts at $49/month for the basic plan.",
        "refund": "Refunds are processed within 5-7 business days.",
        "hours": "We're open Monday-Friday, 9AM-6PM EST.",
    }
    return db.get(query.lower(), f"No information found for '{query}'")


if __name__ == "__main__":
    try:
        from openai import OpenAI
        client = trace_openai(OpenAI())
    except ImportError:
        print("This example requires: pip install openai")
        print("Skipping OpenAI demo — using simulated trace instead.")
        client = None

    # Trace the agent run
    with record_run(
        agent_name="knowledge-agent",
        model="gpt-4o-mini",
        goal="Answer customer question about refund policy"
    ) as rec:
        if client:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful support agent."},
                    {"role": "user", "content": "What's your refund policy?"},
                ],
            )
            answer = response.choices[0].message.content
        else:
            # Simulated trace for demonstration
            answer = search_knowledge_base("refund")
            rec.record(
                name="openai_chat_completion",
                event_type="llm_generation",
                input={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Refund policy?"}]},
                output={"model": "gpt-4o-mini", "content": answer[:100]},
                duration_ms=1234,
            )

        print(f"Agent response: {answer[:120]}...")

    print(f"\nView the trace: agent-replay view {rec.run.run_id}")
