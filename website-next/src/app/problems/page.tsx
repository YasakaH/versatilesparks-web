import type { Metadata } from "next";
import db from "../../db/knowledge-base.json";
import ProblemIndexClient from "../../components/ProblemIndexClient";

export const metadata: Metadata = {
    title: "Browser Automation Error Reference — Versatile Sparks",
    description: "Browse common browser automation errors, their root causes, and production fixes. Search by error message, symptom, or concept.",
    alternates: { canonical: "https://versatilesparks.qzz.io/problems" },
    openGraph: {
        type: "website",
        url: "https://versatilesparks.qzz.io/problems",
        title: "Browser Automation Error Reference — Versatile Sparks",
        description: "Browse common browser automation errors, their root causes, and production fixes.",
    },
};

export default function Page() {
    const grouped: Record<string, typeof db.problems> = {};
    db.problems.forEach((p) => {
        const concept = (p.conceptObject?.title) || "Other";
        if (!grouped[concept]) grouped[concept] = [];
        grouped[concept].push(p);
    });

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{
                    __html: JSON.stringify({
                        "@context": "https://schema.org",
                        "@type": "CollectionPage",
                        name: "Browser Automation Error Reference",
                        description: "Common browser automation errors and their fixes.",
                    }),
                }}
            />
            <ProblemIndexClient problems={db.problems} grouped={grouped} />
        </>
    );
}
