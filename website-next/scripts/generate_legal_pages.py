#!/usr/bin/env python3
"""One-shot generator for static legal/info pages.
Writes .tsx files directly with Python file I/O so the editor's JSX
formatter never touches the generated source.
"""
import os

ROOT = os.path.join(
    "c:/Users/varas/personalities/cookbook/website-next/src/app"
)


def write_file(rel, content):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"wrote {rel} ({len(content)} bytes)")


def header(title, desc, slug):
    return (
        'import LegalLayout, { legalMetadata } from "../../components/LegalLayout";\n\n'
        'export const dynamic = "force-static";\n\n'
        "export const metadata = legalMetadata(\n"
        f'    "{title}",\n'
        f'    "{desc}",\n'
        f'    "/{slug}"\n'
        ");\n\n"
        "export default function Page() {\n"
        "    return (\n"
        f'        <LegalLayout title="{title}" description="{desc}">\n'
    )


FOOTER = "        </LegalLayout>\n    );\n}\n"

ABOUT_BODY = """            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Mission</h2>
            <p>
                Most browser-automation material stops at the basics. We document
                the part that comes after - running automation in production
                against sites that actively resist bots, keeping it observable,
                and recovering it when it breaks. The goal is durable
                infrastructure you can operate, not scripts that work once on a
                tutorial site.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">The Library</h2>
            <p>The site is an interactive index over two handbooks:</p>
            <ul>
                <li>
                    <strong>Python Browser Automation Cookbook</strong> - $29 USD.
                    Recipe-style solutions for selectors, waits, downloads, login
                    flows, and pagination.
                </li>
                <li>
                    <strong>Browser Automation Playbook</strong> - $59 USD. The
                    production handbook: anti-detection, TLS/JA3 fingerprinting,
                    proxy pools, CDP interception, self-healing daemons, and
                    observability.
                </li>
            </ul>
            <p>
                Both books ship as DRM-free PDF + EPUB + source code and include
                free rolling updates as new material is added.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Why this site is a graph</h2>
            <p>
                The knowledge system is a dependency map: each concept (sessions,
                cookies, proxies, CDP, fingerprints...) links to the concepts it
                requires and the recipes that exercise it. It is the index the
                books never had room to print.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Contact</h2>
            <p>
                Errors and corrections go to{" "}
                <a href="mailto:yasaka.hanini@protonmail.com" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]">
                    yasaka.hanini@protonmail.com
                </a>
                . Reported errata are tracked on the{" "}
                <a href="/errata" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]">Errata</a>{" "}
                page.
            </p>
"""

PRIVACY_BODY = """            <p><strong>Last updated:</strong> July 2026.</p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">What we collect</h2>
            <p>
                The website itself is a static export. It does not run a backend,
                does not set tracking cookies, and does not embed third-party
                analytics. We do not collect personal data from visitors browsing
                the knowledge system.
            </p>
            <p>
                Bookmarks and recently-viewed entries are stored in your
                browser's <code>localStorage</code>. They never leave your
                device and are cleared if you clear site data.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Payment processor</h2>
            <p>
                Purchases are handled by{" "}
                <a href="https://gumroad.com" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">Gumroad</a>
                . Gumroad processes your payment and stores your email and purchase
                record. We receive your email and the product you purchased so we can
                deliver updates. Gumroad's privacy policy governs payment data;
                see{" "}
                <a href="https://gumroad.com/policies/privacy" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">gumroad.com/policies/privacy</a>.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Email</h2>
            <p>
                If you email us at{" "}
                <a href="mailto:yasaka.hanini@protonmail.com" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]">yasaka.hanini@protonmail.com</a>
                , we keep that correspondence to resolve your request and, where
                relevant, to notify you of errata or updates to a product you
                purchased. We do not sell or share your email.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Hosting</h2>
            <p>
                The static site is served from Cloudflare. Cloudflare may log edge
                requests as part of its normal operation; see the{" "}
                <a href="https://www.cloudflare.com/privacypolicy/" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">Cloudflare privacy policy</a>.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Your choices</h2>
            <p>
                You can clear all locally-stored data (bookmarks, recent items) from
                your browser settings at any time. You may email us to request
                deletion of any correspondence record we hold.
            </p>
"""

