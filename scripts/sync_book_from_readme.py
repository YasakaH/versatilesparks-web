#!/usr/bin/env python3
"""Split root README.md into a Quarto book under book/ and copy figures."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
README = ROOT / "README.md"
SRC_IMAGES = ROOT / "images"

FIGURES = {
    "how nodriver actually works": (
        "images/cookbook_architecture.png",
        "Cookbook architecture — recipes share a common layer over nodriver CDP.",
    ),
    "recipe 13:": (
        "images/selector_hierarchy.png",
        "Selector priority — prefer purpose over position.",
    ),
    "recipe 19:": (
        "images/login_verification.png",
        "Login verification — never assume authentication succeeded.",
    ),
    "recipe 24:": (
        "images/pagination_safety.png",
        "Pagination safety — three independent stop conditions.",
    ),
    "recipe 26:": (
        "images/download_lifecycle.png",
        "Download lifecycle — complete means stable size, not the click.",
    ),
    "recipe 29:": (
        "images/stop_vs_retry_flow.png",
        "Stop vs retry — temporary failures may retry; permanent ones must stop.",
    ),
}

IMAGE_FILES = [
    "hero.png",
    "cookbook_architecture.png",
    "selector_hierarchy.png",
    "login_verification.png",
    "pagination_safety.png",
    "download_lifecycle.png",
    "stop_vs_retry_flow.png",
]

# Quarto nested parts (unnumbered divider pages)
PART_GROUPS = [
    (
        "Part I — Foundations",
        [
            "chapter-1-getting-started",
            "chapter-2-browser-control",
            "chapter-3-production-foundations",
        ],
    ),
    (
        "Part II — Interaction",
        [
            "chapter-4-elements-forms",
            "chapter-5-authentication-sessions",
        ],
    ),
    (
        "Part III — Extraction & Downloads",
        ["chapter-6-data-collection"],
    ),
    (
        "Part IV — Production",
        [
            "chapter-7-reliable-automation",
            "chapter-8-starter-kit",
        ],
    ),
]


def slug(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60]


def split_outside_fences(md: str) -> list[str]:
    lines = md.splitlines(keepends=True)
    sections: list[list[str]] = []
    current: list[str] = []
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            current.append(line)
            continue
        if not in_fence and re.match(r"^# [^#]", stripped):
            if current and any(s.strip() for s in current):
                sections.append(current)
            current = [line]
            continue
        current.append(line)
    if current and any(s.strip() for s in current):
        sections.append(current)
    return ["".join(s).strip() for s in sections]


def inject_figures(body: str) -> str:
    lines = body.splitlines(keepends=True)
    out: list[str] = []
    used: set[str] = set()
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append(line)
        if in_fence:
            continue
        m = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if not m:
            continue
        heading = m.group(2).strip().lower()
        for needle, (path, cap) in FIGURES.items():
            if needle in heading and path not in used:
                out.append("\n")
                out.append(
                    f'![{cap}]({path}){{fig-align="center" width="100%"}}\n\n'
                )
                used.add(path)
    return "".join(out)


def strip_chapter_h1(body: str) -> str:
    lines = body.splitlines(keepends=True)
    if lines and re.match(r"^# [^#]", lines[0].strip()):
        lines = lines[1:]
        while lines and lines[0].strip() in ("", "---"):
            lines = lines[1:]
    return "".join(lines)


def tex_escape(s: str) -> str:
    return (
        s.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("—", "---")
        .replace("\n", " ")
    )


def write_part_page(fname: str, part_title: str, blurb: str) -> None:
    """Unnumbered mid-page divider — no chapter index on the page."""
    if "—" in part_title:
        label, name = [x.strip() for x in part_title.split("—", 1)]
    else:
        label, name = part_title, ""

    label_t, name_t, blurb_t = tex_escape(label), tex_escape(name), tex_escape(blurb)
    # title kept for TOC; body is pure LaTeX mid-page divider (no chapter number)
    qmd = f"""---
title: "{part_title}"
number: false
---

