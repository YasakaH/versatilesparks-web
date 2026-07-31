#!/usr/bin/env python3
"""
Build KDP-Compliant Interior PDF and Full Cover PDF for Browser Automation Playbook (v2).

Usage:
    python scripts/build_kdp_v2.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
BOOK_V2 = ROOT / "book" / "v2"
DIST_V2 = ROOT / "book" / "dist-v2"
DIST = ROOT / "dist"
RELEASES_V2 = ROOT / "releases" / "v2.0.0" / "PDF"

QUARTO = Path(r"C:\Users\varas\AppData\Local\Programs\Quarto\bin\quarto.exe")
FONT_TITLE = r"C:\Windows\Fonts\segoeuil.ttf"
FONT_BODY = r"C:\Windows\Fonts\segoeui.ttf"


def clean_artifacts() -> None:
    for pattern in ("*.aux", "*.log", "*.out", "*.toc", "*.fls", "*.fdb_latexmk", "*.xdv"):
        for p in BOOK_V2.glob(pattern):
            try:
                p.unlink()
            except OSError:
                pass


def build_quarto_pdf() -> Path:
    if not QUARTO.exists():
        raise SystemExit(f"Quarto executable not found at {QUARTO}")

    print("=== Step 1: Running Quarto Render ===")
    cmd = [str(QUARTO), "render", "--to", "pdf"]
    print("Executing:", " ".join(cmd), "in", BOOK_V2)
    res = subprocess.run(cmd, cwd=str(BOOK_V2))
    if res.returncode != 0:
        raise SystemExit(f"Quarto render failed with return code {res.returncode}")

    pdf_file = DIST_V2 / "Browser-Automation-Playbook.pdf"
    if not pdf_file.exists():
        cands = [p for p in DIST_V2.glob("*.pdf") if "Cover" not in p.name and "print" not in p.name]
        if not cands:
            raise SystemExit(f"No manuscript PDF found in {DIST_V2}")
        pdf_file = max(cands, key=lambda p: p.stat().st_mtime)

    return pdf_file


def sanitize_interior_pdf(src_pdf: Path, dest_pdf: Path) -> int:
    """
    Strips active PDF annotations (/Annots) to prevent KDP's
    'removed non-printable markup' warning.
    """
    print(f"\n=== Step 2: Sanitizing Interior PDF (Removing PDF Annotations/Markup) ===")
    doc = fitz.open(src_pdf)
    total_stripped = 0
    pages_modified = []

    for i in range(doc.page_count):
        page = doc[i]
        annots = list(page.annots() or [])
        if annots:
            for annot in annots:
                page.delete_annot(annot)
                total_stripped += 1
                
        # Deep cleanup: clear /Annots key from low-level page xref dictionary
        page_obj = doc.xref_object(page.xref)
        if "/Annots" in page_obj:
            doc.xref_set_key(page.xref, "Annots", "[]")
            pages_modified.append(i + 1)

    tmp_out = dest_pdf.with_name(dest_pdf.stem + "_tmp.pdf")
    doc.save(tmp_out, garbage=4, deflate=True, clean=True)
    page_count = doc.page_count
    doc.close()
    
    if tmp_out.exists():
        if dest_pdf.exists():
            try:
                dest_pdf.unlink()
            except OSError:
                pass
        shutil.move(tmp_out, dest_pdf)

    print(f"Sanitized interior PDF saved to: {dest_pdf}")
    print(f"Total pages: {page_count}, Stripped link annotations on {len(pages_modified)} pages.")
    return page_count


def generate_kdp_cover(page_count: int, output_cover_pdf: Path) -> Path:
    """
    Generates a 300 DPI KDP Print Cover PDF (Back + Spine + Front + Bleed).
    
    Specifications for 6" x 9" Trim Size:
    - Page height = 9.0" + 0.25" bleed = 9.25" (666.0 pt)
    - Page width = 0.125" bleed + 6.0" back + spine_width + 6.0" front + 0.125" bleed
    - Spine width for 342 pages = 342 * 0.002252" = 0.770" (55.44 pt)
    - Total Full Cover Width = 13.020" (937.44 pt)
    """
    from PIL import Image, ImageDraw, ImageFont

    print(f"\n=== Step 3: Generating KDP Full Cover PDF (Page count: {page_count}) ===")
    
    bleed = 0.125  # in
    trim_w = 6.0   # in
    trim_h = 9.0   # in
    spine_w = page_count * 0.002252  # in (~0.770in for 342p)
    
    full_w_in = bleed + trim_w + spine_w + trim_w + bleed  # 13.020 in
    full_h_in = bleed + trim_h + bleed                     # 9.25 in
    
    dpi = 300
    full_w_px = int(round(full_w_in * dpi))  # ~3906 px
    full_h_px = int(round(full_h_in * dpi))  # ~2775 px

    bleed_px = int(round(bleed * dpi))
    trim_w_px = int(round(trim_w * dpi))
    spine_w_px = int(round(spine_w * dpi))

    spine_x0_px = bleed_px + trim_w_px
    spine_x1_px = spine_x0_px + spine_w_px
    front_x0_px = spine_x1_px

    NAVY_RGB = (5, 11, 26)
    WHITE_RGB = (255, 255, 255)

    # 1. Base Canvas
    canvas = Image.new("RGB", (full_w_px, full_h_px), WHITE_RGB)

    # 2. Spine Area
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([spine_x0_px, 0, spine_x1_px, full_h_px], fill=NAVY_RGB)

    # 3. Front Cover Image
    front_img_path = BOOK_V2 / "Images" / "cover-front.png"
    if front_img_path.exists():
        im_front = Image.open(front_img_path).convert("RGB")
        front_target_w = full_w_px - front_x0_px
        front_target_h = full_h_px
        
        # Scale to leave top/bottom safe margin (50px top, 100px bottom)
        scale = min((front_target_w - 40) / im_front.width, (front_target_h - 150) / im_front.height)
        new_w = int(round(im_front.width * scale))
        new_h = int(round(im_front.height * scale))
        
        im_front_resized = im_front.resize((new_w, new_h), Image.Resampling.LANCZOS)
        paste_x = front_x0_px + (front_target_w - new_w) // 2
        paste_y = 50
        
        canvas.paste(im_front_resized, (paste_x, paste_y))

    # 4. Back Cover Image
    back_img_path = BOOK_V2 / "Images" / "cover-back.png"
    if back_img_path.exists():
        im_back = Image.open(back_img_path).convert("RGB")
        back_target_w = spine_x0_px
        back_target_h = full_h_px
        
        scale = min((back_target_w - 40) / im_back.width, (back_target_h - 150) / im_back.height)
        new_w = int(round(im_back.width * scale))
        new_h = int(round(im_back.height * scale))
        
        im_back_resized = im_back.resize((new_w, new_h), Image.Resampling.LANCZOS)
        paste_x = (back_target_w - new_w) // 2
        paste_y = 50
        
        canvas.paste(im_back_resized, (paste_x, paste_y))

    # 5. Barcode Reservation Box (2.0" x 1.2")
    bar_w_px = int(round(2.0 * dpi))
    bar_h_px = int(round(1.2 * dpi))
    bar_x1_px = spine_x0_px - int(round(0.35 * dpi))
    bar_x0_px = bar_x1_px - bar_w_px
    bar_y1_px = full_h_px - int(round(0.35 * dpi))
    bar_y0_px = bar_y1_px - bar_h_px

    draw.rectangle([bar_x0_px, bar_y0_px, bar_x1_px, bar_y1_px], fill=WHITE_RGB, outline=(200, 200, 200), width=2)
    try:
        font_sm = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
    except OSError:
        font_sm = ImageFont.load_default()
    draw.text((bar_x0_px + 80, bar_y0_px + 160), "[ KDP BARCODE AREA ]", fill=(160, 160, 160), font=font_sm)

    # 6. Spine Text
    if spine_w >= 0.35:
        spine_title = "BROWSER AUTOMATION PLAYBOOK   —   Yasaka Hanini"
        try:
            font_spine = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 38)
        except OSError:
            font_spine = ImageFont.load_default()
            
        txt_img = Image.new("RGBA", (int(full_h_px * 0.75), 60), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((0, 0), spine_title, fill=(245, 245, 245, 255), font=font_spine)
        
        txt_rot = txt_img.rotate(270, expand=True)
        
        spine_center_x = (spine_x0_px + spine_x1_px) // 2
        paste_spine_x = spine_center_x - txt_rot.width // 2
        paste_spine_y = (full_h_px - txt_rot.height) // 2
        
        canvas.paste(txt_rot, (paste_spine_x, paste_spine_y), txt_rot)

    # Save Cover PDF
    canvas.save(output_cover_pdf, "PDF", resolution=300.0)
    print(f"KDP Cover PDF generated at: {output_cover_pdf}")
    print(f"Cover Dimensions: {full_w_in:.3f}\" x {full_h_in:.3f}\"")
    return output_cover_pdf


def main() -> int:
    print("=== Starting KDP PDF Package Build for V2 Playbook ===")
    DIST_V2.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    RELEASES_V2.mkdir(parents=True, exist_ok=True)

    clean_artifacts()

    # Build raw PDF with Quarto
    raw_pdf = build_quarto_pdf()
    
    # Sanitize interior PDF for KDP
    final_interior_pdf = DIST_V2 / "Browser-Automation-Playbook-print.pdf"
    page_count = sanitize_interior_pdf(raw_pdf, final_interior_pdf)
    
    # Generate Full KDP Cover PDF
    final_cover_pdf = DIST_V2 / "Browser-Automation-Playbook-Cover.pdf"
    generate_kdp_cover(page_count, final_cover_pdf)

    # Copy output files to release & dist directories
    targets = [
        (final_interior_pdf, DIST / "Browser-Automation-Playbook-print.pdf"),
        (final_cover_pdf, DIST / "Browser-Automation-Playbook-Cover.pdf"),
        (final_interior_pdf, RELEASES_V2 / "Browser-Automation-Playbook-print.pdf"),
        (final_cover_pdf, RELEASES_V2 / "Browser-Automation-Playbook-Cover.pdf"),
    ]

    for src_f, dest_f in targets:
        dest_f.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src_f, dest_f)
            print(f"COPIED -> {dest_f}")
        except (PermissionError, OSError) as e:
            alt_f = dest_f.with_name(dest_f.stem + "_new.pdf")
            try:
                shutil.copy2(src_f, alt_f)
                print(f"COPIED (locked destination {dest_f.name}) -> {alt_f.name}")
            except OSError:
                print(f"WARNING: Could not copy to {dest_f}: {e}")

    print("\n=== BUILD COMPLETE ===")
    print(f"Interior Manuscript PDF: {final_interior_pdf}")
    print(f"Full KDP Cover PDF:       {final_cover_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
