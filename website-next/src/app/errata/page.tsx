import LegalLayout, { legalMetadata } from "../../components/LegalLayout";

export const dynamic = "force-static";

export const metadata = legalMetadata(
    "Errata",
    "Known corrections for the Browser Automation Playbook and Python Browser Automation Cookbook. Report new errors to yasaka.hanini@protonmail.com.",
    "/errata"
);

export default function Page() {
    return (
        <LegalLayout title="Errata" description="Known corrections for the Browser Automation Playbook and Python Browser Automation Cookbook. Report new errors to yasaka.hanini@protonmail.com.">
            <p>
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
        </LegalLayout>
    );
}
