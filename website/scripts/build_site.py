import os
import json
import xml.etree.ElementTree as ET
from jinja2 import Template

ROOT = "C:/Users/varas/personalities/cookbook"
WEBSITE = os.path.join(ROOT, "website")
BOOKS_DIR = os.path.join(WEBSITE, "books")
TEMPLATES_DIR = os.path.join(WEBSITE, "templates")

# Helper to read files
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# Helper to write files
def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {filepath}")

# Load Book Metadata
def load_books():
    books = []
    for fn in os.listdir(BOOKS_DIR):
        if fn.endswith('.json'):
            fp = os.path.join(BOOKS_DIR, fn)
            with open(fp, 'r', encoding='utf-8') as f:
                books.append(json.load(f))
    return sorted(books, key=lambda x: x['title'])

def get_base_context(title, description, canonical_path, og_type="website"):
    domain = "https://versatilesparks.qzz.io"
    return {
        "title": title,
        "description": description,
        "canonical_url": f"{domain}{canonical_path}",
        "og_image": f"{domain}/assets/covers/browser-automation-playbook-cover.png", # Default OG
        "og_type": og_type
    }

def main():
    books = load_books()

    # Load templates
    layout_tmpl = read_file(os.path.join(TEMPLATES_DIR, "layout.html"))
    index_tmpl = read_file(os.path.join(TEMPLATES_DIR, "index.html"))
    product_tmpl = read_file(os.path.join(TEMPLATES_DIR, "product.html"))
    changelog_tmpl = read_file(os.path.join(TEMPLATES_DIR, "changelog.html"))
    errata_tmpl = read_file(os.path.join(TEMPLATES_DIR, "errata.html"))
    simple_tmpl = read_file(os.path.join(TEMPLATES_DIR, "simple.html"))

    # === 1. Render Homepage (index.html) ===
    home_ctx = get_base_context(
        title="Versatile Sparks — Author Yasaka Hanini",
        description="Practical, production-grade handbooks for browser automation, site reliability, and data engineering workflows using Python and nodriver.",
        canonical_path="/"
    )
    # Inject Organization and Website Schemas
    home_schemas = [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Versatile Sparks",
            "url": "https://versatilesparks.qzz.io",
            "logo": "https://versatilesparks.qzz.io/favicon.svg",
            "publishingPrinciples": "https://versatilesparks.qzz.io/about.html",
            "founder": {
                "@type": "Person",
                "name": "Yasaka Hanini",
                "email": "yasaka.hanini@protonmail.com"
            }
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Versatile Sparks",
            "url": "https://versatilesparks.qzz.io"
        }
    ]
    home_ctx["json_ld_schemas"] = "\n".join([f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in home_schemas])
    
    # Render body
    home_body = Template(index_tmpl).render(books=books)
    home_html = Template(layout_tmpl).render(**home_ctx, content=home_body)
    write_file(os.path.join(WEBSITE, "index.html"), home_html)


    # === 2. Render Book Product Pages & Changelogs ===
    for book in books:
        book_dir = os.path.join(WEBSITE, "books", book["id"])
        changelog_dir = os.path.join(book_dir, "changelog")
        os.makedirs(changelog_dir, exist_ok=True)

        # Base detail context
        prod_path = f"/books/{book['id']}/"
        prod_ctx = get_base_context(
            title=f"{book['title']} — {book['subtitle']}",
            description=book["description"][:155],
            canonical_path=prod_path,
            og_type="book"
        )
        prod_ctx["og_image"] = f"https://versatilesparks.qzz.io/assets/covers/{book['id']}-cover.png"

        # Schemas: Book, Product, Breadcrumb, FAQPage
        prod_schemas = [
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://versatilesparks.qzz.io"},
                    {"@type": "ListItem", "position": 2, "name": book["title"], "item": f"https://versatilesparks.qzz.io{prod_path}"}
                ]
            },
            {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": book["title"],
                "description": book["description"],
                "image": prod_ctx["og_image"],
                "offers": {
                    "@type": "Offer",
                    "price": book["price_usd"],
                    "priceCurrency": "USD",
                    "url": book["gumroad_url"],
                    "availability": "https://schema.org/InStock"
                }
            },
            {
                "@context": "https://schema.org",
                "@type": "Book",
                "name": book["title"],
                "alternativeHeadline": book["subtitle"],
                "author": {"@type": "Person", "name": book["author"]},
                "bookFormat": "https://schema.org/EBook",
                "numberOfPages": 392 if book["id"] == "browser-automation-playbook" else 66,
                "publisher": {"@type": "Organization", "name": "Versatile Sparks"}
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}}
                    for faq in book["faqs"]
                ]
            }
        ]
        prod_ctx["json_ld_schemas"] = "\n".join([f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in prod_schemas])

        # Detail HTML
        prod_body = Template(product_tmpl).render(book=book)
        prod_html = Template(layout_tmpl).render(**prod_ctx, content=prod_body)
        write_file(os.path.join(book_dir, "index.html"), prod_html)

        # Changelog HTML
        changelog_path = f"/books/{book['id']}/changelog/"
        changelog_ctx = get_base_context(
            title=f"Release Changelog — {book['title']}",
            description=f"Changelog and release history for {book['title']}.",
            canonical_path=changelog_path
        )
        changelog_body = Template(changelog_tmpl).render(book=book)
        changelog_html = Template(layout_tmpl).render(**changelog_ctx, content=changelog_body)
        write_file(os.path.join(changelog_dir, "index.html"), changelog_html)


    # === 3. Render Errata Page ===
    errata_ctx = get_base_context(
        title="Errata & Corrections — Versatile Sparks",
        description="Verify known corrections or report technical errors for the Python Browser Automation Cookbook and Browser Automation Playbook.",
        canonical_path="/errata.html"
    )
    errata_body = Template(errata_tmpl).render(books=books)
    errata_html = Template(layout_tmpl).render(**errata_ctx, content=errata_body)
    write_file(os.path.join(WEBSITE, "errata.html"), errata_html)


    # === 4. Render Simple Content Pages ===
    simple_pages = [
        {
            "filename": "about.html",
            "title": "About & Publishing Philosophy",
            "desc": "About the author Yasaka Hanini and the Versatile Sparks publishing philosophy.",
            "body": """
                <p>Versatile Sparks publishes practical, hyper-focused engineering references for people who build products.</p>
                <h3>The Code-First Philosophy</h3>
                <p>Every book is compiled directly from production pipelines. We do not write abstract theory or speculative tutorials. If a code block appears in our books, it has run successfully inside orchestrated containers and is fully tested.</p>
                <h3>Our Setup</h3>
                <p>To support independent engineering and direct direct-to-reader publishing, we bundle the raw Python codebases, compose environments, and reflowable formats directly in the downloads. Downloads and fulfillment are hosted via Gumroad.</p>
                <p>If you have questions, feedback, or would like to submit errata, contact the author directly at <a href="mailto:yasaka.hanini@protonmail.com">yasaka.hanini@protonmail.com</a>.</p>
            """
        },
        {
            "filename": "privacy.html",
            "title": "Privacy Policy",
            "desc": "Privacy policy for Versatile Sparks direct publications.",
            "body": """
                <p><em>Last updated: July 2026</em></p>
                <h3>Information Collection</h3>
                <p>We value developer privacy. We collect only the information you voluntarily provide during purchase (such as your email address to deliver file updates). Payment details are securely processed by Gumroad and Stripe; we never store or see your financial information.</p>
                <h3>Analytics</h3>
                <p>We use Cloudflare Web Analytics, a cookie-less, privacy-respecting service that does not track your identity across the web or collect personal metrics.</p>
            """
        },
        {
            "filename": "terms.html",
            "title": "Terms & Conditions",
            "desc": "Terms & Conditions of sale for Versatile Sparks engineering books.",
            "body": """
                <p><em>Last updated: July 2026</em></p>
                <h3>License Agreement</h3>
                <p>Purchasing any guidebook or codebase template grants you a personal, non-transferable license to read and run the code for educational and product development workflows. You may not distribute, resell, or publicly host the books or complete ZIP bundles without written permission.</p>
                <h3>Refunds</h3>
                <p>Due to the direct nature of digital goods, sales are final. However, if you experience a technical blocker with our codebase or formats, contact <a href="mailto:yasaka.hanini@protonmail.com">yasaka.hanini@protonmail.com</a> within 14 days for assistance or refund evaluation.</p>
            """
        }
    ]

    for sp in simple_pages:
        sp_ctx = get_base_context(
            title=f"{sp['title']} — Versatile Sparks",
            description=sp["desc"],
            canonical_path=f"/{sp['filename']}"
        )
        sp_body = Template(simple_tmpl).render(page_title=sp["title"], content_body=sp["body"])
        sp_html = Template(layout_tmpl).render(**sp_ctx, content=sp_body)
        write_file(os.path.join(WEBSITE, sp["filename"]), sp_html)


    # === 5. Render Robots & Sitemap ===
    robots_txt = "User-agent: *\nAllow: /\nSitemap: https://versatilesparks.qzz.io/sitemap.xml\n"
    write_file(os.path.join(WEBSITE, "robots.txt"), robots_txt)

    sitemap_urls = [
        "https://versatilesparks.qzz.io/",
        "https://versatilesparks.qzz.io/about.html",
        "https://versatilesparks.qzz.io/errata.html",
        "https://versatilesparks.qzz.io/privacy.html",
        "https://versatilesparks.qzz.io/terms.html",
        "https://versatilesparks.qzz.io/books/python-browser-automation-cookbook/",
        "https://versatilesparks.qzz.io/books/python-browser-automation-cookbook/changelog/",
        "https://versatilesparks.qzz.io/books/browser-automation-playbook/",
        "https://versatilesparks.qzz.io/books/browser-automation-playbook/changelog/"
    ]
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_xml += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n'
    sitemap_xml += '</urlset>\n'
    write_file(os.path.join(WEBSITE, "sitemap.xml"), sitemap_xml)

    # === 6. Write manifest.json ===
    manifest_data = {
        "name": "Versatile Sparks",
        "short_name": "Versatile Sparks",
        "description": "Production engineering handbooks.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0b0f19",
        "theme_color": "#38bdf8",
        "icons": [
            {
                "src": "/favicon.svg",
                "sizes": "any",
                "type": "image/svg+xml"
            }
        ]
    }
    write_file(os.path.join(WEBSITE, "manifest.json"), json.dumps(manifest_data, indent=2))

    # === 7. Write favicon.svg ===
    favicon_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#38bdf8"/></svg>'
    write_file(os.path.join(WEBSITE, "favicon.svg"), favicon_svg)

    # === 8. Write 404.html ===
    err404_ctx = get_base_context(
        title="Page Not Found (404) — Versatile Sparks",
        description="The requested page does not exist.",
        canonical_path="/404.html"
    )
    err404_body = Template(simple_tmpl).render(
        page_title="404 — Page Not Found",
        content_body="<p>The page you are looking for has been moved, deleted, or does not exist.</p><p><a href='/'>Return to Home Page &rarr;</a></p>"
    )
    err404_html = Template(layout_tmpl).render(**err404_ctx, content=err404_body)
    write_file(os.path.join(WEBSITE, "404.html"), err404_html)

if __name__ == "__main__":
    main()
