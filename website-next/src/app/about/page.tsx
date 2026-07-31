import LegalLayout, { legalMetadata } from "../../components/LegalLayout";

export const dynamic = "force-static";

export const metadata = legalMetadata(
    "About",
    "Versatile Sparks publishes practical engineering handbooks for browser automation, anti-detection, and reliable production scraping.",
    "/about"
);

export default function Page() {
    return (
        <LegalLayout title="About" description="Versatile Sparks publishes practical engineering handbooks for browser automation, anti-detection, and reliable production scraping.">
            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Mission</h2>
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
        </LegalLayout>
    );
}
