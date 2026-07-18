"""
Recipe 46 (V2): Package Automation With Docker

Problem: Every server has different Chrome versions, paths, and
dependencies. Docker gives you a reproducible runtime everywhere.
"""
import asyncio
from pathlib import Path

DOCKERFILE = """
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \\
    wget gnupg unzip \\
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \\
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \\
    && apt-get update && apt-get install -y google-chrome-stable \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV HEADLESS=true
CMD ["python", "main.py"]
"""


async def main():
    base = Path("./docker-automation")
    base.mkdir(exist_ok=True)
    (base / "Dockerfile").write_text(DOCKERFILE.strip())
    (base / "requirements.txt").write_text("nodriver>=0.50.3\n")
    (base / "main.py").write_text(
        'import asyncio\nimport nodriver as uc\n\n'
        'async def main():\n'
        '    browser = await uc.start(headless=True)\n'
        '    page = await browser.get("https://example.com")\n'
        '    print(f"OK: {await page.title()}")\n'
        '    await browser.stop()\n'
        'asyncio.run(main())\n'
    )
    print(f"Created Docker setup in {base}/")
    print("Build:  docker build -t automation ./docker-automation")
    print("Run:    docker run --rm automation")


if __name__ == "__main__":
    asyncio.run(main())