TERMS_BODY = """            <p><strong>Last updated:</strong> July 2026.</p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">The books</h2>
            <p>
                Each book is sold as a DRM-free digital download (PDF + EPUB + source
                code). Your purchase grants you a personal, non-transferable license
                to read the book and to use the included source code in your own
                projects, including commercial projects.
            </p>
            <p>You may not:</p>
            <ul>
                <li>Redistribute the book files or source code publicly.</li>
                <li>Resell, relicense, or bundle the book into a product you sell.</li>
                <li>Remove authorship or license notices from the source code.</li>
            </ul>
            <p>
                Quoting short excerpts for review, teaching, or criticism is fine.
                If unsure, email{" "}
                <a href="mailto:yasaka.hanini@protonmail.com" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]">yasaka.hanini@protonmail.com</a>.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Updates</h2>
            <p>
                Books receive free rolling updates. When a new edition or revision
                is released, purchasers receive the updated files through Gumroad at
                no additional cost. The version you purchased remains licensed to
                you even if you do not update.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Refunds</h2>
            <p>
                If a book does not work for you, email us within 14 days of purchase
                for a full refund. We may ask what did not fit so we can improve it,
                but we will not withhold a refund.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">The website</h2>
            <p>
                The interactive knowledge system on versatilesparks.qzz.io is provided
                as a free reference. It is licensed under{" "}
                <a href="https://creativecommons.org/licenses/by-nc/4.0/" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">CC BY-NC 4.0</a>
                : you may share and adapt the concept and recipe text for
                non-commercial use with attribution. The source code shown inside
                recipes remains governed by the book license above.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">No warranty</h2>
            <p>
                The books and website are engineering documentation, not legal or
                security advice. Browser automation against third-party sites may be
                governed by those sites' terms of service and by applicable
                law (e.g. CFAA, GDPR). You are responsible for how you use the
                techniques described. The material is provided "as is"
                without warranty of any kind.
            </p>
"""

ERRATA_BODY = """            <p>
                This page tracks known errors in the published books. Each report
                is acknowledged by email and listed here once confirmed.
            </p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Browser Automation Playbook v2.0.0</h2>
            <p>No known issues.</p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Python Browser Automation Cookbook v1.0.0</h2>
            <p>No known issues.</p>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Reporting an error</h2>
            <p>
                Email{" "}
                <a href="mailto:yasaka.hanini@protonmail.com" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]">yasaka.hanini@protonmail.com</a>{" "}
                with the book, chapter, and a short description. If you can, include
                the exact wording and the correction you would expect. Confirmed
                errata appear on this page and are fixed in the next rolling update.
            </p>
"""

CALLBACK_BODY = """            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Download your books</h2>
            <p>
                Purchases are delivered by Gumroad. To download your files or
                recover a lost link:
            </p>
            <ol>
                <li>
                    Go to{" "}
                    <a href="https://gumroad.com/library" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">gumroad.com/library</a>{" "}
                    and sign in with the email you used at purchase.
                </li>
                <li>Open the product to re-download the latest PDF, EPUB, and source.</li>
                <li>
                    If you no longer have the email, use{" "}
                    <a href="https://gumroad.com/recover" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">gumroad.com/recover</a>{" "}
                    to resend your library link.
                </li>
            </ol>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Direct product pages</h2>
            <ul>
                <li>
                    <a href="https://gum.co/python-browser-automation-cookbook" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">
                        Python Browser Automation Cookbook - $29
                    </a>
                </li>
                <li>
                    <a href="https://gum.co/browser-automation-playbook" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]" target="_blank" rel="noopener noreferrer">
                        Browser Automation Playbook - $59
                    </a>
                </li>
            </ul>

            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Need help?</h2>
            <p>
                If Gumroad's self-serve recovery does not work, email{" "}
                <a href="mailto:yasaka.hanini@protonmail.com" className="text-[#f5f2eb] underline hover:text-[#f2f2f2]">yasaka.hanini@protonmail.com</a>{" "}
                with the email you used at purchase and we will resend your access
                link manually.
            </p>
"""


write_file(
    "about/page.tsx",
    header(
        "About",
        "Versatile Sparks publishes practical engineering handbooks for browser automation, anti-detection, and reliable production scraping.",
        "about",
    )
    + ABOUT_BODY
    + FOOTER,
)

write_file(
    "privacy/page.tsx",
    header(
        "Privacy Policy",
        "How Versatile Sparks handles data: local-only bookmarks, no tracking cookies, no personal data sold or shared.",
        "privacy",
    )
    + PRIVACY_BODY
    + FOOTER,
)

write_file(
    "terms/page.tsx",
    header(
        "Terms of Use",
        "License and usage terms for Versatile Sparks books and the interactive knowledge system.",
        "terms",
    )
    + TERMS_BODY
    + FOOTER,
)

write_file(
    "errata/page.tsx",
    header(
        "Errata",
        "Known corrections for the Browser Automation Playbook and Python Browser Automation Cookbook. Report new errors to yasaka.hanini@protonmail.com.",
        "errata",
    )
    + ERRATA_BODY
    + FOOTER,
)

write_file(
    "callback/page.tsx",
    header(
        "Access Your Library",
        "Download your books and source code, or recover a lost purchase link from Gumroad.",
        "callback",
    )
    + CALLBACK_BODY
    + FOOTER,
)

print("done")