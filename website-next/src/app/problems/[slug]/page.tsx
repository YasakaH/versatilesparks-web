import type { Metadata } from "next";
import { notFound } from "next/navigation";
import db from "../../../db/knowledge-base.json";
import ProblemPageClient from "../../../components/ProblemPageClient";

const SITE_URL = "https://versatilesparks.qzz.io";

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
    return db.problems.map((p) => ({ slug: p.slug || p.id }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const { slug } = await params;
    const problem = db.problems.find((p) => (p.slug || p.id) === slug);
    if (!problem) return { title: "Error Not Found" };

    const url = `${SITE_URL}/problems/${slug}`;
    const title = `${problem.title} — Browser Automation Error`;
    const description = problem.description;

    return {
        title,
        description,
        alternates: { canonical: url },
        openGraph: {
            type: "article",
            url,
            title,
            description,
            siteName: "Versatile Sparks",
        },
        twitter: {
            card: "summary",
            title,
            description,
        },
    };
}

export default async function Page({ params }: PageProps) {
    const { slug } = await params;
    const problem = db.problems.find((p) => (p.slug || p.id) === slug);
    if (!problem) notFound();

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        headline: problem.title,
        description: problem.description,
        url: `${SITE_URL}/problems/${slug}`,
        author: { "@type": "Organization", name: "Versatile Sparks" },
        publisher: { "@type": "Organization", name: "Versatile Sparks" },
        keywords: (problem.error_patterns || []).join(", "),
    };

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />
            <ProblemPageClient problemId={problem.id} />
        </>
    );
}
