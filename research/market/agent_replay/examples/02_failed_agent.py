"""02 — Intentionally broken agent with replay.

Demonstrates: debugging a failure using Agent Replay.
This agent has a bug: it skips the verification step.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_replay import record_run, record


# ── Version 1: Correct agent (works) ──

@record("lookup_customer")
def lookup_customer(customer_id):
    return {"id": customer_id, "status": "active", "balance": 500}


@record("verify_payment")
def verify_payment(customer_id, amount):
    customer = lookup_customer(customer_id)
    if customer["balance"] < amount:
        return {"verified": False, "reason": "Insufficient balance"}
    return {"verified": True}


@record("process_refund")
def process_refund(customer_id, amount):
    return {"refund_id": "RFN-" + os.urandom(3).hex().upper(), "amount": amount}


@record("send_notification")
def send_notification(customer_id, message):
    return {"sent": True, "to": customer_id, "message": message}


def run_correct_agent(customer_id, amount):
    """Correct agent flow: verify → refund → notify."""
    customer = lookup_customer(customer_id)
    verification = verify_payment(customer_id, amount)
    if not verification["verified"]:
        return {"status": "failed", "reason": verification["reason"]}
    refund = process_refund(customer_id, amount)
    notification = send_notification(customer_id, f"Refund of ${amount} processed")
    return {"status": "completed", "refund": refund}


# ── Version 2: Broken agent (skips verification — the bug!) ──

def run_broken_agent(customer_id, amount):
    """Broken agent flow: refund BEFORE verification — the bug!"""
    customer = lookup_customer(customer_id)
    # BUG: called refund BEFORE verification
    refund = process_refund(customer_id, amount)
    # Verification happens too late — money already sent
    verification = verify_payment(customer_id, amount)
    if not verification["verified"]:
        # Oops — already refunded!
        return {"status": "failed", "reason": f"Refunded ${amount} but balance insufficient. Money at risk!"}
    notification = send_notification(customer_id, f"Refund of ${amount} processed")
    return {"status": "completed", "refund": refund}


if __name__ == "__main__":
    # Run correct version
    with record_run(agent_name="refund-agent", model="v1-correct", goal="Process refund correctly") as _:
        result = run_correct_agent("C-42", 100)
        print(f"✓ Correct agent: {result['status']}")

    print(f"  Run: {_.run.run_id} ({len(_.run.events)} events)")

    correct_run_id = _.run.run_id

    # Run broken version
    with record_run(agent_name="refund-agent", model="v2-broken", goal="Process refund (with bug)") as _:
        result = run_broken_agent("C-42", 600)
        print(f"✗ Broken agent: {result['status']} — {result.get('reason', '')}")

    print(f"  Run: {_.run.run_id} ({len(_.run.events)} events)")

    broken_run_id = _.run.run_id

    print()
    print("=" * 50)
    print("DEMO COMPLETE — Here's what to do next:")
    print("=" * 50)
    print()
    print("View each run individually:")
    print(f"  agent-replay view {correct_run_id}")
    print(f"  agent-replay view {broken_run_id}")
    print()
    print("Compare to find the bug:")
    print(f"  agent-replay diff {correct_run_id} {broken_run_id}")
    print()
    print("Expected diff output:")
    print("  Step 1: tool changed from 'verify_payment' to 'process_refund'")
    print("  → The broken agent called refund BEFORE verification!")
