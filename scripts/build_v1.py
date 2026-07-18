#!/usr/bin/env python3
"""
Build V1 Foundation PDF (30 recipes, Ch 0–8).

All refinements:
  - Typeset cover over text-free hero_art (no double text)
  - TeX Gyre Pagella body font
  - Numbering 2.3 + a) b) c) (no deep dots)
  - Centered unnumbered Part pages
  - "Foundation" framing (not free edition)
  - Code line-wrap inside grey boxes
  - Strip near-empty pages
  - Upsell for Professional / V2 at end
  - Output to dist/ and releases/ — never book/_build

Usage:
  python scripts/build_v1.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
CHAPTERS = BOOK / "v1"  # V1 manuscript only (Ch 0–8)
IMAGES = BOOK / "images"
STAGING = ROOT / "dist" / "v1-staging"
DIST = ROOT / "dist"
RELEASES = ROOT / "releases"


def _fresh_staging() -> Path:
    """Create a writable staging dir (avoid locked .quarto caches)."""
    base = ROOT / "dist"
    base.mkdir(parents=True, exist_ok=True)
    for name in ("v1-staging", "v1-staging-b", "v1-staging-c"):
        path = base / name
        if path.exists():
            try:
                shutil.rmtree(path)
                return path
            except OSError:
                continue
        return path
    # last resort unique
    import time

    path = base / f"v1-staging-{int(time.time())}"
    path.mkdir(parents=True, exist_ok=True)
    return path

QUARTO = Path(r"C:\Users\varas\AppData\Local\Programs\Quarto\bin\quarto.exe")

# V1 figure insertions (match heading text, case-insensitive)
FIGURES = {
    "getting started": (
        "images/cookbook_architecture.png",
        "Cookbook architecture — recipes share a common layer over nodriver CDP.",
    ),
    "recipe 13": (
        "images/selector_hierarchy.png",
        "Selector priority — prefer purpose over position.",
    ),
    "find elements": (
        "images/selector_hierarchy.png",
        "Selector priority — prefer purpose over position.",
    ),
    "recipe 19": (
        "images/login_verification.png",
        "Login verification — never assume authentication succeeded.",
    ),
    "log in": (
        "images/login_verification.png",
        "Login verification — never assume authentication succeeded.",
    ),
    "recipe 24": (
        "images/pagination_safety.png",
        "Pagination safety — three independent stop conditions.",
    ),
    "pagination": (
        "images/pagination_safety.png",
        "Pagination safety — three independent stop conditions.",
    ),
    "recipe 26": (
        "images/download_lifecycle.png",
        "Download lifecycle — complete means stable size, not the click.",
    ),
    "download files": (
        "images/download_lifecycle.png",
        "Download lifecycle — complete means stable size, not the click.",
    ),
    "recipe 29": (
        "images/stop_vs_retry_flow.png",
        "Stop vs retry — temporary failures may retry; permanent ones must stop.",
    ),
    "resilient": (
        "images/stop_vs_retry_flow.png",
        "Stop vs retry — temporary failures may retry; permanent ones must stop.",
    ),
}

# Architecture also early in book
ARCH_HEADINGS = ("how nodriver", "before you begin", "getting started")


def tex_escape(s: str) -> str:
    return (
        s.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("—", "---")
        .replace("–", "--")
        .replace("\n", " ")
    )


def clean_text(s: str) -> str:
    """Normalize encoding glitches from restructure."""
    s = s.replace("\ufeff", "")
    s = s.replace("\u2014", "—").replace("\u2013", "–")
    # common mojibake for em dash
    s = s.replace("â€”", "—").replace("â€™", "'").replace("â€œ", '"').replace("â€", '"')
    s = s.replace("�?", "—").replace("�", "")
    return s


def strip_leading_h1(body: str) -> str:
    lines = body.splitlines(keepends=True)
    if lines and re.match(r"^# [^#]", lines[0].strip()):
        lines = lines[1:]
        while lines and lines[0].strip() in ("", "---"):
            lines = lines[1:]
    return "".join(lines)


def strip_image_mentions(body: str) -> str:
    """Remove **Images:** / mermaid file references — figures stand alone if present."""
    body = re.sub(r"^\*\*Images:\*\*.*$", "", body, flags=re.M)
    body = re.sub(
        r"^Images:\s*`[^`]+`.*$",
        "",
        body,
        flags=re.M | re.I,
    )
    body = re.sub(
        r"(?i)^.*images? in this chapter.*$",
        "",
        body,
        flags=re.M,
    )
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


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
                break
    return "".join(out)


def title_from_md(path: Path) -> str:
    text = clean_text(path.read_text(encoding="utf-8", errors="replace"))
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def write_chapter_qmd(src: Path, dest: Path) -> None:
    raw = clean_text(src.read_text(encoding="utf-8", errors="replace"))
    title = title_from_md(src)
    body = inject_figures(strip_image_mentions(strip_leading_h1(raw)))
    dest.write_text(
        f'---\ntitle: "{title.replace(chr(34), chr(39))}"\n---\n\n{body.strip()}\n',
        encoding="utf-8",
    )


def write_part_qmd(src: Path, dest: Path) -> None:
    raw = clean_text(src.read_text(encoding="utf-8", errors="replace"))
    title = title_from_md(src)
    body = strip_leading_h1(raw).strip()
    body = re.sub(r"^#+\s*", "", body)
    body = re.sub(r"[*_`]", "", body)
    body = re.sub(r"\s+", " ", body).strip(" -—")
    if "—" in title:
        label, name = [x.strip() for x in title.split("—", 1)]
    elif " - " in title:
        label, name = [x.strip() for x in title.split(" - ", 1)]
    else:
        parts = title.split(None, 2)
        label = " ".join(parts[:2]) if len(parts) >= 2 else title
        name = parts[2] if len(parts) > 2 else ""
    label_t, name_t, blurb_t = tex_escape(label), tex_escape(name), tex_escape(body)
    dest.write_text(
        f"""---
