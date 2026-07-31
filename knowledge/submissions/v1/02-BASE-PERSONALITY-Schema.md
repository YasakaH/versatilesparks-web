# HPF v2 — BASE_PERSONALITY.md Schema (20-field inheritance)

## The Base Class
Every PERSONA.md must implement these 20 fields via `.inherit()`:

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | `id` | string | Unique identifier (e.g., `persona://domain/role`) |
| 2 | `name` | string | Human-readable name |
| 3 | `domain` | string | Primary domain (engineering, product, etc.) |
| 4 | `version` | semver | Current version |
| 5 | `description` | string | One-liner purpose |
| 6 | `role` | enum | `advisor`, `implementer`, `reviewer`, `coordinator` |
| 7 | `expertise` | string[] | Specialized knowledge areas |
| 8 | `capabilities` | string[] | Capability IDs this persona provides |
| 9 | `primary_skills` | string[] | Skill names this persona primarily uses |
| 10 | `inherits` | string | Base path for .inherit() |
| 11 | `thinking_model` | ref | Thinking model to use (from thinking library) |
| 12 | `constraints` | string[] | Domain-specific constraints |
| 13 | `evaluation_criteria` | string[] | How to measure success |
| 14 | `interaction_pattern` | string | How the persona engages with user/problems |
| 15 | `output_preferences` | object | Preferred output format, depth, style |
| 16 | `improvement_feedback` | string[] | What feedback helps this persona improve |
| 17 | `schema_version` | string | Version of the schema this persona uses |
| 18 | `before` | string? | Lifecycle hook: runs before persona activation |
| 19 | `after` | string? | Lifecycle hook: runs after persona deactivation |
| 20 | `error_handler` | string? | Custom error handling for this persona |

## Questions for ChatGPT
1. Should lifecycle hooks (`before`, `after`, `error_handler`) be mandatory or optional?
2. Are 20 fields the right scope? Too many for simple personas, too few for complex ones?
3. Should I add a `dependencies` field for persona-to-persona dependencies?
4. Should personas support multiple roles (e.g., `advisor+reviewer`)?
