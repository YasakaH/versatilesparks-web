import os, sys
from PyPDF2 import PdfReader, PdfWriter

input_pdf = r"E:\Hermes Projects\cookbook\dist-v2\index.pdf"
output_pdf = r"E:\Hermes Projects\cookbook\dist-v2\Browser-Automation-Playbook-print.pdf"

reader = PdfReader(input_pdf)
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

if "/Outlines" in writer._root_object:
    del writer._root_object["/Outlines"]
    print("Stripped bookmarks/outlines")
else:
    print("No outlines to strip")

with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"Saved: {os.path.getsize(output_pdf) / (1024*1024):.1f} MB, {writer.getNumPages()} pages")
