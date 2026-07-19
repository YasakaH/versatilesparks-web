import type { Metadata } from "next";
import { notFound } from "next/navigation";
import db from "../../../db/knowledge-base.json";
import ConceptPageClient from "../../../components/ConceptPageClient";

const SITE_URL = "https://versatilesparks.com";

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
    return db.concepts.map((c) => ({ slug: c.slug || c.id }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const { slug } = await params;
    const concept = db.concepts.find((c) => (c.slug || c.id) === slug);
    if (!concept) return { title: "Concept Not Found" };

    const url = `${SITE_URL}/concepts/${slug}`;
    const title = `${concept.title} — Browser Engineering Concept`;
    const description = concept.summary;

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
            publishedTime: concept.last_reviewed,
        },
        twitter: {
            card: "summary",
            title,
            description,
        },
        other: {
            "article:section": "Concepts",
            "article:tag": concept.related?.join(", ") || concept.id,
        },
    };
}

export default async function Page({ params }: PageProps) {
    const { slug } = await params;
    const concept = db.concepts.find((c) => (c.slug || c.id) === slug);
    if (!concept) notFound();

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        headline: concept.title,
        description: concept.summary,
        url: `${SITE_URL}/concepts/${slug}`,
        dateModified: concept.last_reviewed,
        author: { "@type": "Organization", name: "Versatile Sparks" },
        publisher: { "@type": "Organization", name: "Versatile Sparks" },
        about: (concept.related || []).map((id: string) => {
            const r = db.concepts.find((c) => c.id === id);
            return r ? { "@type": "TechArticle", name: r.title } : null;
        }).filter(Boolean),
        keywords: [concept.id, ...(concept.related || [])].join(", "),
    };

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />
            <ConceptPageClient conceptId={concept.id} />
        </>
    );
}