import type { Metadata } from "next";
import { notFound } from "next/navigation";
import db from "../../../db/knowledge-base.json";
import RecipePageClient from "../../../components/RecipePageClient";

const SITE_URL = "https://versatilesparks.com";

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
    return db.recipes.map((r) => ({ slug: r.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const { slug } = await params;
    const recipe = db.recipes.find((r) => r.slug === slug) as any;
    if (!recipe) return { title: "Recipe Not Found" };

    const url = `${SITE_URL}/recipes/${slug}`;
    const book = db.books.find((b) => b.id === recipe.book);
    const title = `${recipe.title} — Recipe`;
    const description = recipe.summary || `Recipe from ${book?.title || "the browser engineering library"}.`;

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
        other: {
            "article:section": book?.title || "Recipes",
            "article:tag": recipe.concepts?.join(", ") || recipe.id,
        },
    };
}

export default async function Page({ params }: PageProps) {
    const { slug } = await params;
    const recipe = db.recipes.find((r) => r.slug === slug) as any;
    if (!recipe) notFound();

    const book = db.books.find((b) => b.id === recipe.book);
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        headline: recipe.title,
        description: recipe.summary || `Recipe from ${book?.title || "the library"}.`,
        url: `${SITE_URL}/recipes/${slug}`,
        author: { "@type": "Organization", name: "Versatile Sparks" },
        publisher: { "@type": "Organization", name: "Versatile Sparks" },
        isPartOf: book ? { "@type": "Book", name: book.title } : undefined,
        about: (recipe.concepts || []).map((id: string) => {
            const c = db.concepts.find((x) => x.id === id);
            return c ? { "@type": "TechArticle", name: c.title } : null;
        }).filter(Boolean),
        keywords: [recipe.id, ...(recipe.concepts || [])].join(", "),
    };

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />
            <RecipePageClient recipeId={recipe.id} />
        </>
    );
}