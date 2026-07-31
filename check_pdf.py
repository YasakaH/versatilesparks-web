from pypdf import PdfReader
r = PdfReader(r'E:\Hermes Projects\cookbook\dist-v2\Browser-Automation-Playbook-print.pdf')

print(f"Total pages: {len(r.pages)}")
unique_sizes = set()
for i in range(len(r.pages)):
    p = r.pages[i]
    mb = tuple(p.mediabox)
    unique_sizes.add(mb)
    if i < 7:
        print(f"Page {i+1}: MediaBox={mb}")

print(f"\nUnique page sizes: {len(unique_sizes)}")
print(f"All consistent: {len(unique_sizes) == 1}")

# Check for any unusually small or large pages
for i, p in enumerate(r.pages):
    w, h = float(p.mediabox.width), float(p.mediabox.height)
    if abs(w - 432) > 1 or abs(h - 648) > 1:
        print(f"Suspicious page {i+1}: {w}x{h}")
