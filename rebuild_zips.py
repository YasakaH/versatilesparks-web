import os
import zipfile
import shutil
import hashlib

# Root paths
ROOT = "C:/Users/varas/personalities/cookbook"
RELEASES = os.path.join(ROOT, "releases")
PRODUCTS = os.path.join(ROOT, "Products")

# Canonical Quarto Output Paths
V1_PDF_SRC = os.path.join(ROOT, "book/dist-v1/v1.pdf")
V1_EPUB_SRC = os.path.join(ROOT, "book/dist-v1/v1.epub")

V2_PDF_SRC = os.path.join(ROOT, "book/dist-v2/v2.pdf")
V2_EPUB_SRC = os.path.join(ROOT, "book/dist-v2/v2.epub")

# SHA256 helper
def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

# Quality/Existence check gate
def validate_gate(filepath, name):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"QA GATE FAILED: {name} not found at {filepath}")
    size = os.path.getsize(filepath)
    if size == 0:
        raise ValueError(f"QA GATE FAILED: {name} at {filepath} is empty (0 bytes)")
    print(f"QA PASS: {name} exists ({size / (1024*1024):.2f} MB)")

def add_folder_to_zip(zip_file, folder_path, added_set, zip_path_prefix=""):
    """Recursively adds a folder's contents to the zip file, avoiding duplicate paths."""
    if not os.path.exists(folder_path):
        return
    for root_dir, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for fn in files:
            if fn.endswith(('.pyc', '.pyo', '.zip', '.bak')):
                continue
            full_path = os.path.join(root_dir, fn)
            rel_path = os.path.relpath(full_path, folder_path)
            arcname = os.path.join(zip_path_prefix, rel_path).replace("\\", "/")
            if arcname.lower() not in added_set:
                zip_file.write(full_path, arcname)
                added_set.add(arcname.lower())

