#!/usr/bin/env python3
"""
Build V2 Playbook PDF for KDP publishing.

Usage:
  python scripts/build_v2.py

Output:
  dist/Browser-Automation-Playbook.pdf   — final KDP-ready PDF
  releases/V2-Playbook.pdf               — release copy
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book" / "v2"
DIST = ROOT / "dist"
RELEASES = ROOT / "releases"

QUARTO = Path(r"C:\Users\varas\AppData\Local\Programs\Quarto\bin\quarto.exe")

OUTPUT_NAME = "Browser-Automation-Playbook.pdf"


def clean_build_artifacts() -> None:
    for pattern in ("*.tex", "*.aux", "*.log", "*.out", "*.toc", "*.lof", "*.lot",
                    "*.bbl", "*.blg", "*.bcf", "*.run.xml", "*.synctex.gz",
                    "*.fls", "*.fdb_latexmk", "*.xdv"):
        for p in BOOK.glob(pattern):
            try:
                p.unlink()
            except OSError:
                pass

    build_dir = BOOK / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir, ignore_errors=True)


def build_pdf() -> Path:
    if not QUARTO.exists():
        raise SystemExit(f"Quarto not found at {QUARTO}")

    cmd = [str(QUARTO), "render", "--to", "pdf"]
    print("Running:", " ".join(cmd), "in", BOOK)
    r = subprocess.run(cmd, cwd=str(BOOK))
    if r.returncode != 0:
        raise SystemExit(f"quarto render failed: {r.returncode}")

    # Find output PDF
    dist_v2 = BOOK.parent / "dist-v2"
    pdf = dist_v2 / f"{OUTPUT_NAME}"
    if not pdf.exists():
        found = list(dist_v2.glob("*.pdf"))
        if not found:
            raise SystemExit(f"No PDF produced in {dist_v2}")
        pdf = max(found, key=lambda p: p.stat().st_mtime)

    return pdf


def main() -> int:
    print("=== V2 Playbook PDF build ===")
    DIST.mkdir(parents=True, exist_ok=True)
    RELEASES.mkdir(parents=True, exist_ok=True)

    clean_build_artifacts()

    raw_pdf = build_pdf()
    print(f"Raw PDF: {raw_pdf}")

    # Copy to dist and releases
    targets = [
        DIST / OUTPUT_NAME,
        RELEASES / "V2-Playbook.pdf",
    ]
    for t in targets:
        try:
            shutil.copy2(raw_pdf, t)
            print(f"FINAL -> {t}")
        except OSError as e:
            alt = t.with_name(t.stem + "_new.pdf")
            shutil.copy2(raw_pdf, alt)
            print(f"FINAL (locked) -> {alt}: {e}")

    print(f"\nDone. PDF: {raw_pdf}")
    print(f"Size: {raw_pdf.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"Pages: (run pdfinfo or open in reader)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
