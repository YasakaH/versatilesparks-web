# Agent Replay

Debug AI agents like you debug code.

Your AI agent failed. The logs tell you what happened. They don't tell you *why*.

Agent Replay records every LLM call, tool call, decision, state change, and failure — then lets you replay the timeline and compare runs to find the root cause.

```python
pip install agent-replay
```

---

## Before Agent Replay

> "My agent worked yesterday. Today it failed. Why?"

Hours of log spelunking. Guessing what the model decided. No way to compare runs.

## After Agent Replay

Run comparison shows exactly what changed:

```
Step 3 changed:
  verify_payment()    ← yesterday's successful run
  refund()            ← today's failed run

Root cause:
  Agent skipped the authorization check.
```

30 seconds instead of 2 hours.

---

## How it works

Record with a context manager:

```python
from agent_replay import record_run

with record_run(agent_name="support-agent", goal="Refund customer") as rec:
    result = my_agent()
```

Or wrap individual functions:

```python
from agent_replay import record

@record("search_database")
def search(query):
    return db.query(query)
```

View the replay:

```bash
agent-replay list                # List all recorded runs
agent-replay view <run_id>       # Open interactive timeline viewer
agent-replay diff <a> <b>        # Compare two runs
```

---

## What it captures

| Type | Example |
|------|---------|
| LLM calls | prompt, response, model, latency |
| Tool calls | function name, input, output, duration |
| Decisions | what the agent chose and why |
| State changes | before/after snapshots |
| Errors | failure messages, stack context |

Every run produces an **Execution Proof Receipt** — a portable JSON document that captures the full execution trace.

---

## Example: Debugging a failed agent

```python
from agent_replay import record_run, record

with record_run(agent_name="order-agent", goal="Process refund") as rec:

    @record
    def check_customer(id):
        return {"status": "active", "id": id}

    @record
    def refund(amount):
        raise ValueError("Insufficient balance")

    try:
        check_customer("C-42")
        refund(100)
    except Exception as e:
        print(f"Agent failed: {e}")
```

Then:

```bash
agent-replay list
agent-replay view <run_id>
```

The viewer shows the exact failure point with input, output, and error context.

---

## Project status

**v0.1** — Alpha. Open source. No cloud. No accounts. No billing.

```python
pip install agent-replay
```

---

## What's next

- [ ] Agent Replay for LangGraph
- [ ] Agent Replay for Browser-use
- [ ] Agent Replay for CrewAI
- [ ] Cloud storage (optional)
- [ ] Team collaboration

Priorities driven by community feedback.

---

## License

MIT
