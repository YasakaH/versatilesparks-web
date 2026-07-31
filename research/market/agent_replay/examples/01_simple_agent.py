"""01 — Simple tool agent with recording.

Demonstrates: basic @record decorator and record_run context manager.
"""

from agent_replay import record, record_run


@record("search_inventory")
def search_inventory(query):
    products = {
        "laptop": {"name": "MacBook Pro", "price": 1299, "stock": 5},
        "mouse": {"name": "MX Master 3", "price": 79, "stock": 12},
        "keyboard": {"name": "Keychron Q1", "price": 199, "stock": 0},
    }
    return products.get(query, {"error": f"Product '{query}' not found"})


@record("calculate_total")
def calculate_total(product, quantity=1):
    result = search_inventory(product)
    if "error" in result:
        return result
    if result["stock"] < quantity:
        return {"error": f"Insufficient stock: {result['stock']} available"}
    return {
        "product": result["name"],
        "quantity": quantity,
        "unit_price": result["price"],
        "total": result["price"] * quantity,
    }


@record("place_order")
def place_order(product, quantity=1, payment="card"):
    calc = calculate_total(product, quantity)
    if "error" in calc:
        return {"status": "failed", "reason": calc["error"]}
    if not payment:
        return {"status": "failed", "reason": "No payment method"}
    return {
        "status": "completed",
        "order": "ORD-" + __import__("os").urandom(3).hex().upper(),
        "details": calc,
    }


if __name__ == "__main__":
    with record_run(
        agent_name="order-agent",
        model="demo-v1",
        goal="Place order for a laptop with credit card"
    ) as _:
        result = place_order("laptop", 2, "credit_card")
        print(f"Result: {result['status']}")
        if "order" in result:
            print(f"Order: {result['order']}")

    print(f"\nView: agent-replay view {_.run.run_id}")
