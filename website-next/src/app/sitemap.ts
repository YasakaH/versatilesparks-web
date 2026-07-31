import type { MetadataRoute } from "next";
import db from "../db/knowledge-base.json";

const SITE_URL = "https://versatilesparks.qzz.io";

// Required for `output: export` static builds.
export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
    const now = new Date();

    const conceptEntries = db.concepts.map((c) => ({
        url: `${SITE_URL}/concepts/${c.slug || c.id}`,
        lastModified: c.last_reviewed ? new Date(c.last_reviewed) : now,
        changeFrequency: "monthly" as const,
        priority: 0.8,
    }));

    const recipeEntries = db.recipes.map((r) => ({
        url: `${SITE_URL}/recipes/${r.slug}`,
        lastModified: now,
        changeFrequency: "monthly" as const,
        priority: 0.6,
    }));

    const bookEntries = db.books.map((b) => ({
        url: `${SITE_URL}/books/${b.id}`,
        lastModified: now,
        changeFrequency: "monthly" as const,
        priority: 0.7,
    }));

    return [
        { url: SITE_URL, lastModified: now, changeFrequency: "weekly", priority: 1.0 },
        ...bookEntries,
        ...conceptEntries,
        ...recipeEntries,
        // Static legal / info pages (managed by scripts/generate_legal_pages.py)
        { url: `${SITE_URL}/about`, lastModified: now, changeFrequency: "yearly", priority: 0.5 },
        { url: `${SITE_URL}/privacy`, lastModified: now, changeFrequency: "yearly", priority: 0.3 },
        { url: `${SITE_URL}/terms`, lastModified: now, changeFrequency: "yearly", priority: 0.3 },
        { url: `${SITE_URL}/errata`, lastModified: now, changeFrequency: "monthly", priority: 0.4 },
        { url: `${SITE_URL}/callback`, lastModified: now, changeFrequency: "yearly", priority: 0.3 },
    ];
}