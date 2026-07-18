#!/usr/bin/env python3
"""
Post-process V1 Quarto PDF:
  - Premium cover (art + typeset title with system fonts)
  - Drop nearly-empty pages
  - Copy to dist/, releases/, repo root
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
WIN_FONTS = Path(r"C:\Windows\Fonts")

ROOT_PDF = ROOT / "Python_Browser_Automation_Cookbook.pdf"
ROOT_PDF_V2 = ROOT / "Python_Browser_Automation_Cookbook_v2.pdf"
RELEASE_PDF = ROOT / "releases" / "V1-Foundation-Cookbook.pdf"

# Colors
NAVY = (0.020, 0.043, 0.102)  # #050B1A
NAVY_MID = (0.055, 0.10, 0.20)
CYAN = (0.133, 0.827, 0.933)  # #22D3EE
WHITE = (0.98, 0.985, 0.99)
SLATE = (0.72, 0.78, 0.86)
MUTED = (0.58, 0.64, 0.72)


def _font(*names: str) -> str:
    for n in names:
        p = WIN_FONTS / n
        if p.exists():
            return str(p)
    return ""


FONT_TITLE = _font("segoeuil.ttf", "calibril.ttf", "Candara.ttf")  # light display
FONT_TITLE_EMPH = _font("seguisb.ttf", "segoeuib.ttf", "calibrib.ttf")
FONT_BODY = _font("segoeui.ttf", "calibri.ttf")
FONT_META = _font("calibril.ttf", "segoeuil.ttf", "georgia.ttf")


def _resolve_cover_art() -> Path:
    for p in (
        BOOK / "images" / "hero_cover.png",
        ROOT / "images" / "hero_cover.png",
    ):
        if p.exists():
            return p
    return BOOK / "images" / "hero_cover.png"


HERO = _resolve_cover_art()


def find_pdf() -> Path:
    cands = []
    for d in [ROOT / "dist", BOOK / "dist"]:
        p = d / "Python-Browser-Automation-Cookbook.pdf"
        if p.exists():
            cands.append(p)
    if not cands:
        raise SystemExit("No raw Quarto PDF in dist/ — run: python scripts/build_v1.py")
    return max(cands, key=lambda p: p.stat().st_mtime)


def _text(
    page: fitz.Page,
    point: fitz.Point,
    text: str,
    *,
    fontsize: float,
    color: tuple,
    fontfile: str,
    fontname: str = "helv",
) -> None:
    kwargs = {
        "fontsize": fontsize,
        "color": color,
    }
    if fontfile:
        # unique fontname per file avoids clashes
        kwargs["fontfile"] = fontfile
        kwargs["fontname"] = "f_" + Path(fontfile).stem.replace("-", "_")[:28]
    else:
        kwargs["fontname"] = fontname
    page.insert_text(point, text, **kwargs)


def _place_cover_image(page: fitz.Page, path: Path) -> None:
    """Cover-mode: fill page, keep aspect, bias art to the right."""
    w, h = page.rect.width, page.rect.height
    pix = fitz.Pixmap(str(path))
    iw, ih = pix.width, pix.height
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    # Prefer showing right/lower art; leave more of left/top for type
    x0 = w - dw  # align right if wider; else slightly left of center
    if dw <= w:
        x0 = (w - dw) * 0.15  # slight left bias of image box → art stays right
    y0 = h - dh  # align bottom so browsers sit lower; empty sky on top
    if dh <= h:
        y0 = (h - dh) * 0.55  # push art slightly down
    rect = fitz.Rect(x0, y0, x0 + dw, y0 + dh)
    page.insert_image(rect, filename=str(path), keep_proportion=True)
    del pix


def build_cover(w: float, h: float) -> fitz.Document:
    """
    Premium cover layout (editorial book):
      - Soft painted gradient base
      - Full-bleed browser art (no title in image)
      - Title block high in empty upper-left (not mid-page over art)
      - Premium Windows fonts (Segoe UI Light / Semibold)
    """
    doc = fitz.open()
    page = doc.new_page(width=w, height=h)

    # 1) Premium base gradient (top-left dark → bottom-right slightly lifted navy)
    # Paint as horizontal+vertical soft bands
    steps = 48
    for i in range(steps):
        t = i / max(steps - 1, 1)
        # blend NAVY → NAVY_MID
        col = tuple(NAVY[j] * (1 - t) + NAVY_MID[j] * t for j in range(3))
        y0 = h * i / steps
        y1 = h * (i + 1) / steps + 0.5
        page.draw_rect(fitz.Rect(0, y0, w, y1), color=col, fill=col, width=0)

    # 2) Art layer — full cover, aspect preserved
    if HERO.exists():
        print(f"cover art: {HERO}")
        _place_cover_image(page, HERO)
    else:
        print(f"WARNING: missing {HERO}")

    # 3) Soft left/top type safety field (very light — art already has empty space)
    for i in range(20):
        t = i / 19
        opacity = 0.42 * (1 - t) ** 1.6
        x1 = w * 0.58 * (0.35 + 0.65 * t)
        shape = page.new_shape()
        shape.draw_rect(fitz.Rect(0, 0, x1, h * 0.72))
        shape.finish(color=NAVY, fill=NAVY, fill_opacity=opacity, width=0)
        shape.commit()

    # 4) Typography — UPPER LEFT (use the empty sky, not mid-page over windows)
    left = 52
    # Top margin ~12% of page — classic book title block
    y = h * 0.14

    # Title — large, light display face
    _text(
        page,
        fitz.Point(left, y),
        "Python Browser",
        fontsize=34,
        color=WHITE,
        fontfile=FONT_TITLE,
    )
    _text(
        page,
        fitz.Point(left, y + 44),
        "Automation Cookbook",
        fontsize=34,
        color=WHITE,
        fontfile=FONT_TITLE,
    )

    # Accent rule
    rule_y = y + 64
    page.draw_line(
        fitz.Point(left, rule_y),
        fitz.Point(left + 108, rule_y),
        color=CYAN,
        width=1.8,
    )

    # Subtitle
    _text(
        page,
        fitz.Point(left, rule_y + 32),
        "30 Production-Ready Recipes Using nodriver",
        fontsize=12.5,
        color=CYAN,
        fontfile=FONT_BODY,
    )

    # Tagline
    _text(
        page,
        fitz.Point(left, rule_y + 62),
        "Build browser automation that works",
        fontsize=11.5,
        color=SLATE,
        fontfile=FONT_META,
    )
    _text(
        page,
        fitz.Point(left, rule_y + 80),
        "the same on day 30 as on day 1.",
        fontsize=11.5,
        color=SLATE,
        fontfile=FONT_META,
    )

    # Author block — bottom left, clear of art
    _text(
        page,
        fitz.Point(left, h - 100),
        "Yasaka Hanini",
        fontsize=12.5,
        color=WHITE,
        fontfile=FONT_BODY,
    )
    _text(
        page,
        fitz.Point(left, h - 80),
        "Foundation  ·  2026",
        fontsize=11,
        color=MUTED,
        fontfile=FONT_META,
    )
    return doc


def build_back_cover(w: float, h: float) -> fitz.Document:
    """
    Simple back cover matching front: same navy gradient + soft art.
    No sales copy — title, author, edition, year only.
    """
    doc = fitz.open()
    page = doc.new_page(width=w, height=h)

    # Same base gradient as front
    steps = 48
    for i in range(steps):
        t = i / max(steps - 1, 1)
        col = tuple(NAVY[j] * (1 - t) + NAVY_MID[j] * t for j in range(3))
        y0 = h * i / steps
        y1 = h * (i + 1) / steps + 0.5
        page.draw_rect(fitz.Rect(0, y0, w, y1), color=col, fill=col, width=0)

    # Very faint art so it matches front without competing
    if HERO.exists():
        # Place art full-bleed then darken heavily
        _place_cover_image(page, HERO)
        shape = page.new_shape()
        shape.draw_rect(page.rect)
        shape.finish(color=NAVY, fill=NAVY, fill_opacity=0.78, width=0)
        shape.commit()

    # Centered, quiet type block
    cx = w / 2
    # helper: approximate text width via textbox center
    def center_line(y: float, text: str, size: float, color: tuple, fontfile: str) -> None:
        # use insert_textbox for true centering
        rect = fitz.Rect(w * 0.12, y - size, w * 0.88, y + size * 1.4)
        kwargs = {
            "fontsize": size,
            "color": color,
            "align": fitz.TEXT_ALIGN_CENTER,
        }
        if fontfile:
            kwargs["fontfile"] = fontfile
            kwargs["fontname"] = "fb_" + Path(fontfile).stem.replace("-", "_")[:28]
        else:
            kwargs["fontname"] = "helv"
        page.insert_textbox(rect, text, **kwargs)

    mid = h * 0.42
    center_line(mid, "Python Browser Automation Cookbook", 16, WHITE, FONT_TITLE)
    # thin rule
    page.draw_line(
        fitz.Point(cx - 48, mid + 28),
        fitz.Point(cx + 48, mid + 28),
        color=CYAN,
        width=1.2,
    )
    center_line(mid + 52, "Foundation", 12, MUTED, FONT_META)
    center_line(mid + 78, "Yasaka Hanini  ·  2026", 11, MUTED, FONT_BODY)

    return doc


def _content_lines(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def is_nearly_empty_page(page: fitz.Page) -> bool:
    if page.get_images():
        t = page.get_text().strip()
        if len(t) > 40:
            return False
    t = page.get_text().strip()
    if not t:
        return True
    lines = _content_lines(t)
    if len(lines) == 1 and re.fullmatch(r"\d+", lines[0]):
        return True
    if len(lines) <= 2 and len(t) < 90:
        if any(re.fullmatch(r"\d+", ln) for ln in lines):
            return True
        if re.match(r"^\d+\.\s+", lines[0]) and len(lines) == 1:
            return True
    if len(t) < 55:
        return True
    return False


def _is_junk_title_page(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    if len(t) < 240 and "Cookbook" in t and "Yasaka" in t:
        return True
    if len(t) < 80 and re.search(r"^\d+\.\s*Part\s", t):
        return True
    return False


def process(src: Path, dest: Path) -> None:
    body = fitz.open(src)
    w, h = body[0].rect.width, body[0].rect.height
    cover = build_cover(w, h)
    back = build_back_cover(w, h)

    final = fitz.open()
    final.insert_pdf(cover)
    final.insert_pdf(body)

    removed = 0
    for i in range(final.page_count - 1, 0, -1):
        page = final[i]
        text = page.get_text()
        if page.get_images():
            continue
        if _is_junk_title_page(text) or is_nearly_empty_page(page):
            final.delete_page(i)
            removed += 1

    # Back cover last
    final.insert_pdf(back)

    final.save(dest, garbage=4, deflate=True)
    final.close()
    body.close()
    cover.close()
    back.close()
    print(f"removed_empty_pages={removed}")
    print(f"fonts: title={Path(FONT_TITLE).name if FONT_TITLE else 'fallback'}")


def main() -> int:
    src = find_pdf()
    out_dir = ROOT / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "Cookbook-with-cover.pdf"
    try:
        if out.exists():
            out.unlink()
    except OSError:
        out = out_dir / "Cookbook-with-cover-new.pdf"

    print(f"cover art: {HERO} exists={HERO.exists()}")
    process(src, out)

    for dest in (
        ROOT_PDF,
        ROOT_PDF_V2,
        RELEASE_PDF,
        ROOT / "dist" / "V1-Foundation-Cookbook.pdf",
    ):
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(out, dest)
            print(f"copied {dest}")
        except OSError:
            alt = dest.with_name(dest.stem + "_new.pdf")
            shutil.copy2(out, alt)
            print(f"locked {dest.name} -> {alt.name}")

    doc = fitz.open(out)
    print(f"OK {out}")
    print(f"pages={doc.page_count} mb={out.stat().st_size/1024/1024:.2f}")
    print(f"cover images={len(doc[0].get_images())}")
    print("COVER TEXT:\n" + doc[0].get_text())
    doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
