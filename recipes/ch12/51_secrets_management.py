"""
Recipe 51 (V2): Secure Credential Management

Never hardcode passwords. Use .env files with environment
variables for local dev, docker secrets for production.
"""
import os
from pathlib import Path


def load_credentials(file=".env"):
    """Load credentials from .env file. Returns dict."""
    creds = {}
    env_path = Path(file)
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip()
    return creds


def get_secret(name, default=None):
    """Get secret from environment or .env file."""
    return os.environ.get(name, load_credentials().get(name, default))


async def main():
    username = get_secret("LOGIN_USER")
    password = get_secret("LOGIN_PASSWORD")
    if username and password:
        print(f"Credentials loaded for {username}")
    else:
        print("No credentials found. Create a .env file.")


if __name__ == "__main__":
    asyncio.run(main())
