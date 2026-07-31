import fitz

ref = fitz.open(r'E:/Hermes Projects/cookbook/releases/v2.0.0/PDF/Browser-Automation-Playbook-v2.0.0.pdf')
print('=== REFERENCE PDF ===')
print(f'Pages: {ref.page_count}')
print(f'Metadata: {ref.metadata}')

# Fonts on first 5 pages
for pg in range(min(5, ref.page_count)):
    page = ref[pg]
    blocks = page.get_text('dict')['blocks']
    fonts_used = {}
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    key = (s['font'], s['size'])
                    if key not in fonts_used:
                        fonts_used[key] = s['text'][:50]
    print(f'\nPage {pg+1} fonts:')
    for (font, size), example in fonts_used.items():
        print(f'  {font} @ {size}pt: "{example}"')

# TOC
toc = ref.get_toc()
print(f'\nBookmarks: {len(toc)}')
for item in toc[:8]:
    print(f'  L{item[0]}: {item[1][:60]} -> p{item[2]}')

# Check chapter start styling
# Find 'Chapter' mentions
for pg in range(ref.page_count):
    text = ref[pg].get_text()
    if text.strip().startswith('Chapter') and len(text.strip().split('\n')) < 5:
        blocks = ref[pg].get_text('dict')['blocks']
        print(f'\n=== Page {pg+1} (chapter start) ===')
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    line_text = ''.join(s['text'] for s in l['spans'])
                    if line_text.strip():
                        font_info = [(s['font'], s['size']) for s in l['spans']]
                        print(f'  Fonts: {font_info[0] if font_info else "?"}')
                        print(f'  Text: "{line_text.strip()[:80]}"')
        break  # Just first chapter start

# Page size
page = ref[0]
rect = page.rect
print(f'\nPage dimensions: {rect.width:.0f} x {rect.height:.0f} points')
print(f'In inches: {rect.width/72:.2f} x {rect.height/72:.2f}')

ref.close()

# Compare with current
cur = fitz.open(r'E:/Hermes Projects/cookbook/book/v2/index.pdf')
print('\n=== CURRENT PDF ===')
print(f'Pages: {cur.page_count}')
for pg in range(min(3, cur.page_count)):
    page = cur[pg]
    blocks = page.get_text('dict')['blocks']
    fonts_used = {}
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    key = (s['font'], round(s['size'], 1))
                    if key not in fonts_used:
                        fonts_used[key] = s['text'][:50]
    print(f'\nPage {pg+1} fonts:')
    for (font, size), example in sorted(fonts_used.items()):
        print(f'  {font} @ {size}pt: "{example}"')

# Check chapter start in current
for pg in range(cur.page_count):
    text = cur[pg].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines and lines[0].startswith('Chapter') and len(lines) < 5:
        blocks = cur[pg].get_text('dict')['blocks']
        print(f'\n=== Current Page {pg+1} (chapter start) ===')
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    line_text = ''.join(s['text'] for s in l['spans'])
                    if line_text.strip():
                        font_info = [(s['font'], s['size']) for s in l['spans']]
                        print(f'  Font: {font_info[0] if font_info else "?"}')
                        print(f'  Text: "{line_text.strip()[:80]}"')
        break

page2 = cur[0]
rect2 = page2.rect
print(f'\nCurrent page dimensions: {rect2.width:.0f} x {rect2.height:.0f} points')
print(f'In inches: {rect2.width/72:.2f} x {rect2.height/72:.2f}')

cur.close()
