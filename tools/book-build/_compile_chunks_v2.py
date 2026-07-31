"""Compile HPF v2 chunks - CORE full, PERSONA summaries, max 5KB per chunk"""
import os, re

ROOT = r'C:\Users\varas\personalities'
OUT = r'C:\Users\varas\personalities\_for_chatgpt_v2'
os.makedirs(OUT, exist_ok=True)

def extract_persona_summary(filepath):
    """Extract just the identity/schema section from a PERSONA.md"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rel = os.path.relpath(filepath, ROOT)
    lines = content.split('\n')
    
    # Get first 40 lines (title, name, version, category, mission, responsibilities)
    head = '\n'.join(lines[:40])
    
    # Extract key fields
    fields = {}
    for line in lines[:40]:
        m = re.match(r'^##\s+(.+)', line)
        if m:
            section = m.group(1).strip()
    
    # Get first 3-4 sections (~40 lines)
    return f"### {rel}\n{head}\n...\n"

def extract_core_summary(filepath):
    """Full content for core files"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# Chunk definitions with size targets
chunks = [
    # CORE docs - full content (grouped by theme, max 5KB per chunk)
    ("01-Constitution-Principles.md",
     ["CORE/CONSTITUTION.md", "CORE/ARCHITECTURE_PRINCIPLES.md", "CORE/ENGINEERING_PRINCIPLES.md"]),
    
    ("02-Decision-Execution.md",
     ["CORE/DECISION_FRAMEWORK.md", "CORE/EXECUTION_WORKFLOW.md", "CORE/QUALITY_STANDARDS.md"]),
    
    ("03-Thinking-Review.md",
     ["CORE/THINKING_MODELS.md", "CORE/DECISION_ENGINE.md", "CORE/REVIEW_FRAMEWORK.md"]),
    
    ("04-Prioritization-Improvement.md",
     ["CORE/PRIORITIZATION_FRAMEWORK.md", "CORE/CONTINUOUS_IMPROVEMENT.md"]),
    
    ("05-Schema-Creation.md",
     ["CORE/PERSONALITY_SCHEMA.md", "CORE/BASE_PERSONALITY.md", "CORE/PERSONALITY_CREATION_GUIDE.md"]),
    
    ("06-Capabilities-Skills.md",
     ["CORE/CAPABILITY_REGISTRY.md", "CORE/SKILL_CREATION_GUIDE.md", "CORE/SKILL_SELECTION_POLICY.md"]),
    
    ("07-Quality-Output.md",
     ["CORE/QUALITY_GATES.md", "CORE/OUTPUT_STANDARD.md"]),
    
    ("08-System-Evolution.md",
     ["CORE/EVOLUTION_ENGINE.md", "CORE/OBSERVABILITY.md", "CORE/EVALUATION.md"]),
    
    ("09-Policies.md",
     ["CORE/CONFLICT_RESOLUTION_POLICY.md", "CORE/ORCHESTRATION_POLICY.md", "CORE/ESCALATION_POLICY.md"]),
    
    # Governance - full content
    ("10-Governance.md",
     ["governance/ESCALATION.md", "governance/AUTHORITY_MODEL.md", "governance/AUDIT_TRAIL.md",
      "governance/contribution-policy.md", "governance/deprecation-policy.md",
      "governance/personality-policy.md", "governance/security-policy.md",
      "governance/skill-policy.md", "governance/version-policy.md"]),
]

# Persona summaries - group by domain, each chunk has 3-5 personas
persona_files = {}
for root, dirs, files in os.walk(os.path.join(ROOT)):
    if 'PERSONA.md' in files:
        fp = os.path.join(root, 'PERSONA.md')
        rel = os.path.relpath(root, ROOT)
        domain = rel.split(os.sep)[0]
        if domain not in persona_files:
            persona_files[domain] = []
        persona_files[domain].append(fp)

# Flatten persona groups into chunks of max 4 files each
persona_order = [
    "engineering", "architecture", "ai", "devops", "security",
    "data", "research", "education", "healthcare",
    "product", "design", "creative",
    "business", "finance", "legal", "leadership",
    "marketing", "writing", "operations", "chief-of-staff"
]

chunk_idx = 11
for domain in persona_order:
    if domain in persona_files:
        files = persona_files[domain]
        # Split large domains into multiple chunks
        for i in range(0, len(files), 3):
            subset = files[i:i+3]
            suffix = f"-part{i//3+1}" if len(files) > 3 else ""
            name = f"{chunk_idx:02d}-Personas-{domain.title()}{suffix}.md"
            chunks.append((name, subset))
            chunk_idx += 1

# Compile each chunk
total_chars = 0
for filename, file_list in chunks:
    lines = []
    for fp in file_list:
        full = os.path.join(ROOT, fp)
        if os.path.exists(full):
            if 'PERSONA.md' in fp:
                lines.append(extract_persona_summary(full))
                lines.append("")
            else:
                lines.append(f"### {fp}\n")
                lines.append(extract_core_summary(full))
                lines.append("")
        else:
            lines.append(f"### {fp}\n[MISSING]\n")
    
    # Add question
    if 'PERSONA' in filename:
        lines.append("\n## Question\nReview these personas. Any gaps, overlaps, or improvements needed?")
    else:
        lines.append("\n## Question\nReview this chunk. What improvements, gaps, or issues do you see?")
    
    content = '\n'.join(lines)
    outpath = os.path.join(OUT, filename)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    actual_files = len([f for f in file_list if os.path.exists(os.path.join(ROOT, f))])
    print(f"{filename}: {actual_files} files, {len(content):,} chars")
    total_chars += len(content)

print(f"\nTotal: {len(chunks)} chunks, {total_chars:,} total chars")
