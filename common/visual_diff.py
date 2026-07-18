"""
visual_diff.py — Region-Based Visual Comparison

Compare important page regions by DOM structure, not pixels.
Avoids false positives from ads, timestamps, and dynamic content.

Principle:
  ❌ Compare entire screenshot (ads, timestamps, animations change)
  ✅ Compare stable regions by DOM structure (tag tree comparison)

Usage:
    from common.visual_diff import compare_regions, generate_report

    diffs = compare_regions(old_html, new_html, selectors=["#price", ".product-details"])
    report = generate_report(diffs)
    print(report)

    # Optional: include screenshot comparison (requires Pillow)
    from common.visual_diff import screenshot_diff
    changed = screenshot_diff("before.png", "after.png", "diff.png")
"""
from dataclasses import dataclass, field
import json
import hashlib
import logging

logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    # Minimal fallback for when BeautifulSoup isn't installed

    class BeautifulSoup:  # type: ignore
        def __init__(self, html, parser):
            self.html = html

        def select_one(self, selector):
            return None

        def find_all(self, **kwargs):
            return []


@dataclass
class RegionDiff:
    """Result of comparing one page region.

    Attributes:
        selector: CSS selector for the compared region.
        changed: True if structure differs between before and after.
        before: Tag structure of the region before the change.
        after: Tag structure of the region after the change.
    """
    selector: str
    changed: bool
    before: str = ""
    after: str = ""


def normalize_html(html: str):
    """Parse HTML and strip dynamic values for stable comparison.

    Removes data-time, data-timestamp, data-random, and similar
    attributes that change on every page load.
    """
    soup = BeautifulSoup(html, "html.parser")
    if not HAS_BS4:
        return soup

    # Strip dynamic attribute values
    dynamic_attrs = {"data-time", "data-timestamp", "data-random",
                     "data-session", "data-cache", "nonce"}
    for tag in soup.find_all(attrs={a: True for a in dynamic_attrs}):
        for attr in dynamic_attrs:
            if attr in tag.attrs:
                del tag[attr]

    return soup


def extract_structure(element) -> list:
    """Extract the tag-name tree of an element (ignoring text content).

    Returns a list of tag names in document order, which is stable
    across page loads as long as the DOM structure doesn't change.
    """
    if not element:
        return []
    return [
        child.name for child in element.find_all(recursive=True)
        if child.name
    ]


def compare_regions(before_html: str, after_html: str, selectors: list) -> list:
    """Compare specific page regions between two HTML snapshots.

    Args:
        before_html: Raw HTML of the page before the change.
        after_html: Raw HTML of the page after the change.
        selectors: List of CSS selector strings identifying stable regions.

    Returns:
        List of RegionDiff dataclass instances.
    """
    before = normalize_html(before_html)
    after = normalize_html(after_html)

    results = []
    for selector in selectors:
        b = before.select_one(selector) if hasattr(before, 'select_one') else None
        a = after.select_one(selector) if hasattr(after, 'select_one') else None

        if not b or not a:
            results.append(RegionDiff(
                selector=selector,
                changed=True,
                before=str(b) if b else "MISSING",
                after=str(a) if a else "MISSING",
            ))
            continue

        before_structure = extract_structure(b)
        after_structure = extract_structure(a)
        results.append(RegionDiff(
            selector=selector,
            changed=before_structure != after_structure,
            before=str(before_structure),
            after=str(after_structure),
        ))

    return results


def generate_report(diffs: list) -> str:
    """Generate a human-readable diff report from comparison results.

    Args:
        diffs: List of RegionDiff from compare_regions().

    Returns:
        JSON-formatted report string with changed regions.
    """
    report = []
    for diff in diffs:
        entry = {
            "region": diff.selector,
            "status": "CHANGED" if diff.changed else "unchanged",
        }
        if diff.changed:
            entry["before"] = diff.before[:500],
            entry["after"] = diff.after[:500],
        report.append(entry)
    return json.dumps(report, indent=2)


def screenshot_diff(before_path: str, after_path: str, output_path: str) -> dict:
    """Optional: compare two screenshots and highlight differences.

    Requires Pillow. Gracefully returns error dict if not installed.

    Args:
        before_path: Path to baseline screenshot.
        after_path: Path to current screenshot.
        output_path: Path to save diff image.

    Returns:
        Dict with 'changed' bool and 'diff_path' or 'error'.
    """
    try:
        from PIL import Image, ImageChops
        before = Image.open(before_path)
        after = Image.open(after_path)

        if before.size != after.size:
            return {"changed": True, "error": "Dimension mismatch", "diff_path": None}

        diff = ImageChops.difference(before, after)
        if diff.getbbox():
            overlay = Image.new("RGBA", before.size, (0, 0, 0, 0))
            for x in range(before.width):
                for y in range(before.height):
                    if diff.getpixel((x, y)) != (0, 0, 0):
                        overlay.putpixel((x, y), (255, 0, 0, 80))
            combined = Image.alpha_composite(before.convert("RGBA"), overlay)
            combined.save(output_path)
            return {"changed": True, "diff_path": output_path, "error": None}

        return {"changed": False, "diff_path": None, "error": None}

    except ImportError:
        return {"changed": None, "diff_path": None,
                "error": "Pillow not installed (pip install Pillow for screenshot diffs)"}
    except Exception as e:
        return {"changed": None, "diff_path": None, "error": str(e)}
