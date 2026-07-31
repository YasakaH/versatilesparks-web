import sys
try:
    import fitz  # PyMuPDF
except ImportError:
    print("NO_FITZ")
    sys.exit(1)

pdf_path = r"E:\Hermes Projects\cookbook\dist-v2\index.pdf"
doc = fitz.open(pdf_path)

# Render pages 52, 53, 54 (0-indexed: 51, 52, 53)
for page_num in [52, 53, 54]:
    page = doc[page_num]
    mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for clarity
    pix = page.get_pixmap(matrix=mat)
    out_path = rf"C:\Users\varas\AppData\Local\Temp\page_{page_num+1}.png"
    pix.save(out_path)
    print(f"Saved page {page_num+1}: {pix.width}x{pix.height} -> {out_path}")

print(f"Total pages: {doc.page_count}")
