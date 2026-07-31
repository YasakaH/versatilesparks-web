"""Extract actionable items from all chatgpt feedback files and classify them."""
import re, json, os
from collections import Counter

FEEDBACK_DIR = r'C:\Users\varas\personalities\_chatgpt_feedback'
OUTPUT = os.path.join(FEEDBACK_DIR, '_actionable_summary.json')

files = sorted([f for f in os.listdir(FEEDBACK_DIR) if f.endswith('.md') and f != '_summary.json'])

theme_keywords = {
    'domain_boundaries': ['boundary', 'overlap', 'when to activate', 'selection', 'routing'],
    'workflow': ['workflow', 'steps', 'process', 'how to', 'procedure'],
    'evaluation': ['evaluate', 'measure', 'metric', 'success criteria', 'quality gate'],
    'missing_sections': ['missing', 'add a', 'need to add', 'should include', 'lacks'],
    'decision_framework': ['decision', 'tradeoff', 'priority', 'heuristic'],
    'operational_constraints': ['constraint', 'limit', 'boundary', 'scope', 'when not'],
    'mental_models': ['mental model', 'thinking', 'principle'],
}

all_actions = []

for fname in files:
    fpath = os.path.join(FEEDBACK_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the review target from first line
    first_line = content.split('\n')[0] if content else ''
    
    # Find actionable items section
    actions = []
    in_actions = False
    for line in content.split('\n'):
        if '## Actionable Items' in line:
            in_actions = True
            continue
        if in_actions and line.startswith('## '):
            break
        if in_actions and line.strip().startswith('- '):
            actions.append(line.strip()[2:])
    
    # Categorize by theme
    themes = Counter()
    for action in actions:
        for theme, keywords in theme_keywords.items():
            if any(kw in action.lower() for kw in keywords):
                themes[theme] += 1
    
    entry = {
        'file': fname,
        'target': first_line.replace('# ', ''),
        'action_count': len(actions),
        'top_themes': [t for t, c in themes.most_common(3)],
        'actions': actions[:15],  # Top 15 actions
    }
    all_actions.append(entry)

# Cross-cutting themes
all_themes = Counter()
for entry in all_actions:
    for theme in entry['top_themes']:
        all_themes[theme] += 1

output = {
    'total_personas': len(all_actions),
    'total_actions': sum(e['action_count'] for e in all_actions),
    'cross_cutting_themes': dict(all_themes.most_common()),
    'personas': all_actions,
}

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f'Total personas: {len(all_actions)}')
print(f'Total actions: {output["total_actions"]}')
print(f'\nCross-cutting themes:')
for theme, count in all_themes.most_common():
    print(f'  {theme}: {count}/{len(all_actions)} personas affected')

print(f'\nSaved to: {OUTPUT}')