```{{=latex}}
\\clearpage
\\thispagestyle{{empty}}
\\addcontentsline{{toc}}{{chapter}}{{{label_t} --- {name_t}}}
\\vspace*{{\\fill}}
\\begin{{center}}
{{\\LARGE\\sffamily {label_t}}}\\\\[1.0em]
{{\\Huge\\bfseries {name_t}}}\\\\[1.6em]
\\begin{{minipage}}{{0.72\\textwidth}}
\\centering\\large\\itshape
{blurb_t}
\\end{{minipage}}
\\end{{center}}
\\vspace*{{\\fill}}
\\clearpage
```
"""
    (BOOK / fname).write_text(qmd, encoding="utf-8")


def main() -> None:
    if not README.exists():
        raise SystemExit(f"Missing {README}")

    BOOK.mkdir(exist_ok=True)
    img_dir = BOOK / "images"
    img_dir.mkdir(exist_ok=True)
    for name in IMAGE_FILES:
        src = SRC_IMAGES / name
        if src.exists():
            shutil.copy2(src, img_dir / name)
            print(f"image  {name}")

    md = README.read_text(encoding="utf-8").replace("Sandeep Vara", "Yasaka Hanini")
    parts = split_outside_fences(md)
    chapters: dict[str, tuple[str, str]] = {}  # slug -> (title, body)

    for p in parts:
        if not p:
            continue
        first = p.splitlines()[0]
        m = re.match(r"^# (.+)$", first.strip())
        if not m:
            continue
        title = m.group(1).strip()
        low = title.lower()
        if low.startswith("python browser automation"):
            continue
        if low in {"or", "and", "else", "endif"} or len(p) < 80:
            print(f"skip   {title!r} ({len(p)} chars)")
            continue
        body = strip_chapter_h1(inject_figures(p))
        s = slug(title)
        chapters[s] = (title, body)

    # Index / welcome — foundation framing, not "free edition"
    (BOOK / "index.qmd").write_text(
        """---
title: "Welcome"
number: false
---

```{=latex}
\\vspace*{1.5em}
{\\Huge\\bfseries Welcome\\\\[0.6em]}
```

This is the **Foundation** volume of *Python Browser Automation Cookbook* — **30 production-ready recipes** using **nodriver**.

Build browser automation that works the same on day 30 as it did on day 1.

**Yasaka Hanini** · 2026

> When you outgrow these thirty recipes, see the final chapter — *What Comes Next*.
""",
        encoding="utf-8",
    )

    # Write non-part chapters
    part_slugs = {
        "part-i-foundations",
        "part-ii-interaction",
        "part-iii-extraction-downloads",
        "part-iv-production",
    }
    for s, (title, body) in chapters.items():
        if s in part_slugs:
            # Part blurb only — rendered as centered divider page
            blurb = re.sub(r"\s+", " ", body.strip())[:400]
            # strip leftover markdown headings from blurb
            blurb = re.sub(r"^#+\s*", "", blurb)
            blurb = re.sub(r"[*_`]", "", blurb)
            write_part_page(f"{s}.qmd", title, blurb)
            print(f"part   {s}.qmd")
            continue
        safe = title.replace('"', "'")
        qmd = f'---\ntitle: "{safe}"\n---\n\n{body.strip()}\n'
        (BOOK / f"{s}.qmd").write_text(qmd, encoding="utf-8")
        print(f"wrote  {s}.qmd")

    # Linear chapter list: part divider qmd (unnumbered, centered) then chapters
    order = [
        "index.qmd",
        "preface.qmd",
        "the-production-mindset.qmd",
        "how-this-book-works.qmd",
        "how-nodriver-actually-works.qmd",
        "chapter-0-before-you-begin.qmd",
        "part-i-foundations.qmd",
        "chapter-1-getting-started.qmd",
        "chapter-2-browser-control.qmd",
        "chapter-3-production-foundations.qmd",
        "part-ii-interaction.qmd",
        "chapter-4-elements-forms.qmd",
        "chapter-5-authentication-sessions.qmd",
        "part-iii-extraction-downloads.qmd",
        "chapter-6-data-collection.qmd",
        "part-iv-production.qmd",
        "chapter-7-reliable-automation.qmd",
        "chapter-8-starter-kit.qmd",
        "appendix-common-patterns-reference.qmd",
        "professional-edition.qmd",
    ]
    yaml_lines = [f"  - {f}" for f in order if (BOOK / f).exists() or f == "index.qmd"]

    yml = f"""project:
  type: book
  output-dir: ../dist

book:
  title: "Python Browser Automation Cookbook"
  subtitle: "30 Production-Ready Recipes Using nodriver"
  author: "Yasaka Hanini"
  date: "2026"
  chapters:
{chr(10).join(yaml_lines)}

format:
  pdf:
    documentclass: scrbook
    classoption:
      - oneside
      - openany
    fontsize: 11pt
    geometry:
      - margin=1in
      - heightrounded
    # TeX Gyre faces ship with TinyTeX — guaranteed visible font change
    mainfont: "TeX Gyre Pagella"
    monofont: "TeX Gyre Cursor"
    monofontoptions:
      - Scale=0.88
    sansfont: "TeX Gyre Heros"
    colorlinks: true
    linkcolor: NavyBlue
    urlcolor: NavyBlue
    toc: true
    toc-depth: 2
    number-sections: true
    number-depth: 3
    fig-pos: "H"
    keep-tex: false
    linestretch: 1.15
    code-block-bg: "#f1f5f9"
    code-block-border-left: "#0b1630"
    include-in-header:
      - preamble.tex
  html:
    theme: cosmo
    toc: true
    number-sections: true

execute:
  echo: true
  eval: false
"""
    (BOOK / "_quarto.yml").write_text(yml, encoding="utf-8")
    print(f"\nBook ready: {BOOK}")
    print(f"Chapters:   {len(chapters)}")


if __name__ == "__main__":
    main()
