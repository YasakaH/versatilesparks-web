# Evidence Builder

Transforms assembled knowledge objects into a mode-specific argument structure. This is the intellectual heart of HPF.

## Input

- Mode (string): the reasoning mode
- Objects (list): assembled knowledge objects with full content
- Question (string): original question

## Process

1. Select the appropriate mode contract (from REASONING_MODES.md)
2. For each section of the contract, pull relevant facts, interpretations, and recommendations from objects
3. Fill the contract ensuring all required sections are present
4. Validate against the mode's invariants
5. Return the structured argument

## Validation

Each mode has invariants that must be checked before rendering:
- Explain: definition must be self-contained, every claim in Core Mechanics must trace to a fact
- Compare: scoring must reference specific facts, recommendation must be conditional
- Decide: both supporting AND contradictory evidence required
- Troubleshoot: causes ordered by probability, diagnostic steps ordered by speed
- Design: at least 2 approach options, pitfalls from actual experience