title: "{title.replace(chr(34), chr(39))}"
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
""",
        encoding="utf-8",
    )


PREAMBLE = r"""
\setcounter{secnumdepth}{3}
\renewcommand{\thesection}{\arabic{chapter}.\arabic{section}}
\renewcommand{\thesubsection}{\alph{subsection})}
\renewcommand{\thesubsubsection}{}
\renewcommand{\theparagraph}{}

\makeatletter
\renewcommand{\@makeschapterhead}[1]{}
\renewcommand{\@schapter}[1]{%
  \if@twocolumn \@topnewpage[\vspace*{0pt}] \else \vspace*{0pt} \fi
}
\makeatother

\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\brokenpenalty=10000
\raggedbottom
\emergencystretch=3em

\setlength{\parskip}{0.35em plus 0.12em minus 0.08em}
\setlength{\parindent}{0pt}

\usepackage{float}
\floatplacement{figure}{H}
\setkeys{Gin}{width=\linewidth,height=0.38\textheight,keepaspectratio}

\usepackage{xcolor}
\usepackage{fvextra}
\definecolor{shadecolor}{RGB}{241,245,249}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{%
  breaklines=true,
  breakanywhere=true,
  breaksymbolleft={},
  breaksymbolright={},
  fontsize=\footnotesize,
  commandchars=\\\{\}
}
\fvset{breaklines=true,breakanywhere=true,fontsize=\footnotesize}
"""


def assemble_staging() -> list[str]:
    global STAGING
    STAGING = _fresh_staging()
    STAGING.mkdir(parents=True, exist_ok=True)
    (STAGING / "images").mkdir(exist_ok=True)

    # copy figures
    for img in IMAGES.glob("*.png"):
        shutil.copy2(img, STAGING / "images" / img.name)

    chapter_files: list[str] = []

    # Welcome
    (STAGING / "index.qmd").write_text(
        """---
title: "Welcome"
number: false
---

```{=latex}
\\vspace*{1.2em}
{\\Huge\\bfseries Welcome\\\\[0.5em]}
```

This is the **Foundation** volume of *Python Browser Automation Cookbook* — **30 production-ready recipes** using **nodriver**.

Build browser automation that works the same on day 30 as it did on day 1.

**Yasaka Hanini** · 2026

> When you outgrow these thirty recipes, see the final chapter — *What Comes Next*.
""",
        encoding="utf-8",
    )
    chapter_files.append("index.qmd")

    # V1 spine
    spine = [
        ("chapter-00.md", "chapter"),
        ("part-i.md", "part"),
        ("chapter-01.md", "chapter"),
        ("chapter-02.md", "chapter"),
        ("chapter-03.md", "chapter"),
        ("part-ii.md", "part"),
        ("chapter-04.md", "chapter"),
        ("chapter-05.md", "chapter"),
        ("part-iii.md", "part"),
        ("chapter-06.md", "chapter"),
        ("part-iv.md", "part"),
        ("chapter-07.md", "chapter"),
        ("chapter-08.md", "chapter"),
    ]

    for name, kind in spine:
        src = CHAPTERS / name
        if not src.exists():
            print(f"WARNING: missing {src}")
            continue
        dest_name = name.replace(".md", ".qmd")
        dest = STAGING / dest_name
        if kind == "part":
            write_part_qmd(src, dest)
        else:
            write_chapter_qmd(src, dest)
        chapter_files.append(dest_name)
        print(f"  {kind:7} {dest_name}")

    # Upsell → V2 / Professional
    (STAGING / "what-comes-next.qmd").write_text(
        """---
title: "What Comes Next"
---

You finished the **Foundation** volume. That is real progress — thirty production recipes, a reusable common layer, and judgment about when to stop instead of when to retry forever.

This book is the foundation. The **Professional Edition** (V2) is the full workshop.

## The Professional Edition

A deeper kit for people who ship automation for work — not just demos.

### Foundation vs Professional

