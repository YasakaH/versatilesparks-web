"""Restructure HPF v2: 33 docs → 10 kernel + 4 governance + reference"""
import os
from pathlib import Path

BASE = Path(r'C:\Users\varas\personalities')
CORE = BASE / 'CORE'
GOV = BASE / 'governance'

KERNEL = BASE / 'kernel'
GOV_NEW = BASE / 'governance_new'
REF = BASE / 'reference'

def merge_files(target, sources, header=''):
    """Merge multiple source files into one target doc"""
    lines = [f'# {target.stem.replace("_", " ").title()}', '']
    if header:
        lines.append(header)
        lines.append('')
    lines.append(f'> Consolidated from: {", ".join(str(s).replace(str(BASE)+chr(92), "").replace(chr(92), "/") for s in sources)}')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    for src_path in sources:
        if not src_path.exists():
            print(f'  ⚠️ {src_path.name} not found, skipping')
            continue
        content = src_path.read_text(encoding='utf-8')
        parts = content.split('\n', 2)
        body = parts[2] if len(parts) > 2 else content
        lines.append(f'## From: {src_path.name}')
        lines.append('')
        lines.append(body.strip())
        lines.append('')
        lines.append('---')
        lines.append('')
    
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(lines), encoding='utf-8')
    size = target.stat().st_size
    print(f'✅ {target.name} ({size/1024:.0f} KB)')

def create_doc(target, content):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + '\n', encoding='utf-8')
    print(f'✅ Created {target.name} ({len(content)} chars)')

# ========== KERNEL (10 docs) ==========
print('=== KERNEL ===')

# 1. DNA.md - Core identity
create_doc(KERNEL / 'DNA.md', '''# DNA

> The fundamental identity and axioms of Hermes. Immutable.

## Core Identity
Hermes is an intelligent agent operating system. Not a chatbot, not a tool — an OS for cognition.

## Immutable Axioms
1. Truth over agreement
2. Evidence over confidence
3. First principles over convention
4. Simplicity over cleverness
5. Practicality over theory
6. Long-term maintainability over short-term convenience
7. Quality measured by outcomes, not explanations

## Core Drive
Every interaction must leave the system better than it was found.
''')

# 2. CONSTITUTION.md
merge_files(KERNEL / 'CONSTITUTION.md', [
    CORE / 'CONSTITUTION.md',
    CORE / 'CONFLICT_RESOLUTION_POLICY.md',
    CORE / 'ESCALATION_POLICY.md',
])

# 3. ARCHITECTURE.md
merge_files(KERNEL / 'ARCHITECTURE.md', [
    CORE / 'ARCHITECTURE_PRINCIPLES.md',
    CORE / 'ORCHESTRATION_POLICY.md',
    CORE / 'EVOLUTION_ENGINE.md',
])

# 4. PERSONALITY_MODEL.md
merge_files(KERNEL / 'PERSONALITY_MODEL.md', [
    CORE / 'BASE_PERSONALITY.md',
    CORE / 'PERSONALITY_SCHEMA.md',
    CORE / 'PERSONALITY_CREATION_GUIDE.md',
])

# 5. CAPABILITY_MODEL.md
merge_files(KERNEL / 'CAPABILITY_MODEL.md', [
    CORE / 'CAPABILITY_REGISTRY.md',
    CORE / 'SKILL_SELECTION_POLICY.md',
])

# 6. SKILL_MODEL.md
merge_files(KERNEL / 'SKILL_MODEL.md', [
    CORE / 'SKILL_CREATION_GUIDE.md',
])

# 7. ARTIFACT_MODEL.md
create_doc(KERNEL / 'ARTIFACT_MODEL.md', '''# Artifact Model

> Defines output contracts — what Hermes produces and how it is structured.

## Output Principles
1. Every artifact has a schema
2. Every artifact is versioned
3. Every artifact is traceable to its inputs
4. Every artifact is independently reviewable

## Standard Artifact Types
- **Decision Record** — What was decided, why, by whom, with what evidence
- **Execution Plan** — Task DAG, dependencies, expected outputs
- **Review Report** — Findings, severity, recommendations
- **Skill Definition** — Reusable procedure with triggers and verification
- **Persona Definition** — Complete personality with schema compliance

## Validation Gates
Every artifact must pass: schema check → constitution check → quality gate → registry
''')

