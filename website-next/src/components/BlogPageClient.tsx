"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, BookOpen } from "lucide-react";
import ConsoleShell from "./ConsoleShell";
import ContentBody from "./ContentBody";

interface Article {
    id: string;
    slug: string;
    title: string;
    description: string;
    date: string;
    tags: string[];
    concepts: string[];
    body?: string;
}

interface Concept {
    id: string;
    title: string;
    slug: string;
}

interface BlogPageClientProps {
    article: Article;
    concepts: Concept[];
}

export default function BlogPageClient({ article, concepts }: BlogPageClientProps) {
    const router = useRouter();
    const [bookmarks, setBookmarks] = useState<string[]>([]);

    useEffect(() => {
        const saved = localStorage.getItem("vs-bookmarks");
        if (saved) setBookmarks(JSON.parse(saved));
    }, []);

    const dateStr = article.date
        ? new Date(article.date + "T00:00:00Z").toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
          })
        : "";

    return (
        <ConsoleShell
            activeConceptId={null}
            breadcrumb={["Blog", article.title]}
            onSelectConcept={(id: string) => router.push(`/concepts/${id}`)}
        >
            <div className="flex flex-col gap-6 animate-fade-in flex-1 max-w-3xl mx-auto">
                <div className="border-b border-[#242424] pb-4">
                    <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Article</span>
                    <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">
                        {article.title}
                    </h1>
                    {dateStr && (
                        <p className="text-sm text-[#8a8a8a] mt-2 font-mono">{dateStr}</p>
                    )}
                </div>

                <div className="flex flex-wrap gap-2">
                    {(article.tags || []).map((tag: string) => (
                        <span
                            key={tag}
                            className="px-2.5 py-0.5 rounded text-[10px] font-mono border border-[#242424] bg-[#161616] text-[#8a8a8a]"
                        >
                            {tag}
                        </span>
                    ))}
                </div>

                {concepts.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                        {concepts.map((c) => (
                            <button
                                key={c.id}
                                onClick={() => router.push(`/concepts/${c.slug}`)}
                                className="px-2.5 py-0.5 rounded text-[10px] font-mono border border-[#242424] bg-[#161616] text-[#8a8a8a] hover:border-[#8a8a8a] transition-all flex items-center gap-1"
                            >
                                <BookOpen className="w-3 h-3" />
                                {c.title}
                                <ArrowRight className="w-3 h-3" />
                            </button>
                        ))}
                    </div>
                )}

                <p className="text-base text-[#f2f2f2] leading-relaxed font-sans font-light italic border-l-2 border-[#242424] pl-4">
                    {article.description}
                </p>

                <div className="max-w-none">
                    {article.body ? (
                        <ContentBody body={article.body} />
                    ) : (
                        <p className="text-[#8a8a8a]">Content not available.</p>
                    )}
                </div>
            </div>
        </ConsoleShell>
    );
}