| Foundation (this book) | Professional Edition |
|------------------------|----------------------|
| 30 core recipes | **60+** recipes and full project kits |
| Chapters 0–8 | Six advanced chapters (below) plus ops playbooks |
| Single-machine focus | Multi-account, queues, and scheduled fleets |
| Starter scaffold | Production templates + checklists |

### What you unlock

- **Advanced Browser Control** — network interception, mobile emulation, WebSocket, performance metrics  
- **Anti-Detection & Evasion** — fingerprint spoofing, proxy rotation, session diversity  
- **Advanced Interaction** — drag/drop, iframes, shadow DOM, clipboard  
- **Production Systems** — Docker, Kubernetes, database, alerting, webhooks  
- **Data Processing** — cleaning, export, incremental scraping, visual diffing  
- **Case Studies** — four full walkthroughs: price monitor, SaaS dashboard, social media scheduler, internal tool  

### Who it is for

Engineers and freelancers who already know Python, already automated *something*, and need the next tier: work that still runs on Monday morning without a panic fix.

### How to get it

Search for **Python Browser Automation Cookbook — Professional Edition** by **Yasaka Hanini**, or use the purchase link from the same place you found this volume.

Keep this Foundation book. Use it. Break it. Then when the work gets harder than thirty recipes can cover — **upgrade once**, not every time a selector fails.

::: {.callout-tip}
## Build once. Run unattended.

The professional kit is not more theory. It is more *finished* recipes — so you spend less time reinventing the same five production problems.
:::
""",
        encoding="utf-8",
    )
    chapter_files.append("what-comes-next.qmd")

    (STAGING / "preamble.tex").write_text(PREAMBLE, encoding="utf-8")

    yml_chapters = "\n".join(f"  - {c}" for c in chapter_files)
    yml = f"""project:
  type: book
  output-dir: ..

book:
  title: "Python Browser Automation Cookbook"
  subtitle: "Foundation — 30 Production-Ready Recipes Using nodriver"
  author: "Yasaka Hanini"
  date: "2026"
  chapters:
{yml_chapters}

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

execute:
  echo: true
  eval: false
"""
    (STAGING / "_quarto.yml").write_text(yml, encoding="utf-8")
    return chapter_files


def run_quarto() -> Path:
    if not QUARTO.exists():
        raise SystemExit(f"Quarto not found at {QUARTO}")
    # clean previous raw pdf in dist
    for p in DIST.glob("Python-Browser-Automation-Cookbook*.pdf"):
        try:
            p.unlink()
        except OSError:
            pass
    cmd = [str(QUARTO), "render", "--to", "pdf"]
    print("Running:", " ".join(cmd), "in", STAGING)
    r = subprocess.run(cmd, cwd=STAGING)
    if r.returncode != 0:
        raise SystemExit(f"quarto render failed: {r.returncode}")
    pdf = DIST / "Python-Browser-Automation-Cookbook.pdf"
    if not pdf.exists():
        # sometimes named with spaces differently
        found = list(DIST.glob("*.pdf"))
        found = [p for p in found if "Cookbook" in p.name and "cover" not in p.name.lower()]
        if not found:
            raise SystemExit(f"No PDF produced in {DIST}")
        pdf = max(found, key=lambda p: p.stat().st_mtime)
    return pdf


def main() -> int:
    print("=== V1 Foundation PDF build ===")
    print("Staging under dist/v1-staging (not book/)")
    DIST.mkdir(exist_ok=True)
    RELEASES.mkdir(exist_ok=True)

    # ensure no book/_build
    bb = BOOK / "_build"
    if bb.exists():
        shutil.rmtree(bb, ignore_errors=True)
        print("removed book/_build")

    assemble_staging()
    raw_pdf = run_quarto()
    print(f"Raw PDF: {raw_pdf}")

    # finalize cover + empty-page cleanup
    sys.path.insert(0, str(ROOT / "scripts"))
    # force find path
    import finalize_pdf as fin

    # monkey-patch find to use our raw pdf
    fin.find_pdf = lambda: raw_pdf  # type: ignore
    fin.main()

    # copy final named artifacts
    final_candidates = [
        DIST / "Cookbook-with-cover.pdf",
        DIST / "Cookbook-with-cover-new.pdf",
    ]
    final = next((p for p in final_candidates if p.exists()), None)
    if not final:
        # finalize may have written only to root
        final = ROOT / "Python_Browser_Automation_Cookbook.pdf"
    if final.exists():
        targets = [
            DIST / "V1-Foundation-Cookbook.pdf",
            RELEASES / "V1-Foundation-Cookbook.pdf",
            ROOT / "Python_Browser_Automation_Cookbook.pdf",
        ]
        for t in targets:
            try:
                shutil.copy2(final, t)
                print(f"FINAL -> {t}")
            except OSError as e:
                alt = t.with_name(t.stem + "_new.pdf")
                shutil.copy2(final, alt)
                print(f"FINAL (locked) -> {alt}: {e}")

    print("\nDone. book/ was not used as output directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
