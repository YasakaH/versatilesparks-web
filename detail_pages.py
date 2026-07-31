import fitz

pdf_path = r"E:\Hermes Projects\cookbook\dist-v2\index.pdf"
doc = fitz.open(pdf_path)

# Check pages 53-55 and 95-98 in detail
for target_page in [53, 54, 55, 95, 96, 97, 98]:
    page = doc[target_page - 1]
    page_w = page.rect.width
    page_h = page.rect.height
    
    print(f"\n{'='*60}")
    print(f"PAGE {target_page} (size: {page_w:.1f} x {page_h:.1f} pts = {page_w/72:.2f} x {page_h/72:.2f} in)")
    print(f"{'='*60}")
    
    # Get text with positions
    blocks = page.get_text("dict")["blocks"]
    
    worst = []
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            bbox = line["bbox"]
            x0, y0, x1, y1 = bbox
            text = "".join(span["text"] for span in line["spans"])
            
            if x1 > 360.5 or x0 < 60:
                # Only show significant overflows (>5pt) OR any code-like content
                overflow = x1 - 360 if target_page % 2 == 1 else x1 - 370.8
                if abs(overflow) > 3 or any(c in text for c in ['_', '(', '.', '=', '→']):
                    worst.append((x0, y0, x1, y1, text, overflow))
    
    worst.sort(key=lambda w: w[5], reverse=True)
    for x0, y0, x1, y1, text, ov in worst[:10]:
        print(f"  y={y0:.0f} x=[{x0:.1f},{x1:.1f}] ov={ov:+.1f}pt | {text[:90]}")
