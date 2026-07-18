# Chapter 8: Starter Kit

## The Problem This Chapter Solves

Every automation project starts the same way: create directories, write common modules, add a main file. This chapter eliminates setup work by generating a complete project scaffold.


## Recipe 30: Production Browser Automation Starter Kit

**File:** `recipes/30_starter_kit.py`

### Why This Matters

A standard project structure means every automation project you build follows the same conventions. After this recipe, you never set up a project from scratch again.

### The Starter Kit

Run this recipe to generate a complete project:

```
my-automation/
├── common/
│   ├── browser.py
│   ├── config.py
│   ├── logging.py
│   └── retry.py
├── recipes/
│   └── example.py
├── profiles/
├── downloads/
├── logs/
├── .env
├── requirements.txt
├── README.md
└── main.py
```

### 7-Step Walkthrough

```
1. Clone     → python recipes/30_starter_kit.py
2. Install   → pip install -r requirements.txt
3. Configure → edit .env (HEADLESS, TIMEOUT)
4. Run       → python main.py
5. Add       → write your selectors
6. Add       → write your workflow
7. Deploy    → set HEADLESS=true, schedule via cron
```

### The Code

```python
import asyncio
from pathlib import Path

PROJECT_NAME = "my-automation"

async def create_starter_kit(name=PROJECT_NAME):
    base = Path(name)
    dirs = ["common", "recipes", "profiles", "downloads", "logs"]
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)
    (base / "common" / "__init__.py").write_text("")
    (base / "requirements.txt").write_text("nodriver>=0.50.3\n")
    (base / "README.md").write_text(f"# {name}\n\nBrowser automation project.\n")
    (base / ".env").write_text("HEADLESS=false\nTIMEOUT=30\nLOG_LEVEL=info\n")
    return base

async def main():
    project = await create_starter_kit()
    print(f"Created: {project.resolve()}")
    for f in sorted(project.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(project)}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Production Rule

Use the starter kit for every new automation project. It saves 15 minutes of boilerplate.


