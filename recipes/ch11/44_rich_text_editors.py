"""
Recipe 44 (V2): Handle Rich Text Editors

Problem: ContentEditable fields, rich text editors (like TinyMCE,
Quill, CKEditor) don't respond to standard input methods.
Use keyboard simulation and JS evaluation instead.
"""
import asyncio
import nodriver as uc


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")

    # Find contenteditable elements
    editable = await page.find("[contenteditable='true']", timeout=3)
    if editable:
        await editable.click()
        await page.send_keys("Hello from automation!")
        print("Typed into contenteditable field")
    else:
        print("No contenteditable found — try https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_global_contenteditable")

    # Alternative: set innerHTML via JS for editors that use divs
    await page.evaluate("() => {"
        "const ed = document.querySelector('[contenteditable]');"
        "if (ed) ed.innerHTML = '<p>Automated content</p>';"
    "}")
    print("JS injection fallback executed")

    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
