# Question Analyzer

Routes a question to a reasoning mode and extracts roles and entities.

## Input

A question string (plain text).

## Output

```json
{
  "mode": "explain|compare|decide|troubleshoot|design",
  "entities": ["term1", "term2"],
  "roles": ["role1", "role2"]
}
```

## Mode Routing

Based on linguistic signals:

| Signal | Mode |
|--------|------|
| "what is", "how does", "tell me about", "explain" | explain |
| "difference", "vs", "versus", "compare", "which is better" | compare |
| "should i", "is it a good idea", "what should", "recommend" | decide |
| "broken", "failing", "crash", "error", "doesn't work", "why" | troubleshoot |
| "design", "implement", "build", "architecture", "how should" | design |

If multiple signals match, use the most specific mode (decide > compare > explain > troubleshoot > design).
If unclear, default to explain.

## Entity Extraction

Extract noun phrases that could be knowledge object names, technologies, or tools.
