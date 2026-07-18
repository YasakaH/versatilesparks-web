"""
Recipe 38 (V2): Diagnose Environment Differences

Chapter 10 — Browser Fingerprints, Reliability & Compatibility

Problem: Dev, staging, and production need different browser states.
Isolate profiles per environment and diagnose discrepancies.

Prerequisites:
  Recipe 3: Persistent profiles
  Recipe 6: Configuration system
"""
import asyncio, json
from pathlib import Path
import nodriver as uc

ENVS = {"dev": "./profiles/dev", "staging": "./profiles/staging", "production": "./profiles/prod"}


async def setup_environment(name):
    profile_dir = Path(ENVS[name])
    profile_dir.mkdir(parents=True, exist_ok=True)
    browser = await uc.start(user_data_dir=str(profile_dir))
    page = await browser.get("https://httpbin.org/cookies/set?env=" + name)
    cookies = browser.cookies
    (profile_dir / "cookies.json").write_text(json.dumps(cookies, indent=2))
    print(f"Environment '{name}' initialized at {profile_dir}")
    await browser.stop()


async def main():
    for env in ENVS:
        await setup_environment(env)


if __name__ == "__main__":
    asyncio.run(main())
