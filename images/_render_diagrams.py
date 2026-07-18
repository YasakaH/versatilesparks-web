"""
HD conceptual explainer diagrams for Python Browser Automation Cookbook (PDF).
2048x1152 PNG. Concept labels only — no code snippets, no HTML screenshots.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 2048, 1152

BG = (5, 11, 26)
SURFACE = (11, 22, 48)
CYAN = (34, 211, 238)
AMBER = (251, 191, 36)
AMBER_DIM = (217, 119, 6)
GREEN = (52, 211, 153)
RED = (239, 68, 68)
SLATE = (148, 163, 184)
WHITE = (226, 232, 240)
MUTED = (100, 116, 139)

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_MONO = r"C:\Windows\Fonts\CascadiaCode.ttf"
if not Path(FONT_MONO).exists():
    FONT_MONO = r"C:\Windows\Fonts\consola.ttf"


def fnt(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REG)
    return ImageFont.truetype(path, size)


def new_canvas() -> Image.Image:
    img = Image.new("RGBA", (W, H), (*BG, 255))
    draw = ImageDraw.Draw(img)
    step = 64
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=(15, 28, 55, 70), width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=(15, 28, 55, 70), width=1)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W // 2 - 700, -420, W // 2 + 700, 480], fill=(34, 211, 238, 16))
    glow = glow.filter(ImageFilter.GaussianBlur(36))
    return Image.alpha_composite(img, glow)


def measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def text_center(draw, xy, text, font, fill):
    tw, th = measure(draw, text, font)
    draw.text((xy[0] - tw / 2, xy[1] - th / 2), text, font=font, fill=fill)


def text_left(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill)


def rrect(draw, box, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def soft_glow(img: Image.Image, cx: int, cy: int, rx: int, ry: int, color, alpha=36) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(30))
    return Image.alpha_composite(img, layer)


def title_block(draw, title: str, subtitle: str):
    text_left(draw, (88, 52), title, fnt(44, bold=True), WHITE)
    text_left(draw, (88, 112), subtitle, fnt(24), SLATE)


def arrow(draw, x1, y1, x2, y2, color, label=None, width=4):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for da in (0.4, -0.4):
        ax = x2 - 18 * math.cos(ang + da)
        ay = y2 - 18 * math.sin(ang + da)
        draw.line([(x2, y2), (ax, ay)], fill=color, width=width)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        tw, th = measure(draw, label, fnt(18, bold=True))
        rrect(
            draw,
            [mx - tw / 2 - 12, my - th / 2 - 8, mx + tw / 2 + 12, my + th / 2 + 8],
            8,
            fill=(*BG, 240),
            outline=color,
            width=1,
        )
        text_center(draw, (mx, my), label, fnt(18, bold=True), color)


# ── SELECTOR HIERARCHY ──────────────────────────────────────────────────────
def render_selector_hierarchy() -> Image.Image:
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    title_block(
        draw,
        "Selector Priority",
        "Prefer purpose over position — what survives when the page changes",
    )

    rows = [
        ("data-testid", "Built as an automation contract", "Most stable", CYAN, 5),
        ("id", "Unique and intentional", "High", (45, 190, 175), 4),
        ("name", "Forms and input fields", "Medium", (40, 170, 155), 3),
        ("semantic class", "Meaning, not layout chrome", "Medium", AMBER, 2),
        ("CSS hierarchy", "Depends on structure", "Low", (230, 145, 80), 1),
        ("XPath position", "Breaks on any DOM shift", "Avoid", RED, 0),
    ]

    top, row_h = 190, 132
    max_w, min_w, left = 1580, 980, 140

    for i, (label, meaning, stability, color, stars) in enumerate(rows):
        t = i / (len(rows) - 1)
        width = int(max_w - t * (max_w - min_w))
        x0 = left + (max_w - width) // 2
        y0 = top + i * row_h
        y1 = y0 + 104
        cx = x0 + width // 2
        cy = (y0 + y1) // 2

        img = soft_glow(img, cx, cy, width // 2 - 20, 48, color, 32)
        draw = ImageDraw.Draw(img)

        rrect(draw, [x0, y0, x0 + width, y1], 18, fill=(*color, 32), outline=color, width=2)
        draw.rounded_rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], radius=4, fill=color)

        text_left(draw, (x0 + 42, y0 + 18), label, fnt(30, bold=True, mono=True), WHITE)
        text_left(draw, (x0 + 42, y0 + 58), meaning, fnt(22), SLATE)

        if stars:
            dots = "●" * stars + "○" * (5 - stars)
            lw, _ = measure(draw, label, fnt(30, bold=True, mono=True))
            text_left(draw, (x0 + 42 + lw + 20, y0 + 24), dots, fnt(16), color)

        bw, bh = measure(draw, stability, fnt(20, bold=True))
        bx = x0 + width - bw - 56
        by = y0 + 36
        rrect(draw, [bx - 14, by - 8, bx + bw + 14, by + bh + 8], 10, fill=(*color, 40), outline=color, width=1)
        text_left(draw, (bx, by), stability, fnt(20, bold=True), color)

    draw = ImageDraw.Draw(img)
    text_left(
        draw,
        (140, H - 64),
        "Production rule: describe purpose, not position.",
        fnt(22, bold=True),
        MUTED,
    )
    return img


# ── STOP vs RETRY ───────────────────────────────────────────────────────────
def render_stop_vs_retry() -> Image.Image:
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    title_block(
        draw,
        "Stop vs Retry",
        "Only temporary failures earn another attempt — permanent ones must stop",
    )

    def box_node(cx, cy, w, h, title, sub, color, shape="round"):
        nonlocal img, draw
        img = soft_glow(img, cx, cy, w // 2 + 30, h // 2 + 24, color, 34)
        draw = ImageDraw.Draw(img)
        x0, y0 = cx - w // 2, cy - h // 2
        if shape == "diamond":
            pts = [(cx, y0), (x0 + w, cy), (cx, y0 + h), (x0, cy)]
            draw.polygon(pts, fill=(*color, 36), outline=color)
            draw.line(pts + [pts[0]], fill=color, width=3)
        elif shape == "circle":
            draw.ellipse([x0, y0, x0 + w, y0 + h], fill=(*color, 36), outline=color, width=3)
        else:
            rrect(draw, [x0, y0, x0 + w, y0 + h], 18, fill=(*color, 36), outline=color, width=3)
        text_center(draw, (cx, cy - (14 if sub else 0)), title, fnt(26, bold=True), WHITE)
        if sub:
            text_center(draw, (cx, cy + 22), sub, fnt(18), SLATE)

    # Nodes
    box_node(1024, 230, 340, 96, "Operation fails", "step did not succeed", CYAN)
    box_node(1024, 430, 380, 150, "Temporary failure?", "will it fix itself?", AMBER, "diamond")

    box_node(380, 640, 320, 110, "Budget left?", "retries remaining", GREEN, "diamond")
    box_node(380, 900, 280, 96, "Retry", "run the step again", GREEN)

    box_node(1668, 640, 300, 110, "Permanent", "won't self-heal", RED)
    box_node(1668, 900, 280, 96, "STOP", "log and exit cleanly", RED)

    box_node(1024, 900, 260, 96, "Continue", "resume the flow", CYAN, "circle")

    # Arrows
    arrow(draw, 1024, 278, 1024, 355, CYAN)
    arrow(draw, 900, 500, 500, 585, GREEN, "Yes")
    arrow(draw, 1148, 500, 1548, 585, RED, "No")
    arrow(draw, 380, 695, 380, 852, GREEN)
    arrow(draw, 1668, 695, 1668, 852, RED)
    arrow(draw, 520, 900, 890, 900, CYAN, "ok")

    # Budget exhausted → STOP
    arrow(draw, 540, 640, 1518, 640, RED, "no budget")

    # Retry loop arc back to decision
    draw.arc([160, 430, 600, 920], start=100, end=260, fill=GREEN, width=4)
    draw.line([(180, 500), (840, 430)], fill=GREEN, width=3)
    text_left(draw, (200, 470), "while budget allows", fnt(18, bold=True), GREEN)

    # Two concept columns (not code)
    rrect(draw, [88, 1020, 980, 1115], 14, fill=(*SURFACE, 220), outline=GREEN, width=2)
    text_left(draw, (112, 1035), "Worth retrying", fnt(20, bold=True), GREEN)
    text_left(draw, (112, 1070), "timeouts  ·  connection blips  ·  temporary server errors", fnt(20), SLATE)

    rrect(draw, [1068, 1020, 1960, 1115], 14, fill=(*SURFACE, 220), outline=RED, width=2)
    text_left(draw, (1092, 1035), "Must stop", fnt(20, bold=True), RED)
    text_left(draw, (1092, 1070), "bad selector  ·  wrong credentials  ·  CAPTCHA  ·  page changed", fnt(20), SLATE)

    return img


# ── PAGINATION SAFETY ───────────────────────────────────────────────────────
def render_pagination_safety() -> Image.Image:
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    title_block(
        draw,
        "Pagination Safety",
        "Three independent stop conditions — any one ends the loop",
    )

    conditions = [
        ("C1", "No Next control", "The page offers no way\nto go forward", CYAN, "missing"),
        ("C2", "Next is disabled", "Control is present but\ncannot advance", AMBER, "blocked"),
        ("C3", "Max pages hit", "Hard ceiling (e.g. 100)\nprotects the run", RED, "max"),
    ]

    card_w, card_h = 440, 400
    gap = 56
    total = 3 * card_w + 2 * gap
    start_x = (W - total) // 2
    y = 240

    mids = []
    for i, (cid, title, desc, color, kind) in enumerate(conditions):
        x = start_x + i * (card_w + gap)
        cx = x + card_w // 2
        mids.append((cx, color))
        img = soft_glow(img, cx, y + card_h // 2, 180, 160, color, 28)
        draw = ImageDraw.Draw(img)

        rrect(draw, [x, y, x + card_w, y + card_h], 24, fill=(*SURFACE, 235), outline=color, width=3)
        rrect(draw, [x + 28, y + 28, x + 118, y + 82], 12, fill=(*color, 45), outline=color, width=2)
        text_center(draw, (x + 73, y + 55), cid, fnt(28, bold=True), color)

        text_left(draw, (x + 28, y + 110), title, fnt(30, bold=True), WHITE)
        for li, line in enumerate(desc.split("\n")):
            text_left(draw, (x + 28, y + 170 + li * 36), line, fnt(22), SLATE)

        # concept icon
        icx, icy = cx, y + 320
        if kind == "missing":
            rrect(draw, [icx - 48, icy - 30, icx + 48, icy + 30], 10, fill=None, outline=color, width=3)
            draw.line([(icx - 26, icy - 16), (icx + 26, icy + 16)], fill=color, width=4)
            draw.line([(icx + 26, icy - 16), (icx - 26, icy + 16)], fill=color, width=4)
        elif kind == "blocked":
            rrect(draw, [icx - 48, icy - 30, icx + 48, icy + 30], 10, fill=(*color, 28), outline=color, width=3)
            # lock body
            draw.rounded_rectangle([icx - 16, icy - 2, icx + 16, icy + 18], 4, outline=color, width=3)
            draw.arc([icx - 14, icy - 22, icx + 14, icy + 2], 0, 180, fill=color, width=3)
        else:
            draw.arc([icx - 40, icy - 28, icx + 40, icy + 36], 200, 340, fill=color, width=6)
            text_center(draw, (icx, icy + 8), "MAX", fnt(20, bold=True), color)

        draw.line([(cx, y + card_h), (cx, y + card_h + 36)], fill=color, width=3)

    stop_y = y + card_h + 70
    stop_cx = W // 2
    for cx, color in mids:
        draw.line([(cx, stop_y - 34), (stop_cx, stop_y + 8)], fill=color, width=3)

    img = soft_glow(img, stop_cx, stop_y + 55, 240, 50, RED, 48)
    draw = ImageDraw.Draw(img)
    rrect(draw, [stop_cx - 220, stop_y + 16, stop_cx + 220, stop_y + 100], 18, fill=(*RED, 50), outline=RED, width=3)
    text_center(draw, (stop_cx, stop_y + 58), "STOP the loop", fnt(32, bold=True), WHITE)

    text_left(
        draw,
        (120, H - 56),
        "Production rule: never paginate on hope — define every exit before you start.",
        fnt(22, bold=True),
        MUTED,
    )
    return img


# ── DOWNLOAD LIFECYCLE ──────────────────────────────────────────────────────
def render_download_lifecycle() -> Image.Image:
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    title_block(
        draw,
        "Download Lifecycle",
        "A file is not ready when the click finishes — wait for a stable finished state",
    )

    stages = [
        ("1", "Trigger", "Automation or user\nstarts the download", CYAN, "click"),
        ("2", "Temp file", "Browser creates a\npartial download", AMBER, "temp"),
        ("3", "Growing", "Bytes still arriving;\nsize keeps changing", AMBER_DIM, "grow"),
        ("4", "Finalize", "Renamed to final\nname and type", GREEN, "rename"),
        ("5", "Stable", "Size unchanged for\na short quiet window", GREEN, "done"),
    ]

    n = len(stages)
    box_w, box_h = 290, 340
    gap = 36
    total = n * box_w + (n - 1) * gap
    x0 = (W - total) // 2
    y = 260
    centers = []

    for i, (num, title, desc, color, kind) in enumerate(stages):
        x = x0 + i * (box_w + gap)
        cx = x + box_w // 2
        centers.append((cx, color))
        img = soft_glow(img, cx, y + 90, 100, 80, color, 36)
        draw = ImageDraw.Draw(img)

        rrect(draw, [x, y, x + box_w, y + box_h], 22, fill=(*SURFACE, 235), outline=color, width=3)
        draw.ellipse([cx - 38, y + 28, cx + 38, y + 104], fill=(*color, 45), outline=color, width=3)
        text_center(draw, (cx, y + 66), num, fnt(32, bold=True), color)
        text_center(draw, (cx, y + 140), title, fnt(28, bold=True), WHITE)
        for li, line in enumerate(desc.split("\n")):
            text_center(draw, (cx, y + 190 + li * 32), line, fnt(20), SLATE)

        my = y + 290
        if kind == "click":
            draw.ellipse([cx - 20, my - 20, cx + 20, my + 20], outline=color, width=3)
            draw.ellipse([cx - 6, my - 6, cx + 6, my + 6], fill=color)
        elif kind == "temp":
            rrect(draw, [cx - 30, my - 22, cx + 30, my + 22], 6, fill=None, outline=color, width=3)
            draw.line([(cx - 16, my - 6), (cx + 16, my - 6)], fill=color, width=2)
            draw.line([(cx - 16, my + 6), (cx + 4, my + 6)], fill=MUTED, width=2)
        elif kind == "grow":
            for j, hgt in enumerate([12, 20, 30]):
                draw.rectangle([cx - 32 + j * 24, my + 14 - hgt, cx - 14 + j * 24, my + 14], fill=color)
        elif kind == "rename":
            rrect(draw, [cx - 32, my - 16, cx + 8, my + 18], 4, fill=None, outline=MUTED, width=2)
            rrect(draw, [cx - 8, my - 22, cx + 32, my + 12], 4, fill=None, outline=color, width=3)
        else:
            draw.ellipse([cx - 22, my - 22, cx + 22, my + 22], outline=color, width=3)
            draw.line([(cx - 10, my), (cx - 2, my + 10), (cx + 14, my - 10)], fill=color, width=4)

    # forward arrows
    for i in range(n - 1):
        x1 = centers[i][0] + box_w // 2 - 8
        x2 = centers[i + 1][0] - box_w // 2 + 8
        mid_y = y + 66
        c = centers[i + 1][1]
        draw.line([(x1, mid_y), (x2, mid_y)], fill=c, width=4)
        draw.polygon([(x2, mid_y), (x2 - 14, mid_y - 8), (x2 - 14, mid_y + 8)], fill=c)

    # feedback: not stable → keep watching (stage 5 → stage 3)
    loop_y = y + box_h + 64
    c5, c3 = centers[4][0], centers[2][0]
    draw.line([(c5, y + box_h), (c5, loop_y)], fill=AMBER, width=3)
    draw.line([(c5, loop_y), (c3, loop_y)], fill=AMBER, width=3)
    draw.line([(c3, loop_y), (c3, y + box_h)], fill=AMBER, width=3)
    draw.polygon([(c3, y + box_h), (c3 - 8, y + box_h + 14), (c3 + 8, y + box_h + 14)], fill=AMBER)
    text_center(draw, ((c3 + c5) // 2, loop_y - 26), "size still changing → keep watching", fnt(20, bold=True), AMBER)

    text_left(
        draw,
        (120, H - 56),
        "Production rule: complete means stable size — not the click, not the temp name.",
        fnt(22, bold=True),
        MUTED,
    )
    return img


def main():
    jobs = [
        ("selector_hierarchy.png", render_selector_hierarchy),
        ("stop_vs_retry_flow.png", render_stop_vs_retry),
        ("pagination_safety.png", render_pagination_safety),
        ("download_lifecycle.png", render_download_lifecycle),
    ]
    for name, fn in jobs:
        img = fn().convert("RGB")
        path = OUT / name
        img.save(path, "PNG", optimize=True)
        print(f"wrote {path.name}  {img.size}  {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
