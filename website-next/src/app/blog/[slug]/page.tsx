import type { Metadata } from "next";
import { notFound } from "next/navigation";
import db from "../../../db/knowledge-base.json";
import BlogPageClient from "../../../components/BlogPageClient";

const SITE_URL = "https://versatilesparks.qzz.io";

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
    return db.articles.map((a) => ({ slug: a.slug || a.id }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const { slug } = await params;
    const article = db.articles.find((a) => (a.slug || a.id) === slug);
    if (!article) return { title: "Article Not Found" };

    const url = `${SITE_URL}/blog/${slug}`;
    const title = `${article.title} — Browser Automation Guide`;
    const description = article.description;

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
            card: "summary_large_image",
            title,
            description,
        },
    };
}

export default async function Page({ params }: PageProps) {
    const { slug } = await params;
    const article = db.articles.find((a) => (a.slug || a.id) === slug);
    if (!article) notFound();

    const allConcepts: any[] = db.concepts;
    const concepts = (article.concepts || [])
        .map((id: string) => allConcepts.find((c: any) => c.id === id))
        .filter(Boolean);

    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Article",
        headline: article.title,
        description: article.description,
        url: `${SITE_URL}/blog/${slug}`,
        datePublished: article.date,
        author: { "@type": "Organization", name: "Versatile Sparks" },
        publisher: { "@type": "Organization", name: "Versatile Sparks" },
        keywords: (article.tags || []).join(", "),
    };

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />
            <BlogPageClient article={article} concepts={concepts} />
        </>
    );
}
