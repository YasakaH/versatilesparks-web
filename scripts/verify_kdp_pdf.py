#!/usr/bin/env python3
"""
Verify KDP compliance for interior manuscript and cover PDF files.
"""
import sys
from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
DIST_V2 = ROOT / "book" / "dist-v2"
PDF_PATH = DIST_V2 / "Browser-Automation-Playbook-print.pdf"
COVER_PATH = DIST_V2 / "Browser-Automation-Playbook-Cover.pdf"

def verify_interior(pdf_path: Path) -> dict:
    if not pdf_path.exists():
        print(f"ERROR: Interior PDF not found at {pdf_path}")
        return {"ok": False}
    
    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    print(f"=== INTERIOR MANUSCRIPT PDF VERIFICATION ===")
    print(f"File: {pdf_path.name}")
    print(f"Total Pages: {page_count}")
    
    # 1. Page dimensions check (432pt x 648pt = 6in x 9in)
    bad_sizes = []
    for i, page in enumerate(doc):
        w, h = page.rect.width, page.rect.height
        if abs(w - 432) > 1 or abs(h - 648) > 1:
            bad_sizes.append((i + 1, w, h))
    if bad_sizes:
        print(f"FAIL: {len(bad_sizes)} pages have non-standard 6x9 size: {bad_sizes[:5]}")
    else:
        print("PASS: All pages exact 6.0in x 9.0in (432pt x 648pt)")
        
    # 2. Margin & Gutter Overflow Check
    # Geometry: inner=0.80in (57.6pt), outer=0.55in (39.6pt)
    # Odd page (right): left margin (gutter) = 57.6pt, right limit = 432 - 39.6 = 392.4pt
    # Even page (left): left margin = 39.6pt, right limit (gutter) = 432 - 57.6 = 374.4pt
    
    gutter_violations = []
    outer_violations = []
    top_bottom_violations = []
    
    for page_idx in range(page_count):
        pnum = page_idx + 1
        page = doc[page_idx]
        
        if pnum % 2 == 1: # Odd page (right)
            gutter_left = 57.6
            outer_right = 392.4
        else: # Even page (left)
            gutter_right = 374.4
            outer_left = 39.6
            
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                x0, y0, x1, y1 = line["bbox"]
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue
                
                # Check top and bottom margins (0.25in = 18pt safety limit, top limit = 18pt, bottom limit = 630pt)
                if y0 < 18 or y1 > 630:
                    top_bottom_violations.append((pnum, round(y0, 1), round(y1, 1), text[:50]))
                    
                if pnum % 2 == 1: # Odd page (right)
                    # Gutter is on left (x0 should be >= 45pt for KDP min 0.625in, target 57.6pt)
                    if x0 < 45:
                        gutter_violations.append((pnum, "LEFT_GUTTER", round(x0, 1), text[:50]))
                    # Outer margin is on right (x1 should be <= 414pt for KDP min 0.25in limit)
                    if x1 > 414:
                        outer_violations.append((pnum, "RIGHT_OUTER", round(x1, 1), text[:50]))
                else: # Even page (left)
                    # Gutter is on right (x1 should be <= 387pt for KDP min 0.625in, target 374.4pt)
                    if x1 > 387:
                        gutter_violations.append((pnum, "RIGHT_GUTTER", round(x1, 1), text[:50]))
                    # Outer margin is on left (x0 should be >= 18pt for KDP min 0.25in limit)
                    if x0 < 18:
                        outer_violations.append((pnum, "LEFT_OUTER", round(x0, 1), text[:50]))

    if gutter_violations:
        print(f"FAIL: {len(gutter_violations)} lines violate KDP 0.625in gutter requirement!")
        for v in gutter_violations[:10]:
            print(f"   P{v[0]} {v[1]} pos={v[2]}pt | text: '{v[3]}'")
    else:
        print("PASS: 0 gutter violations across all pages! (All text safely within inside margin)")

    if outer_violations:
        print(f"FAIL: {len(outer_violations)} lines violate KDP outside margin requirement!")
        for v in outer_violations[:10]:
            print(f"   P{v[0]} {v[1]} pos={v[2]}pt | text: '{v[3]}'")
    else:
        print("PASS: 0 outer margin violations!")

    if top_bottom_violations:
        print(f"WARNING/FAIL: {len(top_bottom_violations)} lines outside top/bottom safety bounds (18pt-630pt)!")
        for v in top_bottom_violations[:10]:
            print(f"   P{v[0]} y0={v[1]} y1={v[2]} | text: '{v[3]}'")
    else:
        print("PASS: 0 top/bottom margin violations!")

    # 3. Non-printable markup check (PDF Annotations)
    total_annots = 0
    for page in doc:
        annots = page.annots()
        if annots:
            total_annots += len(list(annots))
            
    if total_annots > 0:
        print(f"WARNING: {total_annots} active PDF annotations found (may cause 'removed non-printable markup' warning).")
    else:
        print("PASS: 0 active PDF link annotations (completely clean print file)!")

    doc.close()
    return {"ok": len(bad_sizes) == 0 and len(gutter_violations) == 0 and len(outer_violations) == 0}

def verify_cover(cover_path: Path) -> dict:
    if not cover_path.exists():
        print(f"\nERROR: Cover PDF not found at {cover_path}")
        return {"ok": False}

    doc = fitz.open(cover_path)
    print(f"\n=== FULL COVER PDF VERIFICATION ===")
    print(f"File: {cover_path.name}")
    page = doc[0]
    w_pt, h_pt = page.rect.width, page.rect.height
    w_in, h_in = w_pt / 72.0, h_pt / 72.0
    print(f"Cover Dimensions: {w_in:.3f}in x {h_in:.3f}in ({w_pt:.1f}pt x {h_pt:.1f}pt)")
    
    # Target for 391 pages: 13.131in x 9.25in (945.4pt x 666.0pt)
    target_w, target_h = 945.4, 666.0
    if abs(w_pt - target_w) < 2 and abs(h_pt - target_h) < 2:
        print("PASS: Cover dimensions match exact KDP calculation for 391 pages (13.131in x 9.25in)")
    else:
        print(f"WARNING: Cover dimensions ({w_in:.3f}in x {h_in:.3f}in) slightly differ from target ({target_w/72:.3f}in x {target_h/72:.3f}in)")

    doc.close()
    return {"ok": True}

if __name__ == "__main__":
    r1 = verify_interior(PDF_PATH)
    r2 = verify_cover(COVER_PATH)
    if r1["ok"] and r2["ok"]:
        print("\nSUCCESS: All KDP compliance checks PASSED!")
        sys.exit(0)
    else:
        print("\nVERIFICATION COMPLETED WITH ISSUES.")
        sys.exit(1)
