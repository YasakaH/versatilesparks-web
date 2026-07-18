import fitz, os

# Add cover page to V1 PDF
cover_path = "C:/Users/varas/personalities/cookbook/book/v1/cover-front.png"
pdf_path = "C:/Users/varas/personalities/cookbook/book/dist-v1/Python-Browser-Automation-Cookbook.pdf"

doc = fitz.open(pdf_path)
# Check if page 0 is already a cover image
page0_text = doc[0].get_text()
if "Python Browser Automation Cookbook" in page0_text and len(doc[0].get_images()) == 0:
    # Create cover page from image
    cover_pix = fitz.Pixmap(cover_path)
    cover_page = doc.new_page(-1, width=cover_pix.width, height=cover_pix.height)
    cover_page.insert_image(cover_page.rect, pixmap=cover_pix)
    # Move cover to front
    doc.move_page(doc.page_count - 1, 0)
    # Save to temp and replace
    tmp = pdf_path.replace('.pdf', '_tmp.pdf')
    doc.save(tmp, incremental=False, deflate=True)
    doc.close()
    os.replace(tmp, pdf_path)
    doc = fitz.open(pdf_path)
    print(f"V1 cover prepended. Total pages: {len(doc)}")
else:
    print("V1 cover already present")
doc.close()

# Add cover page to V2 PDF
cover_path = "C:/Users/varas/personalities/cookbook/book/v2/Images/cover-front.png"
pdf_path = "C:/Users/varas/personalities/cookbook/book/dist/Browser Automation Playbook.pdf"

doc = fitz.open(pdf_path)
page0_text = doc[0].get_text()
if "Browser Automation Playbook" in page0_text and len(doc[0].get_images()) == 0:
    cover_pix = fitz.Pixmap(cover_path)
    cover_page = doc.new_page(-1, width=cover_pix.width, height=cover_pix.height)
    cover_page.insert_image(cover_page.rect, pixmap=cover_pix)
    doc.move_page(doc.page_count - 1, 0)
    tmp = pdf_path.replace('.pdf', '_tmp.pdf')
    doc.save(tmp, incremental=False, deflate=True)
    doc.close()
    os.replace(tmp, pdf_path)
    doc = fitz.open(pdf_path)
    print(f"V2 cover prepended. Total pages: {len(doc)}")
else:
    print("V2 cover already present")
doc.close()

# Add cover to Reference Library PDF
cover_path = "C:/Users/varas/personalities/cookbook/book/v2/Images/cover-front.png"
pdf_path = "C:/Users/varas/personalities/cookbook/book/dist/reference-library/Production Reference Library.pdf"

doc = fitz.open(pdf_path)
cover_pix = fitz.Pixmap(cover_path)
cover_page = doc.new_page(-1, width=cover_pix.width, height=cover_pix.height)
cover_page.insert_image(cover_page.rect, pixmap=cover_pix)
doc.move_page(doc.page_count - 1, 0)
doc.save(pdf_path, incremental=False, deflate=True)
print(f"Reference Library cover prepended. Total pages: {len(doc)}")
doc.close()

print("All covers done")
