import type { MetadataRoute } from "next";

const SITE_URL = "https://versatilesparks.com";

// Required for `output: export` static builds.
export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
    return {
        rules: [
            {
                userAgent: "*",
                allow: "/",
                disallow: ["/api/"],
            },
        ],
        sitemap: `${SITE_URL}/sitemap.xml`,
        host: SITE_URL,
    };
}