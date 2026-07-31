# PLANNING_FRAMEWORK.md

## Purpose

How Hermes breaks tasks into actionable steps, estimates complexity, and chooses execution strategy. This is separate from decision-making (which choices to make) and verification (whether outputs are correct). Planning is about structuring the work itself.

## Planning Workflow

```
Understand → Break → Estimate → Choose Strategy → Deliver
    ↓          ↓        ↓              ↓             ↓
  Read full  Divide  How hard?    Fast vs deep   Verify + reflect
  request    into     Can parallel  Trade-off    with checklist
             steps   execute?
```

## Step 1: Break Tasks

For tasks with more than three steps, break them into sub-tasks. Each step should:
- Be atomic (one tool call, one clear outcome)
- Have a defined input and output
- Not depend on unconfirmed assumptions

### When NOT to break tasks down
- Single command execution (`git push`)
- Simple lookups ("what's my IP?")
- One-shot creative generation ("write me a poem")

### When you MUST break tasks down
- More than three sequential operations
- Parallel operations with dependencies
- Any task with potential failure modes
- Tasks involving external state changes (delete, publish, spend)

## Step 2: Estimate Complexity

| Complexity | Signs | Approach |
|-----------|-------|----------|
| **Low** | Clear scope, existing patterns, single layer | Quick plan, execute |
| **Medium** | Some ambiguity, 2-3 layers, known tools | Plan → Execute → Verify |
| **High** | Novel problem, cross-domain, unknowns | Deep research → Multi-step plan → Iterative verification |

## Step 3: Choose Execution Strategy

| Strategy | When | Example |
|----------|------|---------|
| **Direct** | Clear, safe, reversible | `ls`, `grep` |
| **Plan first** | Multi-step, some risk | Deploy, refactor |
| **Research first** | Unknown territory | New framework, unfamiliar API |
| **Iterative** | Exploratory, high uncertainty | Debugging complex issues |

## Step 4: Identify Blockers

Before executing, check for:
- Missing permissions (can we write files in target directory?)
- External dependencies (does this require network access?)
- Time-sensitive resources (API rate limits, session timeouts)
- User preference conflicts (does this violate BOUNDARIES?)

## Step 5: Deliver

After planning completes execution, deliver with:
- Summary of what was done
- Key decisions and rationale
- Next steps (if any)
- Open questions or uncertainties

## Anti-Patterns

- **Over-planning**: If the plan is longer than the execution, you've over-planned. Default to quick plan for <10min tasks.
- **Planning without executing**: If you can't estimate time to complete the plan, you should do it instead of planning it.
- **No rollback plan**: For irreversible actions, always identify how to undo before proceeding.

---

*End of PLANNING_FRAMEWORK.md*
