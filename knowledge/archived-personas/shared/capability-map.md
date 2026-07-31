# Capability Map

Maps each skill to the capabilities it provides. Skills may provide multiple capabilities.
Personalities reference capabilities, not specific skill names.

## Engineering Capabilities

| Capability | Skills That Provide It |
|-----------|----------------------|
| `repository-analysis` | repository-audit, codebase-inspection |
| `architecture-review` | improve-codebase-architecture, architecture-migration |
| `code-review` | code-review, requesting-code-review |
| `performance-analysis` | performance-first, latency-analysis |
| `technical-debt` | repository-audit, improve-codebase-architecture |
| `testing` | tdd, qa, test-driven-development |
| `refactoring` | request-refactor-plan, simplify-code |
| `debugging` | diagnosing-bugs, systematic-debugging |
| `design-review` | design-an-interface, domain-modeling |
| `documentation` | documentation-architect, technical-writer |
| `security-review` | security-auditor, threat-modeler |

## Research Capabilities

| Capability | Skills That Provide It |
|-----------|----------------------|
| `research` | research, deep-research |
| `source-verification` | source-tracker, fact-checker |
| `entity-analysis` | entity-research |
| `competitive-analysis` | competitive-intelligence |
| `fact-checking` | fact-checker, skeptical-researcher |

## Marketing Capabilities

| Capability | Skills That Provide It |
|-----------|----------------------|
| `seo-audit` | seo-keyword-research, seo-crawler, static-site-seo |
| `content-strategy` | content-strategist, marketing-systems |
| `competitor-analysis` | competitive-intelligence |
| `proposal-writing` | proposal-writer |

## AI Capabilities

| Capability | Skills That Provide It |
|-----------|----------------------|
| `mcp-development` | mcp-builder |
| `prompt-engineering` | prompt-review |
| `agent-evaluation` | ai-evaluator |
| `skill-authoring` | hermes-agent-skill-authoring, writing-great-skills |
| `workflow-automation` | workflow-automation, n8n-builder |

## DevOps Capabilities

| Capability | Skills That Provide It |
|-----------|----------------------|
| `github-management` | github-pr-workflow, github-code-review, github-issues |
| `pipelines` | github-pr-workflow |
| `secrets-management` | security-auditor |

## Productivity Capabilities

| Capability | Skills That Provide It |
|-----------|----------------------|
| `note-taking` | obsidian-vault, notion |
| `email` | agentmail |
| `document-processing` | nano-pdf, ocr-and-documents, powerpoint |
| `scheduling` | google-workspace |

## How to Use

1. **Personalities** declare `preferred_skills` as capability names
2. **Skills** advertise capabilities in their frontmatter
3. **The registry** resolves capability → skill at runtime
