"""03 — Compare two agent runs using the diff engine.

Demonstrates: programmatic run comparison and how to interpret the diff.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_replay import record_run, record, save, diff_runs, format_diff_text


@record("fetch_data")
def fetch_data(query):
    return {"results": [query, query * 2]}


@record("transform")
def transform(data, multiplier=2):
    return [x * multiplier for x in data["results"]]


def run_agent(dataset, multiplier=2):
    data = fetch_data(dataset)
    result = transform(data, multiplier)
    return {"output": result}


if __name__ == "__main__":
    with record_run(agent_name="etl-agent", goal="Transform data with multiplier=3") as _:
        run_agent(5, multiplier=3)

    with record_run(agent_name="etl-agent", goal="Transform data with multiplier=4") as _:
        run_agent(5, multiplier=4)

    runs = [_.run]

    print("=" * 50)
    print("AGENT REPLAY — RUN COMPARISON")
    print("=" * 50)
    print()
    print(f"Comparing {len(runs)} runs...")
    print()

    if len(runs) >= 2:
        diff = diff_runs(runs[0], runs[1])
        print(format_diff_text(diff))
    else:
        print("Need at least 2 runs to compare. Run this script twice.")
