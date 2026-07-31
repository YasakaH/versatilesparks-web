import fitz

ref = fitz.open(r'E:/Hermes Projects/cookbook/releases/v2.0.0/PDF/Browser-Automation-Playbook-v2.0.0.pdf')

for pg in range(ref.page_count):
    text = ref[pg].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        continue
    first = lines[0]
    if first in ('1',) and len(lines) > 1 and 'Automation' in lines[1]:
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
                        print(f'  y={y:.0f} font={font} size={size:.1f} "{t.strip()[:70]}"')
        break

ref.close()

cur = fitz.open(r'E:/Hermes Projects/cookbook/book/v2/index.pdf')
for pg in range(cur.page_count):
    text = cur[pg].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        continue
    first = lines[0]
    if first in ('1',) and len(lines) > 1 and 'Browser Automa' in lines[1]:
        blocks = cur[pg].get_text('dict')['blocks']
        print(f'\nCURRENT Page {pg+1}:')
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    y = l['bbox'][1]
                    t = ''.join(s['text'] for s in l['spans'])
                    if t.strip():
                        font = l['spans'][0]['font']
                        size = l['spans'][0]['size']
                        print(f'  y={y:.0f} font={font} size={size:.1f} "{t.strip()[:70]}"')
        break

cur.close()
