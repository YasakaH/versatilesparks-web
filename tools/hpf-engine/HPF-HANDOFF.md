# HPF Engine — Handoff Document

## What This Is

HPF (Hierarchical Provenance Framework) is a reasoning engine that answers browser-automation questions using structured knowledge objects. It was built to prove the thesis: _Can a structured reasoning pipeline produce better engineering answers than a frontier model using the same knowledge domain?_

## Architecture

```
question_analyzer.py          retriever.py          evidence_builder.py       renderer.py
┌────────────────────┐    ┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐
│ Mode detection     │ →  │ Entity matching  │ →  │ Mode-specific     │ →  │ Markdown       │
│ Entity extraction  │    │ Scoring + sort   │    │ argument builder  │    │ formatting     │
│ 30 known entities  │    │ Max-per-entity   │    │ Validation        │    │ 5 mode formatters
└────────────────────┘    └─────────────────┘    └──────────────────┘    └────────────────┘
```

### 5 Reasoning Modes
- **explain** — factual definition + mechanics + examples + limitations
- **compare** — side-by-side criteria scoring + trade-offs + recommendation
- **decide** — should-I-do-X with supporting/contradictory evidence + risks
- **troubleshoot** — problem → likely causes (with probability, evidence, diagnostic steps, fix)
- **design** — problem → approach options → recommendation → pitfalls → best practices

### Key Files
| File | Purpose |
|---|---|
| `hpf/question_analyzer.py` | Mode routing (`\bwhy\b` → troubleshoot, `vs?\b` → compare, `should\b` → decide, `design|build\b` → design, else → explain). Entity extraction (30 KNOWN_ENTITIES + dynamic `-ing`/`-ion` extraction). |
| `hpf/retriever.py` | `load_domain(domain_dir)` loads markdown knowledge objects. `retrieve(entities, objects)` scores each object per entity: exact_id=1.0, id_prefix=0.8, title_match=0.8, tag_match=0.7, partial_id=0.3, semantic_match=0.4. Max-per-entity scoring then tie-breaker (id match > title/tag > semantic only). |
| `hpf/evidence_builder.py` | `build(mode, objects, question)` → `(argument, actual_mode)`. Falls back compare→explain if <2 objects. Builds mode-specific dicts with validation. |
| `hpf/renderer.py` | `render(mode, argument)` → markdown string. 5 formatters: `format_explain`, `format_compare`, `format_decide`, `format_troubleshoot`, `format_design`. |
| `evaluation/harness.py` | `--run hpf rag gemini mistral` — runs benchmark, generates blind eval sets (shuffled A/B), metadata, and results.json. |
| `evaluation/scorer.py` | Dual-judge auto-scorer. Runs Mistral Small + NVIDIA Llama on blind eval files. Each judge outputs 6-dimension scores + winner + rationale. Averages across judges, flags disagreements. |
| `evaluation/benchmark_v1.yaml` | 30 frozen questions across 5 modes (8 explain, 6 compare, 6 decide, 6 troubleshoot, 4 design). |

### Knowledge Domain
14 objects in `domain/knowledge/`:
`anti-detection-principle`, `blocking-rate-limiting-principle`, `browser-profiles-concept`, `cdp-concept`, `download-pipeline-pattern`, `health-check-pattern`, `incremental-extraction-pattern`, `nodriver-concept`, `playwright-concept`, `retry-pattern`, `selector-strategy-pattern`, `selenium-concept`, `session-lifecycle-concept`, `webdriver-concept`

Each object is a markdown file with: Metadata (id, title, tags, entities), Narrative Layer (prose), and optionally Compare/Decide/Troubleshoot/Design sections.

## Bugs Fixed During Development

