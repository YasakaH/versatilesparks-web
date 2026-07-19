import os
import re

# Root paths
ROOT = "C:/Users/varas/personalities/cookbook"
V1_DIR = os.path.join(ROOT, "book/v1")
V2_DIR = os.path.join(ROOT, "book/v2")
OUTPUT_DIR = os.path.join(ROOT, "website-next/content/recipes")

# Clear existing output directory to remove colliding recipe files
if os.path.exists(OUTPUT_DIR):
    for f in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, f))
else:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helper to determine concept mapping based on chapter number
def get_concepts_for_chapter(ch_num, book_id):
    if book_id == "cookbook":
        mapping = {
            1: ["profiles"],
            2: ["cdp"],
            3: ["authentication"],
            4: ["cookies", "sessions"],
            5: ["anti-detection", "fingerprints"],
            6: ["cdp", "network-interception"],
            7: ["observability"],
            8: ["scaling"],
            9: ["recovery"]
        }
        return mapping.get(ch_num, ["profiles"])
    else:
        # V2 Playbook
        mapping = {
            1: ["profiles"],
            2: ["profiles"],
            3: ["observability", "recovery"],
            4: ["authentication"],
            5: ["authentication", "sessions", "cookies"],
            6: ["network-interception"],
            7: ["anti-detection", "fingerprints"],
            8: ["scaling"],
            9: ["cdp", "network-interception", "observability"],
            10: ["profiles"],
            11: ["anti-detection"],
            12: ["scaling", "observability", "recovery"],
            13: ["network-interception"],
            14: ["recovery"]
        }
        return mapping.get(ch_num, ["profiles"])

def generate_v1():
    # Loop V1 chapters
    for fn in os.listdir(V1_DIR):
        if not fn.startswith("chapter-") or not fn.endswith(".md"):
            continue
        
        ch_num = int(re.search(r"chapter-(\d+)", fn).group(1))
        file_path = os.path.join(V1_DIR, fn)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Matches "## Recipe 1: Title"
        recipes = re.findall(r"## Recipe (\d+):\s*(.*)", content)
        for r_num_str, r_title in recipes:
            r_num = int(r_num_str)
            r_title = r_title.strip()
            
            concepts = get_concepts_for_chapter(ch_num, "cookbook")
            difficulty = "Beginner" if r_num <= 5 else ("Intermediate" if r_num <= 10 else "Advanced")
            
            mdx_content = f"""---
id: "recipe-v1-{r_num}"
title: "{r_title}"
concepts: {repr(concepts)}
difficulty: "{difficulty}"
environment: ["Python", "nodriver"]
downloads: ["recipes/0{r_num}_launch_browser.py"]
book: "cookbook"
---

This recipe covers '{r_title}' from Chapter {ch_num} of the Python Browser Automation Cookbook.

### Implementation Goals

* Understand low-level CDP triggers.
* Implement structured async handlers.
* Prevent resource leakage.
"""
            out_path = os.path.join(OUTPUT_DIR, f"recipe-v1-{r_num}.mdx")
            with open(out_path, "w", encoding="utf-8") as out_f:
                out_f.write(mdx_content)
            print(f"Generated Cookbook V1 Recipe {r_num}: {r_title}")

def generate_v2():
    # Loop V2 chapters
    for fn in os.listdir(V2_DIR):
        if not fn.startswith("chapter-") or not fn.endswith(".md"):
            continue
        
        ch_num = int(re.search(r"chapter-(\d+)", fn).group(1))
        file_path = os.path.join(V2_DIR, fn)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Matches:
        # ## Recipe 13 — Find Elements Reliably
        # ## Recipe 31: Intercept and Analyze Network Traffic with CDP
        recipes = re.findall(r"## Recipe (\d+\w?)\s*[-:—–]\s*(.*)", content)
        for r_num_str, r_title in recipes:
            r_title = r_title.strip()
            concepts = get_concepts_for_chapter(ch_num, "playbook")
            
            # Simple difficulty distribution
            if ch_num <= 4:
                difficulty = "Beginner"
            elif ch_num <= 9:
                difficulty = "Intermediate"
            else:
                difficulty = "Advanced"
                
            mdx_content = f"""---
id: "recipe-v2-{r_num_str}"
title: "{r_title}"
concepts: {repr(concepts)}
difficulty: "{difficulty}"
environment: ["Python", "nodriver", "Docker"]
downloads: ["recipes/ch{ch_num:02d}/{r_num_str}_code.py"]
book: "playbook"
---

This recipe covers '{r_title}' from Chapter {ch_num} of the Browser Automation Playbook.

### Production Engineering Strategy

* Evade standard browser timing metrics.
* Route requests through backconnect residential proxy pools.
* Configure auto-healing watchdogs for lifecycle monitoring.
"""
            out_path = os.path.join(OUTPUT_DIR, f"recipe-v2-{r_num_str}.mdx")
            with open(out_path, "w", encoding="utf-8") as out_f:
                out_f.write(mdx_content)
            print(f"Generated Playbook V2 Recipe {r_num_str}: {r_title}")

if __name__ == "__main__":
    generate_v1()
    generate_v2()
    print("Done generating all recipe objects!")
