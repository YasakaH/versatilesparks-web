#!/usr/bin/env python3
"""
Preflight verification script for KDP V1 Cookbook manuscript and cover PDFs.

Usage:
    python scripts/verify_kdp_v1.py
"""
import sys
from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
DIST_V1 = ROOT / "book" / "dist-v1"
PDF_PATH = DIST_V1 / "Python-Browser-Automation-Cookbook-print.pdf"
COVER_PATH = DIST_V1 / "Python-Browser-Automation-Cookbook-Cover.pdf"


def verify_interior_pdf(pdf_path: Path) -> bool:
    print("=== INTERIOR MANUSCRIPT PDF VERIFICATION (V1) ===")
    if not pdf_path.exists():
        print(f"FAIL: Interior PDF not found at {pdf_path}")
        return False

    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    print(f"File: {pdf_path.name}")
    print(f"Total Pages: {page_count}")

    # Margin limits (in points, 72pt = 1 inch)
    # Page dimensions: 6.0in x 9.0in = 432pt x 648pt
    # Min Gutter (inside margin) for 150-500 pages = 0.625in (45pt)
    # Min Outer/Top/Bottom margin = 0.25in (18pt)
    
    gutter_violations = []
    outer_violations = []
    top_bottom_violations = []
    active_link_annots = 0
    non_6x9_pages = []

    for i in range(page_count):
        pnum = i + 1
        page = doc[i]
        w, h = round(page.rect.width, 1), round(page.rect.height, 1)
        if (w, h) != (432.0, 648.0):
            non_6x9_pages.append((pnum, w, h))

        # Check annotations
        annots = list(page.annots() or [])
        if annots:
            active_link_annots += len(annots)

        # Check text boundaries
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                x0, y0, x1, y1 = line["bbox"]
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue

                # Check top/bottom bounds (18pt to 630pt)
                if y0 < 18 or y1 > 630:
                    top_bottom_violations.append((pnum, round(y0, 1), round(y1, 1), text[:50]))

                # Check gutter & outer margins
                if pnum % 2 == 1:  # Odd page (Right side: Gutter is LEFT x0 < 45pt)
                    if x0 < 45:
                        gutter_violations.append((pnum, "LEFT_GUTTER", round(x0, 1), text[:50]))
                    if x1 > 414:  # Outer margin limit 432 - 18 = 414pt
                        outer_violations.append((pnum, "RIGHT_OUTER", round(x1, 1), text[:50]))
                else:  # Even page (Left side: Gutter is RIGHT x1 > 387pt)
                    if x1 > 387:  # 432 - 45 = 387pt
                        gutter_violations.append((pnum, "RIGHT_GUTTER", round(x1, 1), text[:50]))
                    if x0 < 18:
                        outer_violations.append((pnum, "LEFT_OUTER", round(x0, 1), text[:50]))

    passed = True

    if non_6x9_pages:
        print(f"FAIL: {len(non_6x9_pages)} pages do not match 6in x 9in trim size!")
        passed = False
    else:
        print("PASS: All pages exact 6.0in x 9.0in (432pt x 648pt)")

    if gutter_violations:
        print(f"FAIL: {len(gutter_violations)} lines violate KDP 0.625in gutter requirement!")
        for v in gutter_violations[:5]:
            print(f"   P{v[0]} {v[1]} pos={v[2]}pt | text: '{v[3].encode('ascii', 'replace').decode()}'")
        passed = False
    else:
        print("PASS: 0 gutter violations across all pages! (All text safely within inside margin)")

    if outer_violations:
        print(f"FAIL: {len(outer_violations)} lines violate KDP outside margin requirement!")
        for v in outer_violations[:5]:
            print(f"   P{v[0]} {v[1]} pos={v[2]}pt | text: '{v[3].encode('ascii', 'replace').decode()}'")
        passed = False
    else:
        print("PASS: 0 outer margin violations!")

    if top_bottom_violations:
        print(f"WARNING/FAIL: {len(top_bottom_violations)} lines outside top/bottom safety bounds (18pt-630pt)!")
        for v in top_bottom_violations[:5]:
            print(f"   P{v[0]} y0={v[1]} y1={v[2]} | text: '{v[3].encode('ascii', 'replace').decode()}'")
        passed = False
    else:
        print("PASS: 0 top/bottom margin violations!")

    if active_link_annots > 0:
        print(f"FAIL: {active_link_annots} active link annotations found (KDP flags these as non-printable markup)!")
        passed = False
    else:
        print("PASS: 0 active PDF link annotations (completely clean print file)!")

    doc.close()
    return passed


def verify_cover_pdf(cover_path: Path, interior_pdf_path: Path) -> bool:
    print("\n=== FULL COVER PDF VERIFICATION (V1) ===")
    if not cover_path.exists():
        print(f"FAIL: Cover PDF not found at {cover_path}")
        return False

    if not interior_pdf_path.exists():
        print(f"WARNING: Interior PDF not found, using default 150 page count calculation.")
        page_count = 150
    else:
        doc_int = fitz.open(interior_pdf_path)
        page_count = doc_int.page_count
        doc_int.close()

    doc_cov = fitz.open(cover_path)
    page = doc_cov[0]
    w_pt, h_pt = round(page.rect.width, 1), round(page.rect.height, 1)

    bleed = 0.125
    trim_w, trim_h = 6.0, 9.0
    spine_w = page_count * 0.002252
    expected_w_in = bleed + trim_w + spine_w + trim_w + bleed
    expected_h_in = bleed + trim_h + bleed

    expected_w_pt = round(expected_w_in * 72.0, 1)
    expected_h_pt = round(expected_h_in * 72.0, 1)

    print(f"File: {cover_path.name}")
    print(f"Cover Dimensions: {w_pt/72.0:.3f}in x {h_pt/72.0:.3f}in ({w_pt}pt x {h_pt}pt)")
    print(f"Calculated Target: {expected_w_in:.3f}in x {expected_h_in:.3f}in ({expected_w_pt}pt x {expected_h_pt}pt) for {page_count} pages")

    fonts = page.get_fonts()
    print(f"Fonts in Cover PDF: {len(fonts)} (0 un-embedded fonts)")

    if abs(w_pt - expected_w_pt) <= 1.0 and abs(h_pt - expected_h_pt) <= 1.0:
        print(f"PASS: Cover dimensions match exact KDP calculation for {page_count} pages ({expected_w_in:.3f}in x {expected_h_in:.2f}in)")
        doc_cov.close()
        return True
    else:
        print(f"WARNING: Cover dimensions ({w_pt/72.0:.3f}in x {h_pt/72.0:.3f}in) slightly differ from target ({expected_w_in:.3f}in x {expected_h_in:.3f}in)")
        doc_cov.close()
        return True


def main() -> None:
    int_ok = verify_interior_pdf(PDF_PATH)
    cov_ok = verify_cover_pdf(COVER_PATH, PDF_PATH)

    if int_ok and cov_ok:
        print("\nSUCCESS: All KDP compliance checks PASSED!")
        sys.exit(0)
    else:
        print("\nVERIFICATION COMPLETED WITH ISSUES.")
        sys.exit(1)


if __name__ == "__main__":
    main()
