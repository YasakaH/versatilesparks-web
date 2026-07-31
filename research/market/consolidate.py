#!/usr/bin/env python3
"""
Consolidate all iteration files into one master document.
Usage: python consolidate.py
"""

import os
import glob
import datetime

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research_outputs")

def collect_files():
    """Collect all iteration files, sorted by branch then depth."""
    all_files = []
    
    # Deep iteration files
    for f in sorted(glob.glob(os.path.join(OUT_DIR, "deep_*.txt"))):
        all_files.append(f)
    
    # Earlier phase iteration files
    for f in sorted(glob.glob(os.path.join(OUT_DIR, "iteration_L*.txt"))):
        if f not in all_files:
            all_files.append(f)
    
    return all_files

def consolidate():
    files = collect_files()
    
    print(f"Found {len(files)} files to consolidate")
    
    lines = []
    lines.append("=" * 70)
    lines.append("AUTOMATION RELIABILITY — CONSOLIDATED RESEARCH DOCUMENT")
    lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total files consolidated: {len(files)}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("")
    
    total_chars = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"[ERROR READING FILE: {e}]"
        
        # Extract the path from the file content for better headers
        path_info = ""
        for line in content.split("\n"):
            if line.startswith("Path:"):
                path_info = line.replace("Path:", "").strip()
                break
            elif line.startswith("CURRENT PROBLEM:"):
                path_info = line.replace("CURRENT PROBLEM:", "").strip()
                break
        
        lines.append("")
        lines.append("=" * 70)
        lines.append(f"FILE: {filename}")
        if path_info:
            lines.append(f"PATH: {path_info}")
        lines.append("=" * 70)
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("─" * 40)
        lines.append("")
        
        total_chars += len(content)
    
    # Write consolidated file
    output_path = os.path.join(OUT_DIR, "consolidated text file.txt")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    size_kb = os.path.getsize(output_path) / 1024
    print(f"\nConsolidated file written: {output_path}")
    print(f"Size: {size_kb:.1f} KB")
    print(f"Total characters: {total_chars:,}")
    print(f"Total files: {len(files)}")
    
    return output_path

if __name__ == "__main__":
    consolidate()