# Main packaging process
def main():
    print("Running Release QA Gate checks...")
    validate_gate(V1_PDF_SRC, "V1 PDF")
    validate_gate(V1_EPUB_SRC, "V1 EPUB")
    validate_gate(V2_PDF_SRC, "V2 PDF")
    validate_gate(V2_EPUB_SRC, "V2 EPUB")
    print("All QA checks passed. Packaging releases...")

    # === V1 Release ===
    v1_rel_dir = os.path.join(RELEASES, "v1.0.0")
    if os.path.exists(v1_rel_dir):
        shutil.rmtree(v1_rel_dir)
    os.makedirs(os.path.join(v1_rel_dir, "PDF"), exist_ok=True)
    os.makedirs(os.path.join(v1_rel_dir, "EPUB"), exist_ok=True)
    os.makedirs(os.path.join(v1_rel_dir, "ZIP"), exist_ok=True)

    # Destination paths for Release files (Consistent Naming)
    v1_pdf_dest = os.path.join(v1_rel_dir, "PDF/Python-Browser-Automation-Cookbook-v1.0.0.pdf")
    v1_epub_dest = os.path.join(v1_rel_dir, "EPUB/Python-Browser-Automation-Cookbook-v1.0.0.epub")
    v1_zip_dest = os.path.join(v1_rel_dir, "ZIP/Python-Browser-Automation-Cookbook-v1.0.0.zip")

    shutil.copy2(V1_PDF_SRC, v1_pdf_dest)
    shutil.copy2(V1_EPUB_SRC, v1_epub_dest)

    # Build V1 ZIP with PDF, EPUB, Code, and Docs
    v1_added = set()
    with zipfile.ZipFile(v1_zip_dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add PDF and EPUB to the root of the ZIP
        zf.write(v1_pdf_dest, "Python-Browser-Automation-Cookbook-v1.0.0.pdf")
        v1_added.add("python-browser-automation-cookbook-v1.0.0.pdf")
        zf.write(v1_epub_dest, "Python-Browser-Automation-Cookbook-v1.0.0.epub")
        v1_added.add("python-browser-automation-cookbook-v1.0.0.epub")

        # Add root and book/v1 extras
        v1_extras = [
            ("book/v1/CHANGELOG.md", "CHANGELOG.md"),
            ("book/v1/LICENSE.md", "LICENSE.md"),
            ("book/v1/VERSION", "VERSION"),
            ("book/v1/README.md", "README.md"),
            ("book/v1/cover-front.png", "cover-front.png"),
            ("book/v1/cover-back.png", "cover-back.png"),
        ]
        for src_rel, dest_rel in v1_extras:
            full_src = os.path.join(ROOT, src_rel)
            if os.path.exists(full_src):
                zf.write(full_src, dest_rel)
                v1_added.add(dest_rel.lower())

        # Add V1 code from common/ and recipes/
        add_folder_to_zip(zf, os.path.join(ROOT, "common"), v1_added, "code/common")
        add_folder_to_zip(zf, os.path.join(ROOT, "recipes"), v1_added, "code/recipes")

    # Copy V1 ZIP to Products directory
    prod_v1 = os.path.join(PRODUCTS, "Python Browser Automation Cookbook/v1.0.0/Python-Browser-Automation-Cookbook-v1.0.0.zip")
    os.makedirs(os.path.dirname(prod_v1), exist_ok=True)
    shutil.copy2(v1_zip_dest, prod_v1)

    # Write V1 SHA256SUMS
    with open(os.path.join(v1_rel_dir, "SHA256SUMS"), "w") as f:
        f.write(f"{get_sha256(v1_pdf_dest)}  PDF/Python-Browser-Automation-Cookbook-v1.0.0.pdf\n")
        f.write(f"{get_sha256(v1_epub_dest)}  EPUB/Python-Browser-Automation-Cookbook-v1.0.0.epub\n")
        f.write(f"{get_sha256(v1_zip_dest)}  ZIP/Python-Browser-Automation-Cookbook-v1.0.0.zip\n")

    # Write v1.0.0 release notes
    with open(os.path.join(v1_rel_dir, "release-notes.md"), "w") as f:
        f.write("# Release Notes v1.0.0\n\nPython Browser Automation Cookbook - Foundation Release.\n")

    print(f"V1 Packaging Complete. ZIP size: {os.path.getsize(v1_zip_dest) / (1024*1024):.2f} MB")


    # === V2 Release ===
    v2_rel_dir = os.path.join(RELEASES, "v2.0.0")
    if os.path.exists(v2_rel_dir):
        shutil.rmtree(v2_rel_dir)
    os.makedirs(os.path.join(v2_rel_dir, "PDF"), exist_ok=True)
    os.makedirs(os.path.join(v2_rel_dir, "EPUB"), exist_ok=True)
    os.makedirs(os.path.join(v2_rel_dir, "ZIP"), exist_ok=True)

    # Destination paths for Release files (Consistent Naming)
    v2_pdf_dest = os.path.join(v2_rel_dir, "PDF/Browser-Automation-Playbook-v2.0.0.pdf")
    v2_epub_dest = os.path.join(v2_rel_dir, "EPUB/Browser-Automation-Playbook-v2.0.0.epub")
    v2_zip_dest = os.path.join(v2_rel_dir, "ZIP/Browser-Automation-Playbook-v2.0.0.zip")

    shutil.copy2(V2_PDF_SRC, v2_pdf_dest)
    shutil.copy2(V2_EPUB_SRC, v2_epub_dest)

    # Build V2 ZIP
    v2_zip_prefix = "Browser-Automation-Playbook-v2.0.0"
    v2_added = set()
    with zipfile.ZipFile(v2_zip_dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add PDF and EPUB at root of the zip (inside directory)
        zf.write(v2_pdf_dest, f"{v2_zip_prefix}/Browser-Automation-Playbook-v2.0.0.pdf")
        v2_added.add(f"{v2_zip_prefix}/browser-automation-playbook-v2.0.0.pdf")
        zf.write(v2_epub_dest, f"{v2_zip_prefix}/Browser-Automation-Playbook-v2.0.0.epub")
        v2_added.add(f"{v2_zip_prefix}/browser-automation-playbook-v2.0.0.epub")

        # Add V2 extras from the book/v2/ folder
        v2_extras = [
            ("book/v2/CHANGELOG.md", "CHANGELOG.md"),
            ("book/v2/LICENSE.md", "LICENSE.md"),
            ("book/v2/dist-extra/VERSION", "VERSION"),
            ("book/v2/dist-extra/README.md", "README.md"),
            ("book/v2/dist-extra/docs/Errata.md", "docs/Errata.md"),
            ("book/v2/Images/cover-front.png", "Images/cover-front.png"),
            ("book/v2/Images/cover-back.png", "Images/cover-back.png"),
        ]
        for src_rel, dest_rel in v2_extras:
            full_src = os.path.join(ROOT, src_rel)
            if os.path.exists(full_src):
                arcname = f"{v2_zip_prefix}/{dest_rel}"
                zf.write(full_src, arcname)
                v2_added.add(arcname.lower())

        # Add V2 starter kit and code contents
        add_folder_to_zip(zf, os.path.join(ROOT, "browser-automation-starter"), v2_added, v2_zip_prefix)

    # Copy V2 ZIP to Products directory
    prod_v2 = os.path.join(PRODUCTS, "Browser Automation Playbook/v2.0.0/Browser-Automation-Playbook-v2.0.0.zip")
    os.makedirs(os.path.dirname(prod_v2), exist_ok=True)
    shutil.copy2(v2_zip_dest, prod_v2)

    # Write V2 SHA256SUMS (Consistent Naming)
    with open(os.path.join(v2_rel_dir, "SHA256SUMS"), "w") as f:
        f.write(f"{get_sha256(v2_pdf_dest)}  PDF/Browser-Automation-Playbook-v2.0.0.pdf\n")
        f.write(f"{get_sha256(v2_epub_dest)}  EPUB/Browser-Automation-Playbook-v2.0.0.epub\n")
        f.write(f"{get_sha256(v2_zip_dest)}  ZIP/Browser-Automation-Playbook-v2.0.0.zip\n")

    # Write v2.0.0 release notes
    with open(os.path.join(v2_rel_dir, "release-notes.md"), "w") as f:
        f.write("# Release Notes v2.0.0\n\nBrowser Automation Playbook - Production Engineering Release.\n")

    print(f"V2 Packaging Complete. ZIP size: {os.path.getsize(v2_zip_dest) / (1024*1024):.2f} MB")

    # Copy ZIP files to root folder as well for fallback / legacy support
    shutil.copy2(v1_zip_dest, os.path.join(ROOT, "Python-Browser-Automation-Cookbook-v1.0.0.zip"))
    shutil.copy2(v2_zip_dest, os.path.join(ROOT, "Browser-Automation-Playbook-v2.0.0.zip"))
    print("Legacy root copies generated.")

if __name__ == "__main__":
    main()
