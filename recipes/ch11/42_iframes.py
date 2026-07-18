"""
Recipe 42 (V2): Work With iFrames and Nested Contexts

Problem: Elements inside iFrames are in a separate document tree.
Normal selectors fail — you must switch contexts first.
"""
import asyncio
import nodriver as uc


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")

    frames = await page.find_all("iframe")
    print(f"Found {len(frames)} iframe(s)")

    for i, frame_el in enumerate(frames):
        try:
            frame = await frame_el.content_frame()
            if frame:
                title = await frame.title()
                print(f"  iFrame {i}: {title or '(no title)'}")
            else:
                print(f"  iFrame {i}: cross-origin (cannot access)")
        except Exception as e:
            print(f"  iFrame {i}: {e}")

    if not frames:
        print("No iframes on this page. Try a site like https://www.w3schools.com/html/html_iframe.asp")

    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
