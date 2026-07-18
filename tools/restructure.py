"""Create V2 chapter files and move recipes into chNN/ directories."""
import shutil
from pathlib import Path

ROOT = Path("c:/Users/varas/personalities/cookbook")
RECIPES = ROOT / "recipes"
CHAPTERS = ROOT / "book" / "chapters"

# Recipe -> chapter mapping
V1 = {
    "01": ("01", "Launch and Close a Browser"),
    "02": ("01", "Open and Manage Browser Tabs"),
    "03": ("01", "Reuse a Browser Profile"),
    "04": ("01", "Customize Browser Startup"),
    "05": ("02", "Navigate Like a User"),
    "06": ("02", "Capture Screenshots"),
    "07": ("02", "Execute JavaScript in the Page"),
    "08": ("02", "Inspect Browser State"),
    "09": ("03", "Wait for the Right Moment"),
    "10": ("03", "Build a Robust Retry System"),
    "11": ("03", "Add Logging to Your Automation"),
    "12": ("03", "Manage Configuration"),
    "13": ("04", "Find Elements Reliably"),
    "14": ("04", "Click Elements That Actually Work"),
    "15": ("04", "Fill Forms Like a User"),
    "16": ("04", "Upload Files"),
    "17": ("04", "Handle Dropdowns and Selects"),
    "18": ("04", "Recover From Unexpected Modals"),
    "19": ("05", "Log Into Any Website"),
    "20": ("05", "Save and Restore Cookies"),
    "21": ("05", "Validate Authentication"),
    "22": ("05", "Handle Session Expiry"),
    "23": ("06", "Extract Data From Tables"),
    "24": ("06", "Navigate Paginated Results"),
    "25": ("06", "Scroll Infinite Pages"),
    "26": ("06", "Download Files Safely"),
    "27": ("06", "Extract Media Content"),
    "28": ("07", "Handle Browser Crashes"),
    "29": ("07", "Build a Reliable Retry Pipeline"),
    "30": ("08", "Build Production Starter Kit"),
}

V2 = {
    "31": ("09", "Intercept and Analyze Network Traffic with CDP"),
    "32": ("09", "Block Unnecessary Resources for Performance"),
    "33": ("09", "Debug Through Console Logs"),
    "34": ("09", "Measure Browser Performance"),
    "35": ("09", "Emulate Different Browser Environments"),
    "36": ("10", "Audit Your Browser Environment"),
    "37": ("10", "Create Consistent Browser Environments"),
    "38": ("10", "Diagnose Environment Differences"),
    "39": ("10", "Audit Timezone, Language & Locale"),
    "40": ("10", "Debug Automation Compatibility Issues"),
    "41": ("11", "Automate Drag and Drop"),
    "42": ("11", "Work With iFrames"),
    "43": ("11", "Automate Shadow DOM"),
    "44": ("11", "Handle Rich Text Editors"),
    "45": ("11", "Automate Keyboard and Clipboard"),
    "46": ("12", "Package Automation With Docker"),
    "47": ("12", "Schedule Browser Jobs"),
    "48": ("12", "Store Automation Data"),
    "49": ("12", "Add Monitoring and Alerts"),
    "50": ("12", "Build Health Checks and Recovery"),
    "51": ("13", "Clean and Normalize Data"),
    "52": ("13", "Deduplicate Data"),
    "53": ("13", "Export Data"),
    "54": ("13", "Incremental Data Collection"),
    "55": ("13", "Data Quality and Validation Pipeline"),
    "56": ("14", "Build a Price Monitoring System"),
    "57": ("14", "Build a SaaS Dashboard Automation"),
    "58": ("14", "Build a Lead Management Workflow"),
    "59": ("14", "Build a Data Collection Pipeline"),
    "60": ("14", "Build the Automation Platform"),
}

# Move recipe files into chapter directories
for num, (ch, title) in {**V1, **V2}.items():
    src = RECIPES / f"{num}_{recipe_name(num, title)}.py"
    # Find the actual file
    found = list(RECIPES.glob(f"{num}_*.py"))
    if found:
        dst_dir = RECIPES / f"ch{ch}"
        dst = dst_dir / found[0].name
        shutil.move(str(found[0]), str(dst))
        print(f"  ✓ Moved {found[0].name} → recipes/ch{ch}/")
    else:
        print(f"  ✗ Not found: {num}_*.py")

print("\nDone moving recipe files.")
