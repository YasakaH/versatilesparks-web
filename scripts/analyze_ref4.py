import fitz

ref = fitz.open(r'E:/Hermes Projects/cookbook/releases/v2.0.0/PDF/Browser-Automation-Playbook-v2.0.0.pdf')

# Check page 16 (first chapter start from bookmarks)
pg = 15  # 0-indexed
blocks = ref[pg].get_text('dict')['blocks']
print(f'REFERENCE Page {pg+1}:')
for b in blocks:
    if 'lines' in b:
        for l in b['lines']:
            y = l['bbox'][1]
            t = ''.join(s['text'] for s in l['spans'])
            if t.strip():
                font = l['spans'][0]['font']
                size = l['spans'][0]['size']
                print(f'  y={y:.0f} font={font} size={size:.1f} "{t.strip()[:80]}"')

# Also check a later chapter start (e.g., chapter 2)
# Find "2" on its own line
for pg_i in range(16, ref.page_count):
    text = ref[pg_i].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines and lines[0] in ('2',) and len(lines) > 1:
        blocks = ref[pg_i].get_text('dict')['blocks']
        print(f'\nREFERENCE Chapter 2 start - Page {pg_i+1}:')
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
