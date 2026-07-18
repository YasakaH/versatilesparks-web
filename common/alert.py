"""
alert.py — Alert dispatcher for production automation.

Sends notifications when automation fails, validation thresholds
are exceeded, or human intervention is required.

Usage:
    from common.alert import AlertLevel, send_slack_alert, send_alert

    await send_alert("Price monitor failed", AlertLevel.ERROR)
"""

import os
import json
from enum import Enum
from urllib.request import Request, urlopen
from urllib.error import URLError


class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


LEVEL_COLORS = {
    AlertLevel.INFO: "#36a64f",
    AlertLevel.WARNING: "#f2c744",
    AlertLevel.ERROR: "#ef4444",
}


async def send_slack_alert(
    message: str,
    level: AlertLevel = AlertLevel.ERROR,
    details: str = "",
    webhook_url: str = "",
):
    """Send an alert to Slack via incoming webhook."""
    url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL", "")
    if not url:
        return

    payload = {
        "attachments": [
            {
                "color": LEVEL_COLORS.get(level, "#ef4444"),
                "title": f"[{level.value.upper()}] Automation Alert",
                "text": message,
                "fields": (
                    [{"title": "Details", "value": details, "short": False}]
                    if details
                    else []
                ),
            }
        ]
    }

    try:
        req = Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        urlopen(req, timeout=10)
    except URLError as e:
        print(f"Alert delivery failed: {e}")


async def send_alert(
    message: str,
    level: AlertLevel = AlertLevel.ERROR,
    details: str = "",
):
    """Send alert via configured channel(s). Currently supports Slack."""
    await send_slack_alert(message, level, details)
