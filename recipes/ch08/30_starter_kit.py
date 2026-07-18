"""
Recipe 30 (revised): Production Browser Automation Starter Kit

Generate a reusable automation project scaffold with full common/
modules, README, .env, and example recipe.
"""
import asyncio
from pathlib import Path

PROJECT_NAME = "browser-automation-starter"


async def create_starter_kit(name=PROJECT_NAME):
    """Generate a complete automation project scaffold."""
    base = Path(name)
    dirs = ["common", "recipes", "profiles", "downloads", "logs"]
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)

    # __init__.py
    (base / "common" / "__init__.py").write_text("")
    (base / "recipes" / "__init__.py").write_text("")

    # requirements.txt
    (base / "requirements.txt").write_text("nodriver>=0.50.3\n")

    # .env
    (base / ".env").write_text(
        "HEADLESS=false\nTIMEOUT=30\nLOG_LEVEL=info\nCDP_PORT=9222\n"
    )

    # .gitignore
    (base / ".gitignore").write_text(
        ".venv/\n__pycache__/\n*.pyc\n.env\nprofiles/\ndownloads/\nlogs/\n"
    )

    # README.md
    (base / "README.md").write_text(
        f"# {name}\n\n"
        f"Browser automation project generated from the Python Browser Automation Cookbook.\n\n"
        f"## Setup\n\n"
        f"```bash\npython -m venv .venv\nsource .venv/bin/activate  # or .venv\\Scripts\\activate\n"
        f"pip install --upgrade pip\npip install -r requirements.txt\n```\n\n"
        f"## Usage\n\n"
        f"```bash\npython main.py\n```\n"
    )

    # main.py
    (base / "main.py").write_text(
        "import asyncio\n"
        "from common.browser import launch_browser, close_browser\n"
        "from common.logging import logger\n\n\n"
        "async def main():\n"
        '    logger.info("Starting automation")\n'
        "    browser = await launch_browser()\n"
        '    page = await browser.get("https://example.com")\n'
        "    title = await page.title()\n"
        f'    logger.info(f"Loaded: {{title}}")\n'
        "    await close_browser(browser)\n\n\n"
        'if __name__ == "__main__":\n'
        "    asyncio.run(main())\n"
    )

    # common/browser.py
    (base / "common" / "browser.py").write_text(
        '"""Browser lifecycle utilities."""\n\n'
        "import asyncio\n"
        "import nodriver as uc\n"
        "from common.config import HEADLESS, CDP_PORT, logger\n\n\n"
        "async def launch_browser(**kwargs):\n"
        '    """Launch a Chrome browser instance."""\n'
        "    options = {\n"
        '        "headless": HEADLESS,\n'
        "    }\n"
        "    options.update(kwargs)\n"
        "    if options.get(\"user_data_dir\"):\n"
        '        user_data_dir = options.pop("user_data_dir")\n'
        "        browser = await uc.start(user_data_dir=user_data_dir, **options)\n"
        "    else:\n"
        "        browser = await uc.start(**options)\n"
        '    logger.info("Browser launched")\n'
        "    return browser\n\n\n"
        "async def close_browser(browser):\n"
        '    """Close the browser instance."""\n'
        "    try:\n"
        "        browser.stop()\n"
        '        logger.info("Browser closed")\n'
        "    except Exception:\n"
        "        pass\n"
    )

    # common/config.py
    (base / "common" / "config.py").write_text(
        '"""Centralized configuration from environment variables."""\n\n'
        "import os\n\n"
        "HEADLESS = os.environ.get(\"HEADLESS\", \"false\").lower() == \"true\"\n"
        'TIMEOUT = int(os.environ.get("TIMEOUT", "30"))\n'
        'CDP_PORT = int(os.environ.get("CDP_PORT", "9222"))\n'
        'LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()\n'
    )

    # common/logging.py
    (base / "common" / "logging.py").write_text(
        '"""Structured stdout logger."""\n\n'
        "import logging\n"
        "from common.config import LOG_LEVEL\n\n"
        "logging.basicConfig(\n"
        "    level=getattr(logging, LOG_LEVEL, logging.INFO),\n"
        '    format="%(asctime)s [%(levelname)s] %(message)s",\n'
        '    datefmt="%H:%M:%S",\n'
        ")\n"
        "logger = logging.getLogger(\"browser\")\n"
    )

    # common/retry.py
    (base / "common" / "retry.py").write_text(
        '"""Async retry with configurable backoff."""\n\n'
        "import asyncio\n"
        "from common.logging import logger\n\n\n"
        "async def retry(fn, *args, exceptions=(TimeoutError,), max_retries=3, delay=2, **kwargs):\n"
        '    """Retry a function on specific exceptions."""\n'
        "    last_error = None\n"
        "    for attempt in range(1, max_retries + 1):\n"
        "        try:\n"
        "            return await fn(*args, **kwargs)\n"
        "        except exceptions as e:\n"
        f'            logger.warning(f"Attempt {{attempt}}/{{max_retries}} failed: {{e}}")\n'
        "            last_error = e\n"
        "            if attempt < max_retries:\n"
        "                await asyncio.sleep(delay)\n"
        f'    logger.error(f"All {{max_retries}} attempts failed")\n'
        "    raise last_error\n"
    )

    # recipes/example.py
    (base / "recipes" / "example.py").write_text(
        '"""Example recipe: find and click an element."""\n\n'
        "import asyncio\n"
        "from common.browser import launch_browser, close_browser\n"
        "from common.logging import logger\n\n\n"
        "async def main():\n"
        '    logger.info("Starting example recipe")\n'
        "    browser = await launch_browser()\n"
        '    page = await browser.get("https://example.com")\n'
        "    link = await page.find(\"a\")\n"
        "    if link:\n"
        f'        logger.info(f"Found link: {{link.text}}")\n'
        "    await close_browser(browser)\n\n\n"
        'if __name__ == "__main__":\n'
        "    asyncio.run(main())\n"
    )

    return base


async def main():
    project = await create_starter_kit()
    print(f"Created: {project.resolve()}")
    print("Files:")
    for f in sorted(project.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(project)}")


if __name__ == "__main__":
    asyncio.run(main())
