"""
Recipe 47 (V2): Schedule Browser Jobs

Problem: Manual execution doesn't scale. Schedule automation
using cron (Linux), Task Scheduler (Windows), or job runners.
"""
import asyncio
from pathlib import Path

CRONTAB_ENTRY = "# Run daily at 6 AM\n30 6 * * * cd /home/user/automation && python main.py >> logs/cron.log 2>&1\n"
SCHEDULER_SCRIPT = """# Windows Task Scheduler PowerShell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "main.py" -WorkingDirectory "C:\\automation"
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00AM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "BrowserAutomation" -Action $action -Trigger $trigger -Settings $settings
"""


async def main():
    base = Path("./scheduler-setup")
    base.mkdir(exist_ok=True)
    (base / "crontab.example").write_text(CRONTAB_ENTRY)
    (base / "windows_scheduler.ps1").write_text(SCHEDULER_SCRIPT.strip())
    (base / "main.py").write_text(
        'import asyncio\nimport nodriver as uc\n\n'
        'async def main():\n'
        '    print("Scheduled automation started")\n'
        '    browser = await uc.start(headless=True)\n'
        '    page = await browser.get("https://example.com")\n'
        '    print(f"OK: {await page.title()}")\n'
        '    await browser.stop()\n'
        'asyncio.run(main())\n'
    )
    print("Scheduler templates created:")
    print("  Linux:   crontab crontab.example")
    print("  Windows: powershell -File windows_scheduler.ps1")


if __name__ == "__main__":
    asyncio.run(main())
