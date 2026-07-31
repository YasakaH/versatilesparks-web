# Node Contracts v1.0

> **Status:** Frozen  
> **Date:** 2026-07-22  
> **Purpose:** Formal interface declarations between nodes — what each consumes, produces, guarantees, and does NOT guarantee.

---

## Rules

Every node MUST declare its contract. This is not documentation — it is the API specification that neighboring nodes depend on.

A contract has four fields:

| Field | Meaning |
|---|---|
| **Consumes** | What inputs this node expects |
| **Produces** | What outputs this node emits |
| **Guarantees** | What the node always delivers |
| **Does NOT Guarantee** | Explicit limitations — what neighbors must handle themselves |

If a neighboring node depends on something not listed in the contract, it is a dependency violation.

---

*End of Node Contracts Specification v1.0*
