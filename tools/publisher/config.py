import os
from pathlib import Path
from dotenv import load_dotenv


def _find_env() -> list[Path]:
    script_dir = Path(__file__).resolve().parents[2]
    candidates = [
        script_dir / ".env",
        Path.home() / "AppData/Local/hermes/.env",
        Path.home() / ".env",
    ]
    return [p for p in candidates if p.exists()]


def load_config() -> dict[str, str | None]:
    for env_path in _find_env():
        load_dotenv(env_path)

    return {
        "devto_api_key": os.getenv("DEVTO_API_KEY"),

        "github_pat": os.getenv("GITHUB_PAT"),
        "medium_token": os.getenv("MEDIUM_TOKEN"),
    }
