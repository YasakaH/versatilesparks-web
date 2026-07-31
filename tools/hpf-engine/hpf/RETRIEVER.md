# Retriever

Finds candidate knowledge objects by matching extracted entities against object identities and metadata.

## Input

Entities (list of strings) from the Question Analyzer.

## Process

1. Load domain package.yaml for the target domain
2. For each entity, search knowledge objects by:
   - Exact id match
   - Title contains entity
   - Tags contain entity
   - Semantic layer contains entity
3. Rank by match quality
4. Return ordered candidates with relevance scores

## Output

```json
[
  {"id": "cdp-concept", "score": 1.0, "matched_on": "exact_id"},
  {"id": "webdriver-concept", "score": 0.8, "matched_on": "tag_match"}
]
```
