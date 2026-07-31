import fitz

ref = fitz.open(r'E:/Hermes Projects/cookbook/releases/v2.0.0/PDF/Browser-Automation-Playbook-v2.0.0.pdf')

# Check pages 17-18 for chapter 1
for pg in [16, 17, 18, 19]:
    if pg >= ref.page_count:
        break
    blocks = ref[pg].get_text('dict')['blocks']
    print(f'REFERENCE Page {pg+1}:')
    lines_out = []
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                y = l['bbox'][1]
                t = ''.join(s['text'] for s in l['spans'])
                if t.strip():
                    font = l['spans'][0]['font']
                    size = l['spans'][0]['size']
                    lines_out.append((y, font, size, t.strip()))
    lines_out.sort(key=lambda x: x[0])
    for y, font, size, t in lines_out[:20]:
        is_bold = 'Bold' in font
        marker = ' [B]' if is_bold else ''
        print(f'  y={y:.0f} {font}{marker} sz={size:.1f} "{t[:80]}"')
    if len(lines_out) > 20:
        print(f'  ... ({len(lines_out)} total lines)')
    print()

# Also check a standard chapter (e.g., around pg 30-40)
for pg in range(25, 50):
    text = ref[pg].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines and lines[0].startswith('Chapter') and 'The Browser' in text:
        blocks = ref[pg].get_text('dict')['blocks']
        print(f'REFERENCE Chapter 2 start - Page {pg+1}:')
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    y = l['bbox'][1]
                    t = ''.join(s['text'] for s in l['spans'])
                    if t.strip():
                        font = l['spans'][0]['font']
                        size = l['spans'][0]['size']
                        print(f'  y={y:.0f} font={font} size={size:.1f} "{t.strip()[:80]}"')
        break

ref.close()
print('\n---')
# Check current PDF chapter 2 start
cur = fitz.open(r'E:/Hermes Projects/cookbook/book/v2/index.pdf')
for pg in range(cur.page_count):
    text = cur[pg].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines and lines[0] in ('2',) and len(lines) > 2:
        blocks = cur[pg].get_text('dict')['blocks']
        print(f'CURRENT Chapter 2 - Page {pg+1}:')
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    y = l['bbox'][1]
                    t = ''.join(s['text'] for s in l['spans'])
                    if t.strip():
                        font = l['spans'][0]['font']
                        size = l['spans'][0]['size']
                        print(f'  y={y:.0f} font={font} size={size:.1f} "{t.strip()[:80]}"')
        break
cur.close()
