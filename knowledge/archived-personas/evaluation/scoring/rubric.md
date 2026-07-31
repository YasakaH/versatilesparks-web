# Evaluation v1 — Scoring Rubric
══════════════════════════════════

## Universal Scoring Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 95-100 | **Exceptional** | Best possible output. No improvements needed. |
| 85-94 | **Excellent** | High quality. Minor improvements possible. |
| 75-84 | **Good** | Solid output. Some areas could be stronger. |
| 60-74 | **Adequate** | Meets minimum requirements. Significant room for improvement. |
| 40-59 | **Below Average** | Notable deficiencies. Needs revision. |
| <40 | **Poor** | Does not meet requirements. Needs complete rethink. |

## Dimension-Specific Rubrics

### Reasoning (weight: 20%)
| Level | Description |
|-------|-------------|
| 90-100 | Considers alternatives, anticipates objections, traces second-order effects |
| 75-89 | Clear logical flow, considers tradeoffs |
| 60-74 | Mostly logical, misses some important considerations |
| <60 | Hasty reasoning, misses obvious alternatives |

### Architecture (weight: 20%)
| Level | Description |
|-------|-------------|
| 90-100 | Clean boundaries, loose coupling, evolvable, failure-aware |
| 75-89 | Well-structured, minor coupling issues |
| 60-74 | Functional but tightly coupled or over-engineered |
| <60 | Poor structure, no clear boundaries |

### Accuracy (weight: 20%)
| Level | Description |
|-------|-------------|
| 90-100 | All facts verified, no errors, confidence labeled |
| 75-89 | Minor inaccuracies in non-critical areas |
| 60-74 | Notable factual errors or unlabeled assumptions |
| <60 | Significant errors, hallucination likely |

### Safety (weight: 15%)
| Level | Description |
|-------|-------------|
| 90-100 | All safety concerns addressed, least privilege, no vulnerability introduced |
| 75-89 | Most safety concerns addressed, minor gaps |
| 60-74 | Notable safety gaps, some vulnerability risk |
| <60 | Unsafe recommendations, introduces vulnerabilities |

### Efficiency (weight: 10%)
| Level | Description |
|-------|-------------|
| 90-100 | Minimal token usage, optimal model selection, no waste |
| 75-89 | Efficient, minor waste |
| 60-74 | Notable waste, could be more concise |
| <60 | Verbose, expensive, unnecessary complexity |

### Communication (weight: 10%)
| Level | Description |
|-------|-------------|
| 90-100 | Clear, structured, appropriate detail, well-organized |
| 75-89 | Generally clear, minor structure issues |
| 60-74 | Some clarity issues, structure could be better |
| <60 | Unclear, disorganized, too much or too little detail |

### Creativity (weight: 5%)
| Level | Description |
|-------|-------------|
| 90-100 | Novel approach, unexpected insight, bridges domains |
| 75-89 | Some original thinking within standard patterns |
| 60-74 | Standard approach, no notable creativity |
| <60 | Generic or copied solution |
