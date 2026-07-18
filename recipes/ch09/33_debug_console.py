"""
Recipe 33 (V2): Debug Web Applications Through Console Logs

Problem: Automation fails because JavaScript fails silently.
Capture console errors, warnings, and exceptions as they happen.
"""
import asyncio
import nodriver as uc


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")

    captured = []

    async def on_console(event):
        level = event.type
        text = " ".join(str(a.value or "") for a in (event.args or []) if a.value)
        captured.append({"level": level, "text": text})
        if level == "error":
            print(f"[JS ERROR] {text[:200]}")

    page.add_handler(uc.cdp.runtime.ConsoleAPICalled, on_console)

    # Trigger test messages
    await page.evaluate("console.warn('Deprecated API'); console.error('Network failure');")
    await page.sleep(2)
    print(f"Captured {len(captured)} console messages")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
