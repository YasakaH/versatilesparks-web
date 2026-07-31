# Node Contract — Perception

> **Status:** Pilot Draft  
> **Package:** Node 01 (Perception)  
> **Version:** 0.1.0  
> **Last Updated:** 2026-07-22  

---

## Contract Declaration

```yaml
node: 01
name: Perception

consumes:
  raw_signals:
    description: Unprocessed environmental data from execution surfaces
    format: varies by surface (pixels, bytes, streams, events)
    source: Nodes 17–22 (Execution Surfaces)
  previous_observations:
    description: Recent observations from working memory for temporal context
    format: observation objects with confidence scores
    source: Node 09 (Working Memory)

produces:
  structured_observation:
    description: Transformed, tokenized representation of environmental state ready for Decision Engine
    includes:
      - content: text tokens, embeddings, scalars, JSON objects
      - confidence_score: numeric certainty 0.0–1.0
      - timestamp: when observation was captured
      - token_count: number of tokens emitted
      - modality_used: which perception method was selected
    target: Node 02 (Decision Engine)
  perception_span:
    description: Observability span for every perception event
    format: structured telemetry (latency, cost, modality, result)
    emits_to: Node 12 (Observability)

guarantees:
  - confidence_estimate: Every observation carries a confidence score, even if very low
  - freshness_metadata: Timestamp included on every observation
  - modality_transparency: Observation identifies which modality produced it

does_not_guarantee:
  - correctness: Captures what surface provides, not ground truth
    responsibility: Decision Engine must weigh confidence and cross-validate
  - completeness: Some surfaces may not expose all relevant signals
    responsibility: Downstream nodes must handle partial observations
  - timeliness: Latency varies widely by modality (3s AXTree → 60s vision multi-step)
    responsibility: Scheduling must account for variable perception latency
  - temporal_persistence: Does not persist observations beyond session scope
    responsibility: Working Memory and Long-term Memory handle persistence

side_effects:
  - writes_working_memory: Stores recent observations for context
    scope: Session-scoped only (see Node 09)
  - emits_observation_span: Creates an observability span for every perception event
    scope: Tracked in Observability node (Node 12)

timing:
  min_latency_per_step: "3s (AXTree on compliant site)"
  max_latency_per_step: "60s (vision multi-step on complex page)"
  throughput_constraint: Bounded by slowest modality in use and token budget
  ordering: Observations from consecutive steps are temporally ordered; parallel paths may reorder
```

---

## Neighboring Node Dependencies

| Neighbor | What It Gets | What It Provides | Risk if Contract Breached |
|---|---|---|---|
| **Node 02: Decision Engine** | Structured observation + confidence score | Raw signals when task requires visual understanding | Bad decisions from missing or wrong signals |
| **Node 09: Working Memory** | Current observation | Session-scoped storage of recent observations | Loss of temporal context |
| **Node 11: Environment State** | Mutations when environment changes | Ground truth conditions being observed | Stale perception of changed state |
| **Node 12: Observability** | Perception spans | Aggregated metrics across steps | Untraceable perception costs |
| **Nodes 17–22: Execution Surfaces** | Raw signal availability | Signal quality dictates available modalities | Wrong modality selection |
