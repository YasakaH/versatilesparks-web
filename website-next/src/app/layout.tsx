import type { Metadata } from "next";
import "./globals.css";

const SITE_URL = "https://versatilesparks.com";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Browser Engineering Knowledge System — Versatile Sparks",
    template: "%s — Versatile Sparks",
  },
  description:
    "An interactive database and dependency map for production-grade browser automation, anti-detection, and session recovery.",
  applicationName: "Versatile Sparks",
  authors: [{ name: "Versatile Sparks", url: SITE_URL }],
  creator: "Versatile Sparks",
  publisher: "Versatile Sparks",
  keywords: [
    "browser automation",
    "anti-detection",
    "session recovery",
    "Playwright",
    "Selenium",
    "CDP",
    "fingerprints",
    "proxies",
    "observability",
  ],
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url: SITE_URL,
    siteName: "Versatile Sparks",
    title: "Browser Engineering Knowledge System — Versatile Sparks",
    description:
      "An interactive database and dependency map for production-grade browser automation, anti-detection, and session recovery.",
    locale: "en_US",
  },
  twitter: {
    card: "summary",
    title: "Browser Engineering Knowledge System — Versatile Sparks",
    description:
      "An interactive database and dependency map for production-grade browser automation, anti-detection, and session recovery.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-snippet": -1, "max-image-preview": "large" },
  },
};

const orgJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Versatile Sparks",
  url: SITE_URL,
  description:
    "Publisher of browser engineering knowledge — cookbooks, playbooks, and an interactive knowledge system covering automation, anti-detection, and reliability.",
  knowsAbout: [
    "Browser automation",
    "Anti-detection",
    "Session recovery",
    "Observability",
    "Playwright",
    "Selenium",
    "CDP",
    "Fingerprints",
    "Proxies",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased dark">
      <body className="min-h-full flex flex-col bg-[#090909] text-[#f2f2f2]">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
        />
        {children}
      </body>
    </html>
  );
}