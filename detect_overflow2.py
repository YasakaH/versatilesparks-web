import fitz
from collections import Counter

pdf_path = r"E:\Hermes Projects\cookbook\dist-v2\index.pdf"
doc = fitz.open(pdf_path)

overflow_pages = []

for page_num in range(doc.page_count):
    page = doc[page_num]
    page_1 = page_num + 1
    page_w = page.rect.width  # 432
    page_h = page.rect.height  # 648
    
    # Correct text area boundaries:
    # Odd page (right side): inner/gutter on LEFT, outer on RIGHT
    #   left=72pt, right=370.8pt (432-61.2), text_width=298.8pt
    # Even page (left side): outer on LEFT, inner/gutter on RIGHT
    #   left=61.2pt, right=360pt (432-72), text_width=298.8pt
    # Running headers use headwidth which may be different
    
    if page_1 % 2 == 1:  # odd = right page
        text_x0 = 72.0
        text_x1 = 370.8
    else:  # even = left page
        text_x0 = 61.2
        text_x1 = 360.0
    
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            bbox = line["bbox"]
            x0, y0, x1, y1 = bbox
            text = "".join(span["text"] for span in line["spans"])
            
            # REAL overflow: text extends beyond right text boundary by >5pt
            if x1 > text_x1 + 5:
                overflow_pages.append({
                    "page": page_1,
                    "x0": round(x0, 1),
                    "x1": round(x1, 1),
                    "limit": round(text_x1, 1),
                    "overflow_pt": round(x1 - text_x1, 1),
                    "overflow_in": round((x1 - text_x1) / 72, 2),
                    "y": round(y0, 1),
                    "text": text[:150]
                })
            
            # Check off-page overflow (beyond physical page width - safety margin)
            if x1 > page_w - 20:  # within 20pt of edge = dangerous
                overflow_pages.append({
                    "page": page_1,
                    "issue": "NEAR_PAGE_EDGE",
                    "x1": round(x1, 1),
                    "page_w": page_w,
                    "text": text[:150]
                })

print(f"Total REAL overflow issues (>5pt): {len(overflow_pages)}")
print(f"Pages with overflow: {len(set(o['page'] for o in overflow_pages))}")

# Group by page
page_counts = Counter(o["page"] for o in overflow_pages)
print(f"\nAll pages with overflow (sorted by count):")
for pg, cnt in page_counts.most_common(30):
    examples = [o for o in overflow_pages if o["page"] == pg]
    worst = max(examples, key=lambda o: o.get("overflow_pt", 0))
    print(f"  Page {pg}: {cnt} lines, worst={worst.get('overflow_pt',0):.1f}pt ({worst.get('overflow_in',0):.2f}in)")

# Show worst overflows across whole book
print(f"\nWORST 20 overflows in entire book:")
sorted_ov = sorted(overflow_pages, key=lambda o: o.get("overflow_pt", 0), reverse=True)
for o in sorted_ov[:20]:
    print(f"  P{o['page']} y={o.get('y','?')} ov={o.get('overflow_pt','?'):+.1f}pt | {o['text'][:100]}")
