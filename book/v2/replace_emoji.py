import os, re

V2 = "C:/Users/varas/personalities/cookbook/book/v2"

# Emoji → text replacements for print-friendly output
replacements = {
    "\u2705": "[✓]",    # ✅
    "\u274C": "[✗]",    # ❌
    "\u2B50": "★",       # ⭐
    "\u26A0\uFE0F": "[!]", # ⚠️ with variation selector
    "\u26A0": "[!]",     # ⚠ without variation selector
    "\U0001F534": "[CRIT]", # 🔴
    "\U0001F7E2": "[OK]",   # 🟢
    "\U0001F7E3": "[DEV]",  # 🟣
    "\U0001F7E0": "[SEN]",  # 🟠
    "\U0001F527": "[FIX]",  # 🔧
    "\u2764": "",         # ♥ bare (was in some files)
    "\U0001F4D6": "",     # 📖
    "\u2193": "\u2193",   # ↓ — keep as-is
    "\u2191": "\u2191",   # ↑ — keep as-is
    "\U0001F449": "→",    # 👉
    "\U0001F4A1": "",     # 💡
    "\U0001F6A7": "",     # 🚧
    "\U0001F50D": "",     # 🔍
    "\U0001F511": "",     # 🔑
    "\u2728": "",         # ✨
    "\U0001F4CC": "",     # 📌
    "\u0023\uFE0F\u20E3": "#",  # #️⃣
    "\u0031\uFE0F\u20E3": "1",  # 1️⃣
    "\u0032\uFE0F\u20E3": "2",  # 2️⃣
    "\u0033\uFE0F\u20E3": "3",  # 3️⃣
    "\u0034\uFE0F\u20E3": "4",  # 4️⃣
    "\u0035\uFE0F\u20E3": "5",  # 5️⃣
    "\U0001F51C": "[...]", # 🔜
    "★": "*",             # Some stars → asterisk
}

def replace_emoji(text):
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    return text

for root, dirs, files in os.walk(V2):
    for fname in files:
        if fname.endswith(".md") or fname.endswith(".qmd"):
            path = os.path.join(root, fname)
            content = open(path, encoding="utf-8").read()
            new_content = replace_emoji(content)
            if new_content != content:
                open(path, "w", encoding="utf-8").write(new_content)
                changes = sum(1 for e, r in replacements.items() if e in content)
                print(f"Replaced in {os.path.relpath(path, V2)}")

print("\nDone! All emoji replaced with print-safe alternatives.")
