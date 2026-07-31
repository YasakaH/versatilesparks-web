"""Regenerate all images with premium SD3 prompts."""
import requests, base64, json, os

with open(r'C:\Users\varas\AppData\Local\hermes\.env', 'r') as f:
    for line in f:
        if 'STABILITY' in line and '=' in line:
            key = line.strip().split('=', 1)[1]
            break

url = 'https://api.stability.ai/v2beta/stable-image/generate/sd3'
DIR = 'C:/Users/varas/personalities/cookbook/images/'
PRESET = 'digital-art'

images = [
    ('hero.png', '''Dark navy geometric abstract background, deep indigo to almost black gradient, subtle thin grid lines receding into darkness. Flowing cyan neon light trails forming abstract data stream patterns. Small amber accent light particles. Clean minimal composition with generous negative space. Professional book cover background. No text. No objects. No robots. Cinematic lighting. 8K quality. Premium corporate aesthetic.'''),

    ('selector_hierarchy.png', '''Clean 5-layer pyramid diagram, dark navy background, each layer rendered as a floating horizontal bar. Top bar glows cyan, second bar green, third teal, fourth amber, bottom bar red. Bars decrease in width from top to bottom forming pyramid. Connecting vertical lines between bars. Minimal tech diagram style. No text. No labels. Geometric precision. Same color palette as Stripe docs. Soft subtle glow on edges.'''),

    ('stop_vs_retry_flow.png', '''Clean decision flowchart on dark navy background. Single entry point node at top, diamond decision node below. Two paths: right path in red leads to stop block, left path in green leads to retry loop. Retry loop shows arrow cycling back to decision diamond with a small counter icon. Minimal flowchart style. No text. No labels. Clean node outlines with subtle inner glow. Vercel-like technical illustration quality.'''),

    ('pagination_safety.png', '''Three parallel horizontal bars on dark navy background. First bar cyan, second bar amber, third bar red. All three arrows converge rightward into a single vertical stop bar glowing red. Clean minimal diagram. No text. No labels. Geometric precision. Straight lines and right angles only. Small X icons near each bar suggesting termination conditions. Premium tech doc style.'''),

    ('download_lifecycle.png', '''Horizontal 5-stage pipeline on dark navy background. Five connected nodes in sequence: first cyan circle representing click, then amber square for temp file, amber square for growing file, green square for rename, green circle with checkmark for done. Connecting arrows between stages. Clean minimal pipeline diagram. No text. No labels. Same visual language as Linear's documentation diagrams.'''),
]

for name, prompt in images:
    print(f'Generating {name}...', end=' ', flush=True)
    resp = requests.post(url,
        headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json'},
        files={
            'prompt': (None, prompt),
            'output_format': (None, 'png'),
            'aspect_ratio': (None, '16:9'),
            'style_preset': (None, PRESET),
            'cfg_scale': (None, '7'),
        },
        timeout=120
    )
    if resp.status_code == 200:
        data = resp.json()
        img = base64.b64decode(data['image'])
        path = f'{DIR}{name}'
        with open(path, 'wb') as f:
            f.write(img)
        print(f'OK ({len(img)} bytes)')
    else:
        print(f'FAILED: {resp.status_code}')
        # Check if rate limited
        print(resp.text[:200])
