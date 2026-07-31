"""Regenerate all images with ChatGPT-optimized premium prompts."""
import requests, base64

with open(r'C:\Users\varas\AppData\Local\hermes\.env', 'r') as f:
    for line in f:
        if 'STABILITY' in line and '=' in line:
            key = line.strip().split('=', 1)[1]
            break

url = 'https://api.stability.ai/v2beta/stable-image/generate/sd3'
DIR = 'C:/Users/varas/personalities/cookbook/images/'
PRESET = 'digital-art'
CFG = '7'

# Global style prefix
PREFIX = '''Premium technical editorial illustration for a high-end Python automation engineering cookbook.
Dark navy visual system (#050B1A), deep graphite shadows, subtle indigo gradients, cyan primary highlights, controlled amber accents.
Style inspired by Linear, Vercel, Stripe developer documentation, Apple technical diagrams.
Minimal but sophisticated. Precision-engineered feel. Clean geometric forms. Soft volumetric lighting. Glassmorphism surfaces. Thin luminous edges. Professional enterprise software aesthetic.
Ultra high resolution, cinematic depth, realistic materials, sharp details.
No text, no labels, no letters, no numbers, no logos, no characters, no robots.'''

images = [
    ('hero.png',
     PREFIX + '''
A dark navy futuristic developer workspace atmosphere without showing computers or people.
Abstract visualization of automated browser workflows: multiple elegant cyan data streams flowing through a precise geometric network, representing navigation, extraction, and intelligent automation.
Subtle layered glass panels and architectural grid structures floating in space. Thin luminous paths converge toward a central intelligent workflow engine shape.
Deep indigo-to-black gradient background. Small controlled amber particles representing successful automation events.
Large clean negative space on the left and upper area for book typography.
Sophisticated enterprise technology aesthetic. Not sci-fi, not cyberpunk, not robots.
Cinematic lighting, realistic depth, premium software documentation quality.
16:9.'''),

    ('selector_hierarchy.png',
     PREFIX + '''
Premium technical architecture illustration showing a hierarchy of selector reliability.
Dark navy background. Five floating horizontal glass layers stacked vertically like an engineered ranking system.
Top layer: bright cyan transparent glass with strongest illumination.
Lower layers gradually become darker and less stable.
Each layer represented by different geometric material quality: top = precise crystal structure, middle = polished metal, bottom = fragmented unstable geometry.
Thin glowing connections showing progression from reliable to fragile.
The visual should communicate: stable automation contracts at the top, brittle implementation details at the bottom.
Professional developer documentation illustration. Linear/Vercel quality.
16:9.'''),

    ('stop_vs_retry_flow.png',
     PREFIX + '''
Premium engineering decision flow illustration.
Dark navy background. A single glowing cyan path enters from the top representing a failed automation operation.
At the center: a transparent glass decision node.
Two clearly separated outcomes:
Left path: controlled green circular retry loop, showing limited recovery cycles, clean engineering resilience.
Right path: red descending path ending in a stable stop state, representing safe termination.
Small visual indicators: clock symbol for temporary failures, warning symbol for permanent failures.
Balanced composition. Minimal geometric design.
Enterprise reliability engineering aesthetic. Stripe developer documentation quality.
16:9.'''),

    ('pagination_safety.png',
     PREFIX + '''
Premium workflow engineering illustration showing safe pagination control.
Dark navy background. Three independent automation safety mechanisms arranged horizontally:
First: cyan infinite-page detection mechanism.
Second: amber state verification checkpoint.
Third: red maximum safety boundary.
All three converge into a final glowing stop barrier.
Visual language: automation pipeline, controlled execution, preventing endless loops.
Glass panels, thin luminous edges, precision geometry.
High-end developer documentation illustration.
16:9.'''),

    ('download_lifecycle.png',
     PREFIX + '''
Premium software engineering pipeline illustration.
Dark navy background. A five-stage file processing pipeline represented visually.
Beginning: cyan browser interaction point.
Middle: amber temporary file state with subtle incomplete energy.
Next: file growth and processing visualization.
Next: green finalized file transformation.
End: clean completed state with a stable illuminated object.
Connected by elegant glowing pathways.
Communicate: temporary to processing to finalized.
Professional cloud infrastructure documentation aesthetic.
16:9.'''),
]

for name, prompt in images:
    print(f'{name}...', end=' ', flush=True)
    resp = requests.post(url,
        headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json'},
        files={
            'prompt': (None, prompt),
            'output_format': (None, 'png'),
            'aspect_ratio': (None, '16:9'),
            'style_preset': (None, PRESET),
            'cfg_scale': (None, CFG),
        },
        timeout=180
    )
    if resp.status_code == 200:
        img = base64.b64decode(resp.json()['image'])
        with open(f'{DIR}{name}', 'wb') as f:
            f.write(img)
        print(f'{len(img)} bytes')
    else:
        print(f'FAILED ({resp.status_code}): {resp.text[:100]}')