1. **Retrieval scoring** — used sum across entities → changed to max-per-entity scoring
2. **Semantic field missing** — `semantic` field wasn't in retrieve output
3. **Tag parsing** — tags in Identity section weren't parsed because `_parse_list` only checked Metadata
4. **Section extraction** — regex didn't handle blank lines after section headers
5. **Mode detection** — "why do" not in troubleshoot patterns → added `\bwhy (do|does|is|are|can't|didn't)\b`
6. **Explain vs troubleshoot ambiguity** — "why do browser profiles matter?" misclassified → added explanatory-marker check
7. **Compare mode with <2 objects** — produced validation errors → fallback to explain mode
8. **Entity extraction** — missed "browser", "crash", "navigation" → added dynamic extraction
9. **Mode fallback propagation** — `build()` changed mode but `render()` used original → now returns `(argument, actual_mode)`
10. **Evidence output** — used object IDs in user-facing text → changed to titles

## Benchmark Results (run_002)

| Mode | HPF avg | RAG avg | Winner |
|---|---|---|---|
| explain (8) | **74.6** | 38.9 | HPF 6-2 |
| troubleshoot (6) | **54.1** | 48.1 | HPF 3-3 (edge) |
| design (4) | **57.8** | 52.9 | HPF 2-2 (edge) |
| decide (6) | 32.2 | **37.1** | RAG 3-3 (edge) |
| compare (6) | 48.5 | **72.2** | RAG 4-2 |
| **Total (30)** | **63.0** | 63.4 | HPF 9 wins, RAG 11 wins, 10 disagreements |

Dual-judge (Mistral + Llama averaged): HPF 1891 total, RAG 1903 total.

## M1 Exit Criteria (Met)

- ✅ Dual-judge benchmark operational (Mistral Small + NVIDIA Llama)
- ✅ Blind evaluation pipeline validated (30 shuffled eval files)
- ✅ Reproducible scoring established (scores.json with per-judge traces)
- ✅ Initial benchmark dataset collected (run_002)
- ✅ Evidence available to guide HPF improvements

## M2 Plan (Analysis Phase — Not Started)

The M2 analysis should produce these 5 documents before any implementation:

1. **`disagreement-analysis.md`** — Classify 10 disagreement cases into rubric ambiguity, prompt ambiguity, model variance, HPF behavioural issue, RAG behavioural issue, or genuine tie
2. **`compare-mode-analysis.md`** — For all 6 compare tasks: what HPF produced, what RAG produced, why RAG won, which capability failed
3. **`decision-mode-analysis.md`** — Why decide mode scores are low (knowledge gap? reasoning gap? framework gap?)
4. **`systemic-deficiencies.md`** — Aggregate patterns: 22 isolated mistakes → 9 recurring behaviours → 3 systemic deficiencies
5. **`improvement-priority.md`** — Ranked priorities with evidence

The recommended M2 workflow: Observation → Pattern → Root Cause → Hypothesis → Improvement → Validation. Only one behavioural improvement per cycle to maintain attribution.

## Providers Available

| Provider | Model | Key | Status |
|---|---|---|---|
| Mistral Small | `mistral-small-latest` | `MISTRAL_API_KEY` | ✅ Works |
| NVIDIA Llama | `meta/llama-3.1-8b-instruct` | `NVIDIA_API_KEY` | ✅ Works |
| Gemini | `gemini-2.0-flash` | `GOOGLE_API_KEY` | ⚠ Rate-limited (429) |
| Gemma | `gemma-4-31b-it` | `GOOGLE_API_KEY` | ⚠ Thinking mode interferes with JSON |
| GPT-4 | `gpt-4` | `OPENAI_API_KEY` | ❌ No key |
| Claude | `claude-3-5-sonnet` | `ANTHROPIC_API_KEY` | ❌ No key |

API keys in `C:\Users\varas\AppData\Local\hermes\.env`.

## What's NOT Done (Future Work)

- Compare mode: needs dynamic criteria from retrieved objects instead of hardcoded template
- Decide mode: needs better claim/support extraction
- Blind human evaluation: 10 disagreement cases need manual review
- Additional frontier model comparison (GPT, Claude) if keys become available
- Knowledge Pack expansion beyond 14 objects
