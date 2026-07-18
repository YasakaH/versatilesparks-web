import os
import fitz

ROOT = "C:/Users/varas/personalities/cookbook"
V1_PDF = os.path.join(ROOT, "releases/v1.0.0/PDF/Python-Browser-Automation-Cookbook-v1.0.0.pdf")
V2_PDF = os.path.join(ROOT, "releases/v2.0.0/PDF/Browser-Automation-Playbook-v2.0.0.pdf")

DOWNLOADS = os.path.join(ROOT, "website/downloads")

def extract_pdf_section(src_path, dest_path, max_pages):
    print(f"Extracting sample from {src_path} -> {dest_path}")
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source PDF not found: {src_path}")
        
    doc = fitz.open(src_path)
    sample_doc = fitz.open()
    
    # Insert from page 0 (first page) to min(max_pages, total_pages)
    to_page = min(max_pages, len(doc)) - 1
    sample_doc.insert_pdf(doc, from_page=0, to_page=to_page)
    
    # Save the output
    sample_doc.save(dest_path)
    sample_doc.close()
    doc.close()
    print(f"Sample extraction complete. Pages: {to_page+1}, Size: {os.path.getsize(dest_path)//1024} KB")

def main():
    os.makedirs(DOWNLOADS, exist_ok=True)
    
    # Extract first 12 pages for V1 (Cover, Frontmatter, TOC, Chapter 1)
    v1_dest = os.path.join(DOWNLOADS, "python-browser-automation-cookbook-sample.pdf")
    extract_pdf_section(V1_PDF, v1_dest, max_pages=12)
    
    # Extract first 22 pages for V2 (Cover, Frontmatter, TOC, Mindset, Chapter 1)
    v2_dest = os.path.join(DOWNLOADS, "browser-automation-playbook-sample.pdf")
    extract_pdf_section(V2_PDF, v2_dest, max_pages=22)

if __name__ == "__main__":
    main()
