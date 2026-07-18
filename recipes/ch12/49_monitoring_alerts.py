"""
Recipe 49 (V2): Add Monitoring and Alerts

Problem: Unattended automation fails silently. Get notified
when success rate drops or a critical error occurs.
"""
import asyncio, json, urllib.request
from pathlib import Path


def send_slack(webhook_url, message):
    payload = json.dumps({"text": message}).encode()
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)


def send_email(smtp_host, port, user, password, to, subject, body):
    import smtplib
    msg = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP(smtp_host, port) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, [to], msg.encode("utf-8"))


async def main():
    # Simulated monitoring
    pages_scraped = 150
    errors = 2
    success_rate = (pages_scraped - errors) / pages_scraped * 100
    threshold = 95

    status = "OK" if success_rate >= threshold else "DEGRADED"
    print(f"Status: {status} ({success_rate:.0f}% success)")

    if success_rate < threshold:
        print("Alert: Success rate below threshold")
        # send_slack("https://hooks.slack.com/...", f"Automation degraded: {success_rate:.0f}%")

    # Save monitoring log
    log = Path("monitoring.log")
    log.write_text(json.dumps({
        "pages": pages_scraped, "errors": errors,
        "success_rate": round(success_rate, 1), "status": status
    }))


if __name__ == "__main__":
    asyncio.run(main())
