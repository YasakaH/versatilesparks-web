"""Split README.md into per-chapter files in book/chapters/.

Detects # Chapter N, # Part, # Preface, etc. as split points.
Also creates Part-hint files for the Table of Contents flow.
"""
import re
from pathlib import Path

ROOT = Path("c:/Users/varas/personalities/cookbook")
README = ROOT / "README.md"
OUT = ROOT / "book" / "chapters"

text = README.read_text(encoding="utf-8")
lines = text.split("\n")

def chapter_number(title):
    m = re.search(r"Chapter (\d+)", title)
    return int(m.group(1)) if m else None

# Define all split points (h1 headings) and their target filenames
HEADINGS = {
    "# Preface": "preface.md",
    "# The Production Mindset": "production-mindset.md",
    "# How This Book Works": "how-this-book-works.md",
    "# How nodriver Actually Works": "how-nodriver-works.md",
}
# Add chapters by number
for i in range(0, 15):
    HEADINGS[f"# Chapter {i}:"] = f"chapter-{i:02d}.md"
# Add parts
HEADINGS["# Part I — Foundations"] = "part-i.md"
HEADINGS["# Part II — Interaction"] = "part-ii.md"
HEADINGS["# Part III — Extraction"] = "part-iii.md"
HEADINGS["# Part IV — Production"] = "part-iv.md"
HEADINGS["# Part V — Next Steps"] = "part-v.md"
HEADINGS["# Appendix"] = "appendix.md"
HEADINGS["# Epilogue"] = "epilogue.md"

# Split logic
current_key = None
current_lines = []
chunks = {}

for line in lines:
    # Check if this line starts any known heading
    matched = None
    for prefix in sorted(HEADINGS.keys(), key=len, reverse=True):
        # Handle prefixes like "# Chapter 1:" — need to match start of line
        if line.startswith(prefix):
            matched = prefix
            break
        # Also handle "# Chapter 10:" etc — must match exactly
    if matched:
        if current_key is not None:
            chunks[current_key] = current_lines
        current_key = matched
        current_lines = [line]
    elif current_key is not None:
        current_lines.append(line)

if current_key is not None:
    chunks[current_key] = current_lines

# Write files
written = []
for heading, filename in HEADINGS.items():
    if heading in chunks:
        content = "\n".join(chunks[heading]) + "\n"
        path = OUT / filename
        path.write_text(content, encoding="utf-8")
        cn = chapter_number(heading)
        lbl = f"Ch {cn}" if cn else heading.replace("# ", "")
        written.append(f"  ✓ {filename} ({lbl}, {len(content)} chars)")
    else:
        written.append(f"  - {filename} (NOT FOUND in README)")

print(f"Split results ({len(written)} files):")
for w in written:
    print(w)
