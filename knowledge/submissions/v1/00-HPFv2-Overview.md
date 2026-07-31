# HPF v2 — Hermes Personality Framework v2

## Overview
A modular personality orchestration system for Hermes Agent (v0.4+). 122+ components:
- 88 framework files (DNA, Constitution, Core docs, Policies, Governance)
- 34 PERSONA.md files across 19 domains
- Capability Registry, Evaluation Suite, Plugin API

## Architecture
### Layers (bottom-up):
1. **DNA** — immutable identity, values, ethics
2. **Constitution** — behavioral rules, response patterns
3. **BASE_PERSONALITY.md** — 20-field inheritance schema (base class)
4. **CORE Documents** (16 files) — Domain knowledge, response patterns, constraints
5. **Policies** (7 files) — Security, privacy, ethics, quality, communication, decision-making, tool-use
6. **Capability Registry** — 13 registered capabilities with scoring/ranking
7. **Governance Rules** (6 files) — Evolution, OS roles, conflict resolution, review process, meta-rules, directory standards
8. **Evaluation Suite** — Templates for skill/personality testing, regression tasks, scoring rubric
9. **Plugin & Extension API** — Manifest template, categories, security guidelines
10. **PERSONA.md files** (34 files across 19 domains)

### Key Design Decisions:
- Personalities = Orchestrators (not capability containers)
- Skills = Workers (doers, not deciders)
- Framework > Markdown (structure over prose)
- Capability Registry replaces skill tagging
- 4 Governance Pillars: CapReg, Governance Rules, Eval Suite, Plugin API

## Questions for ChatGPT
1. Is the 20-field BASE_PERSONALITY.md schema complete? What's missing?
2. Should personalities be Orchestrators or should I separate orchestrator behavior from domain knowledge?
3. Is the Capability Registry weighted scoring formula correct?
4. Are 34 personas across 19 domains the right scope, or too many/few?
5. Should I add an Observability layer to PERSONA.md (tracking persona usage/effectiveness)?
6. Is the Evaluation Suite comprehensive enough to validate persona quality?
