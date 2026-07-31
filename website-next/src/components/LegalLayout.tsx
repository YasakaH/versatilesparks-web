import React from "react";
import Link from "next/link";
import type { Metadata } from "next";

export const SITE_URL = "https://versatilesparks.qzz.io";

interface LegalLayoutProps {
    title: string;
    eyebrow?: string;
    description?: string;
    children: React.ReactNode;
}

/**
 * Shared layout for the static "info" / legal routes — /about, /privacy,
 * /terms, /errata, /callback. Keeps the dark-console aesthetic of the rest
 * of the site while remaining fully static-export compatible and indexable.
 */
export default function LegalLayout({
    title,
    eyebrow = "Versatile Sparks",
    description,
    children,
}: LegalLayoutProps) {
    return (
        <div className="min-h-screen flex flex-col bg-[#090909] text-[#f2f2f2] font-sans">
            <header className="border-b border-[#242424] bg-[#0c0c0c] px-6 py-4 flex items-center justify-between select-none">
                <Link
                    href="/"
                    className="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-[#f2f2f2] hover:text-[#f5f2eb]"
                >
                    <span className="w-2.5 h-2.5 rounded-full bg-[#f5f2eb]" />
                    Browser Infrastructure Browser
                </Link>
                <nav className="flex items-center gap-4 text-[11px] font-mono text-[#8a8a8a]">
                    <Link href="/about" className="hover:text-[#f2f2f2]">About</Link>
                    <Link href="/errata" className="hover:text-[#f2f2f2]">Errata</Link>
                    <Link href="/privacy" className="hover:text-[#f2f2f2]">Privacy</Link>
                    <Link href="/terms" className="hover:text-[#f2f2f2]">Terms</Link>
                    <Link
                        href="https://gum.co/python-browser-automation-cookbook"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:text-[#f2f2f2]"
                    >
                        Library ↗
                    </Link>
                </nav>
            </header>

            <main className="flex-1 max-w-3xl w-full mx-auto px-6 py-12 md:py-16">
                <span className="text-[10px] font-mono uppercase text-[#8a8a8a] tracking-widest">
                    {eyebrow}
                </span>
                <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-2 text-[#f5f2eb]">
                    {title}
                </h1>
                {description && (
                    <p className="text-md text-[#8a8a8a] mt-3 leading-relaxed font-light">
                        {description}
                    </p>
                )}
                <div className="prose prose-invert max-w-none mt-8 text-sm md:text-md leading-relaxed text-[#cfcfcf] space-y-4">
                    {children}
                </div>
            </main>

            <footer className="border-t border-[#242424] bg-[#0c0c0c] px-6 py-4 flex flex-wrap items-center justify-between gap-3 text-[11px] text-[#8a8a8a] font-mono select-none">
                <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-[#f5f2eb]" />
                        Versatile Sparks
                    </span>
                    <span>•</span>
                    <span>v2.0.0</span>
                </div>
                <div className="flex items-center gap-4">
                    <Link href="/about" className="hover:text-[#f2f2f2]">About</Link>
                    <Link href="/errata" className="hover:text-[#f2f2f2]">Errata</Link>
                    <Link href="/privacy" className="hover:text-[#f2f2f2]">Privacy</Link>
                    <Link href="/terms" className="hover:text-[#f2f2f2]">Terms</Link>
                    <Link href="/callback" className="hover:text-[#f2f2f2]">Access</Link>
                </div>
            </footer>
        </div>
    );
}

/** Helper to build consistent metadata for a legal page. */
export function legalMetadata(
    title: string,
    description: string,
    path: string
): Metadata {
    return {
        title,
        description,
        alternates: { canonical: `${SITE_URL}${path}` },
        openGraph: {
            title: `${title} — Versatile Sparks`,
            description,
            url: `${SITE_URL}${path}`,
            type: "article",
            siteName: "Versatile Sparks",
        },
        robots: { index: true, follow: true },
    };
}