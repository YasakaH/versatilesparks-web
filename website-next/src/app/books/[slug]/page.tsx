import type { Metadata } from "next";
import { notFound } from "next/navigation";
import db from "../../../db/knowledge-base.json";
import type { Book } from "../../../types/knowledge";
import BookPageClient from "../../../components/BookPageClient";

const SITE_URL = "https://versatilesparks.qzz.io";

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
    return db.books.map((b) => ({ slug: b.id }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const { slug } = await params;
    const book = db.books.find((b) => b.id === slug) as Book | undefined;
    if (!book) return { title: "Book Not Found" };

    const url = `${SITE_URL}/books/${slug}`;
    const recipeCount = db.recipes.filter((r) => r.book === slug).length;
    const title = `${book.title} — Book`;
    const description = book.summary || `${book.title} — ${recipeCount} recipes in the browser engineering library.`;

    return {
        title,
        description,
        alternates: { canonical: url },
        openGraph: {
            type: "book",
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
        other: {
            "article:section": "Books",
        },
    };
}

export default async function Page({ params }: PageProps) {
    const { slug } = await params;
    const book = db.books.find((b) => b.id === slug) as Book | undefined;
    if (!book) notFound();

    const recipes = db.recipes.filter((r) => r.book === slug);
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Book",
        name: book.title,
        description: book.summary,
        url: `${SITE_URL}/books/${slug}`,
        author: { "@type": "Organization", name: "Versatile Sparks" },
        publisher: { "@type": "Organization", name: "Versatile Sparks" },
        hasPart: recipes.map((r) => ({
            "@type": "TechArticle",
            name: r.title,
            url: `${SITE_URL}/recipes/${r.slug}`,
        })),
        keywords: recipes.flatMap((r) => r.concepts || []).join(", "),
    };

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />
            <BookPageClient bookId={book.id} />
        </>
    );
}