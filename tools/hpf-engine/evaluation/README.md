# HPF Evaluation Harness

Minimal benchmark for comparing HPF output against frontier model baselines.

## Structure

```
evaluation/
  benchmark_v1.yaml     # Frozen 30-question benchmark
  providers/            # AnswerProvider interface + implementations
    __init__.py         # Abstract base + HPFProvider
    gpt_provider.py     # GPT-4
    claude_provider.py  # Claude 3.5 Sonnet
    gemini_provider.py  # Gemini 2.0 Flash
    rag_provider.py     # Naive RAG baseline (no structured reasoning)
  harness.py            # Benchmark runner
  runs/                 # Generated evaluation runs
  blind/                # Blind eval sets (answers shuffled)
  meta/                 # Metadata mapping letters -> providers
  results.json          # Full results
  scores/               # Scored results
  reports/              # Summary reports
```

## Usage

```bash
# List benchmark questions
python evaluation/harness.py --list

# Run all providers
python evaluation/harness.py

# Run specific providers
python evaluation/harness.py --providers hpf gpt

# Re-run a specific run
python evaluation/harness.py --providers hpf --run 001
```

## Scoring Rubric

| Criterion             | Weight | Description                         |
|-----------------------|--------|-------------------------------------|
| Technical correctness | 30     | Are the facts accurate?             |
| Completeness          | 20     | Does it cover what matters?         |
| Reasoning quality     | 20     | Are claims supported by evidence?   |
| Actionability         | 15     | Can the reader act on this?         |
| Clarity               | 10     | Is it well-structured and clear?    |
| Hallucination penalty | 5      | Penalty for fabrications            |

## Success Threshold

- Average score >= baseline (GPT-4 or Claude)
- No hallucinations on benchmark questions
- Every recommendation includes supporting evidence
- Every troubleshooting answer includes verification steps
- Every comparison includes explicit trade-offs
