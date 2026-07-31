"""Parse ChatGPT response file — split by [ASSISTANT] markers."""
import re, json
from pathlib import Path

RESPONSES_FILE = r'C:\Users\varas\personalities\_chatgpt_all_responses.txt'
PARSE_DIR = Path(r'C:\Users\varas\personalities\_chatgpt_feedback')
PARSE_DIR.mkdir(exist_ok=True)

with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

# Split by [ASSISTANT] markers
chunks = re.split(r'={3,}\s*\[ASSISTANT\]\s*={3,}', text)
chunks = [c.strip() for c in chunks if c.strip() and len(c.strip()) > 100]

print(f'Found {len(chunks)} assistant response chunks')

summary = []
for i, chunk in enumerate(chunks):
    # Extract the "Review:" line
    lines = chunk.split('\n')
    header = lines[0] if lines else ''
    
    # Find what's being reviewed
    review_match = re.search(r'Review:\s*(.+?)(?:\n|$)', chunk)
    review_target = review_match.group(1).strip() if review_match else header[:100]
    
    # Count chars
    char_count = len(chunk)
    
    # Extract actionable sentences
    actions = []
    for line in lines:
        ll = line.strip().lower()
        if any(w in ll for w in ['should', 'need to', 'add a', 'remove', 'change', 'consider', 'recommend', 'suggest', 'missing']):
            actions.append(line.strip()[:200])
    
    # Save individual file
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', review_target.lower().strip()[:40])
    filepath = PARSE_DIR / f'{i:02d}_{safe_name}.md'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'# ChatGPT Response {i+1}: {review_target}\n\n')
        f.write(f'> Size: {char_count} chars | Chunk: {i+1}/{len(chunks)}\n\n')
        if actions:
            f.write('## Actionable Items\n\n')
            for a in actions[:10]:
                f.write(f'- {a}\n')
        f.write('\n---\n\n')
        f.write(chunk[:30000])  # Truncate very long ones
        if len(chunk) > 30000:
            f.write('\n\n... [truncated]')
    
    summary.append({
        'index': i,
        'review_target': review_target,
        'size': char_count,
        'actionable_items': len(actions),
        'file': filepath.name
    })
    
    print(f'  [{i+1:02d}] {review_target[:60]:60s} {char_count:>7,} chars  {len(actions)} actions')

# Save summary
with open(PARSE_DIR / '_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f'\nTotal: {len(chunks)} responses, saved to {PARSE_DIR}')
print(f'Summary: {PARSE_DIR / "_summary.json"}')