# 8. MEMORY_MODEL.md
create_doc(KERNEL / 'MEMORY_MODEL.md', '''# Memory Model

> Governs how Hermes captures, stores, retrieves, and expires knowledge.

## Memory Levels
- **Ephemeral** — Current task context (lost after completion)
- **Session** — Conversation state (persists for session duration)
- **Long-term** — Stable preferences, rules, skills (survives restarts)
- **System** — Hermes knowledge base (versioned, audited)

## Memory Manager (subsystem, not personality)
Responsibilities:
1. **Capture** — Extract learnings from completed tasks
2. **Classify** — Assign memory level based on stability/relevance
3. **Retrieve** — Context-aware recall with decay weighting
4. **Expire** — TTL-based cleanup with confirmation for long-term
5. **Audit** — Log all memory operations for review

## Sync Strategy
- Local SQLite store (Honcho-compatible)
- Telegram backup for long-term/system memory
- 30-minute sync cadence for new entries
''')

# 9. EVALUATION_MODEL.md
merge_files(KERNEL / 'EVALUATION_MODEL.md', [
    CORE / 'EVALUATION.md',
    CORE / 'CONTINUOUS_IMPROVEMENT.md',
    CORE / 'PRIORITIZATION_FRAMEWORK.md',
])

# 10. SECURITY_MODEL.md
create_doc(KERNEL / 'SECURITY_MODEL.md', '''# Security Model

> Security boundaries, threat models, and safe operation principles.

## Core Principles
1. Least privilege — operate with minimum required access
2. Defense in depth — multiple layers of verification
3. Auditability — every security-relevant action is logged
4. Fail secure — default-deny on all permissions

## Security Gates
- **Input validation** — Sanitize all external inputs
- **Output review** — No sensitive data in responses
- **Escalation check** — Approve high-risk operations
- **Session isolation** — No cross-session data leakage
''')

# ========== GOVERNANCE (4 docs) ==========
print('\\n=== GOVERNANCE ===')

merge_files(GOV_NEW / 'VERSION_POLICY.md', [
    GOV / 'personality-policy.md',
    GOV / 'contribution-policy.md',
])

merge_files(GOV_NEW / 'CHANGE_MANAGEMENT.md', [
    GOV / 'AUTHORITY_MODEL.md',
    GOV / 'ESCALATION.md',
    GOV / 'AUDIT_TRAIL.md',
])

merge_files(GOV_NEW / 'QUALITY_GATES.md', [
    CORE / 'QUALITY_GATES.md',
    CORE / 'QUALITY_STANDARDS.md',
    CORE / 'OUTPUT_STANDARD.md',
    CORE / 'OBSERVABILITY.md',
])

merge_files(GOV_NEW / 'DEPRECATION_POLICY.md', [
    GOV / 'deprecation-policy.md',
    GOV / 'security-policy.md',
])

# Create reference dir
print()
print('=== REFERENCE ===')
REF.mkdir(parents=True, exist_ok=True)

# Move remaining CORE docs to reference
for f in sorted(CORE.glob('*.md')):
    dest = REF / f.name
    content = f.read_text(encoding='utf-8')
    dest.write_text('> Originally from CORE/' + f.name + '\n\n' + content, encoding='utf-8')
    label = 'CORE/' + f.name + ' -> reference/'
    print(label)

print()
print('Restructure complete!')
print('Kernel: ' + str(len(list(KERNEL.glob('*.md')))) + ' docs')
print('Governance: ' + str(len(list(GOV_NEW.glob('*.md')))) + ' docs')
print('Reference: ' + str(len(list(REF.glob('*.md')))) + ' docs')

