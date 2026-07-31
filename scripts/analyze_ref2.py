import fitz

ref = fitz.open(r'E:/Hermes Projects/cookbook/releases/v2.0.0/PDF/Browser-Automation-Playbook-v2.0.0.pdf')
cur = fitz.open(r'E:/Hermes Projects/cookbook/book/v2/index.pdf')

def analyze_chapter_start(pdf, name):
    # Find chapter start pages
    for pg in range(pdf.page_count):
        text = pdf[pg].get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if not lines:
            continue
        # Check if this page starts with "Chapter" or "1"
        first = lines[0]
        if first.startswith('Chapter') or (first.startswith('1') and 'Automation' in text):
            blocks = pdf[pg].get_text('dict')['blocks']
            print(f'\n=== {name} - Page {pg+1} first lines: ===')
            for i, l in enumerate(lines[:8]):
                print(f'  {l[:80]}')
            
            # Get y-positions of content
            print(f'\n  Block structure (y-positions):')
            for b in blocks:
                if 'lines' in b:
                    for l in b['lines']:
                        y = l['bbox'][1]  # top y
                        text = ''.join(s['text'] for s in l['spans'])
                        if text.strip():
                            font = l['spans'][0]['font']
                            size = l['spans'][0]['size']
                            print(f'  y={y:.0f} font={font} size={size:.1f} "{text.strip()[:60]}"')
            break

analyze_chapter_start(ref, 'REFERENCE')
analyze_chapter_start(cur, 'CURRENT')

# Also check page dimensions and margins
print('\n=== Margins analysis ===')
for pdf, name in [(ref, 'REFERENCE'), (cur, 'CURRENT')]:
    page = pdf[0]
    rect = page.rect
    # Get first text block position
    blocks = page.get_text('dict')['blocks']
    text_blocks = [b for b in blocks if 'lines' in b and any(l['spans'][0]['text'].strip() for l in b['lines'])]
    
    print(f'\n{name} ({rect.width/72:.1f}x{rect.height/72:.1f} in):')
    if text_blocks:
        first = text_blocks[0]
        x0, y0, x1, y1 = first['bbox']
        print(f'  First text block: left={x0:.0f} top={y0:.0f} right={x1:.0f} bottom={y1:.0f}')
        print(f'  Margins: left={x0:.0f}pt top={y0:.0f}pt right={rect.width-x1:.0f}pt bottom={rect.height-y1:.0f}pt')

ref.close()
cur.close()
