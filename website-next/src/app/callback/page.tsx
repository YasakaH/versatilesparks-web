import LegalLayout, { legalMetadata } from "../../components/LegalLayout";

export const dynamic = "force-static";

export const metadata = legalMetadata(
    "Access Your Library",
    "Download your books and source code, or recover a lost purchase link from Gumroad.",
    "/callback"
);

export default function Page() {
    return (
        <LegalLayout title="Access Your Library" description="Download your books and source code, or recover a lost purchase link from Gumroad.">
            <h2 className="text-lg font-bold text-[#f5f2eb] font-mono">Download your books</h2>
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
        </LegalLayout>
    );
}