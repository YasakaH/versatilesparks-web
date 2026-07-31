"""Compile ALL HPF v2 framework files into ChatGPT chunks"""
import os, json

ROOT = r'C:\Users\varas\personalities'
CHUNKS_DIR = r'C:\Users\varas\personalities\_for_chatgpt_v2'
os.makedirs(CHUNKS_DIR, exist_ok=True)

# Define chunk boundaries - grouped by topic for coherent review
chunks = [
    {
        "name": "01-CORE-Overview",
        "desc": "CORE Framework overview + Constitution + Architecture/Engineering Principles",
        "files": [
            "CORE/CONSTITUTION.md",
            "CORE/ARCHITECTURE_PRINCIPLES.md",
            "CORE/ENGINEERING_PRINCIPLES.md",
            "CORE/DECISION_FRAMEWORK.md",
            "CORE/QUALITY_STANDARDS.md",
            "CORE/EXECUTION_WORKFLOW.md",
        ]
    },
    {
        "name": "02-CORE-Behavior",
        "desc": "CORE behavior docs - thinking models, decision engine, review framework",
        "files": [
            "CORE/THINKING_MODELS.md",
            "CORE/DECISION_ENGINE.md",
            "CORE/REVIEW_FRAMEWORK.md",
            "CORE/PRIORITIZATION_FRAMEWORK.md",
            "CORE/CONTINUOUS_IMPROVEMENT.md",
        ]
    },
    {
        "name": "03-CORE-Schema",
        "desc": "Personality schema, base personality, creation guide",
        "files": [
            "CORE/PERSONALITY_SCHEMA.md",
            "CORE/BASE_PERSONALITY.md",
            "CORE/PERSONALITY_CREATION_GUIDE.md",
        ]
    },
    {
        "name": "04-CORE-Capabilities",
        "desc": "Capability registry, skill architecture, quality gates",
        "files": [
            "CORE/CAPABILITY_REGISTRY.md",
            "CORE/SKILL_CREATION_GUIDE.md",
            "CORE/SKILL_SELECTION_POLICY.md",
            "CORE/QUALITY_GATES.md",
            "CORE/OUTPUT_STANDARD.md",
        ]
    },
    {
        "name": "05-CORE-System",
        "desc": "System docs - evolution, observability, evaluation, conflict resolution",
        "files": [
            "CORE/EVOLUTION_ENGINE.md",
            "CORE/OBSERVABILITY.md",
            "CORE/EVALUATION.md",
            "CORE/CONFLICT_RESOLUTION_POLICY.md",
            "CORE/ORCHESTRATION_POLICY.md",
            "CORE/ESCALATION_POLICY.md",
        ]
    },
    {
        "name": "06-Governance",
        "desc": "Governance framework docs",
        "files": [
            "governance/ESCALATION.md",
            "governance/AUTHORITY_MODEL.md",
            "governance/AUDIT_TRAIL.md",
            "governance/contribution-policy.md",
            "governance/deprecation-policy.md",
            "governance/personality-policy.md",
            "governance/security-policy.md",
            "governance/skill-policy.md",
            "governance/version-policy.md",
        ]
    },
]

# Create chunks for persona groups
persona_dirs = {}
for root, dirs, files in os.walk(os.path.join(ROOT)):
    if 'PERSONA.md' in files:
        rel = os.path.relpath(root, ROOT)
        parts = rel.split(os.sep)
        domain = parts[0] if len(parts) > 0 else 'root'
        persona_name = parts[1] if len(parts) > 1 else os.path.basename(root)
        if domain not in persona_dirs:
            persona_dirs[domain] = []
        persona_dirs[domain].append(os.path.join(rel, 'PERSONA.md'))

# Group personas into logical chunks
persona_groups = [
    ("07-Personas-Engineering", ["engineering", "architecture", "ai", "devops", "security"]),
    ("08-Personas-Data-Research", ["data", "research", "education", "healthcare"]),
    ("09-Personas-Product-Design", ["product", "design", "creative"]),
    ("10-Personas-Business-Finance", ["business", "finance", "legal", "leadership"]),
    ("11-Personas-Marketing-Writing", ["marketing", "writing", "operations", "chief-of-staff"]),
]

for chunk_name, domains in persona_groups:
    chunk_files = []
    for domain in domains:
        if domain in persona_dirs:
            chunk_files.extend(persona_dirs[domain])
    chunks.append({
        "name": chunk_name,
        "desc": f"Persona files from {', '.join(domains)}",
        "files": chunk_files
    })

# Compile each chunk
for chunk in chunks:
    lines = [f"# HPF v2 — {chunk['name']}", f"## {chunk['desc']}", ""]
    total_chars = 0
    
    for filepath in chunk['files']:
        fullpath = os.path.join(ROOT, filepath)
        if not os.path.exists(fullpath):
            lines.append(f"\n[MISSING: {filepath}]\n")
            continue
        with open(fullpath, 'r', encoding='utf-8') as f:
            content = f.read()
        lines.append(f"\n---\n### {filepath}\n")
        lines.append(content)
        total_chars += len(content)
    
    lines.append(f"\n\n## Question for ChatGPT\nReview this chunk. What improvements, gaps, or issues do you see?")
    content = '\n'.join(lines)
    
    filepath = os.path.join(CHUNKS_DIR, f"{chunk['name']}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    file_count = len([f for f in chunk['files'] if os.path.exists(os.path.join(ROOT, f))])
    print(f"{chunk['name']}: {file_count} files, {len(content)} chars")

print(f"\nTotal chunks: {len(chunks)}")

# Save manifest
with open(os.path.join(CHUNKS_DIR, 'MANIFEST.json'), 'w') as f:
    json.dump([
        {"name": c['name'], "desc": c['desc'], "files": len(c['files'])} 
        for c in chunks
    ], f, indent=2)
