import fitz  # PyMuPDF
import json

pdf_path = r"E:\Hermes Projects\cookbook\dist-v2\index.pdf"
doc = fitz.open(pdf_path)

# Page is 6x9 inches = 432x648 points (1 inch = 72 points)
# Text column: inner=1.0in (gutter), outer=0.85in, top=0.5in, bottom=0.5in
# For a right-side page (odd page number): left margin=0.85, right margin=1.0
# For a left-side page (even page number): left margin=1.0, right margin=0.85
# Text width = 6 - 0.85 - 1.0 = 4.15 inches = 298.8 points
# Page width = 432 points

# Text area boundaries:
# Right page (odd): x0=0.85*72=61.2, x1=432-1.0*72=360
# Left page (even): x0=1.0*72=72, x1=432-0.85*72=370.8

overflow_pages = []

for page_num in range(doc.page_count):
    page = doc[page_num]
    page_num_1based = page_num + 1
    
    # Determine text area boundaries for this page
    if page_num_1based % 2 == 1:  # odd = right page
        text_x0 = 61.2
        text_x1 = 360.0
    else:  # even = left page
        text_x0 = 72.0
        text_x1 = 370.8
    
    # Get all text blocks with positions
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if "lines" not in block:
            continue
        
        for line in block["lines"]:
            bbox = line["bbox"]  # [x0, y0, x1, y1]
            x0, y0, x1, y1 = bbox
            
            # Check if text extends beyond right margin
            if x1 > text_x1 + 2:  # 2pt tolerance
                text = ""
                for span in line["spans"]:
                    text += span["text"]
                
                overflow_pages.append({
                    "page": page_num_1based,
                    "x0": round(x0, 1),
                    "x1": round(x1, 1),
                    "right_limit": round(text_x1, 1),
                    "overflow_pt": round(x1 - text_x1, 1),
                    "text": text[:120]
                })
            
            # Check if text extends beyond LEFT margin (into gutter or off-page)
            if x0 < text_x0 - 5:  # 5pt tolerance for left
                text = ""
                for span in line["spans"]:
                    text += span["text"]
                
                overflow_pages.append({
                    "page": page_num_1based,
                    "issue": "LEFT_OVERFLOW",
                    "x0": round(x0, 1),
                    "left_limit": round(text_x0, 1),
                    "overflow_pt": round(text_x0 - x0, 1),
                    "text": text[:120]
                })

# Summary
print(f"Total pages checked: {doc.page_count}")
print(f"Total overflow issues: {len(overflow_pages)}")

# Group by page
from collections import Counter
page_counts = Counter(o["page"] for o in overflow_pages)
print(f"\nPages with overflow (top 20):")
for page, count in page_counts.most_common(20):
    print(f"  Page {page}: {count} lines overflow")

# Show details for pages 53, 54, 55
for target in [53, 54, 55, 95, 96, 97, 98]:
    matching = [o for o in overflow_pages if o["page"] == target]
    if matching:
        print(f"\n=== Page {target} ===")
        for o in matching[:5]:
            print(f"  x1={o.get('x1','?')} limit={o.get('right_limit','?')} overflow={o.get('overflow_pt','?')}pt")
            print(f"  text: {o['text'][:100]}")
