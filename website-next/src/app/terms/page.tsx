import LegalLayout, { legalMetadata } from "../../components/LegalLayout";

export const dynamic = "force-static";

export const metadata = legalMetadata(
    "Terms of Use",
    "License and usage terms for Versatile Sparks books and the interactive knowledge system.",
    "/terms"
);

export default function Page() {
    return (
        <LegalLayout title="Terms of Use" description="License and usage terms for Versatile Sparks books and the interactive knowledge system.">
            <p><strong>Last updated:</strong> July 2026.</p>

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
        </LegalLayout>
    );
}
