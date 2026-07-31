import LegalLayout, { legalMetadata } from "../../components/LegalLayout";

export const dynamic = "force-static";

export const metadata = legalMetadata(
    "Privacy Policy",
    "How Versatile Sparks handles data: local-only bookmarks, no tracking cookies, no personal data sold or shared.",
    "/privacy"
);

export default function Page() {
    return (
        <LegalLayout title="Privacy Policy" description="How Versatile Sparks handles data: local-only bookmarks, no tracking cookies, no personal data sold or shared.">
            <p><strong>Last updated:</strong> July 2026.</p>

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
        </LegalLayout>
    );
}
