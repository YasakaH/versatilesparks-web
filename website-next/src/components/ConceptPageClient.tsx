"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Bookmark } from "lucide-react";

import ConsoleShell from "./ConsoleShell";
import ContentBody from "./ContentBody";
import db from "../db/knowledge-base.json";

interface ConceptPageClientProps {
    conceptId: string;
}

export default function ConceptPageClient({ conceptId }: ConceptPageClientProps) {
    const router = useRouter();
    const [bookmarks, setBookmarks] = useState<string[]>([]);

    useEffect(() => {
        const savedBookmarks = localStorage.getItem("vs-bookmarks");
        if (savedBookmarks) setBookmarks(JSON.parse(savedBookmarks));
    }, []);

    const handleSelectConcept = (id: string) => {
        const conceptObj = db.concepts.find((c) => c.id === id);
        if (!conceptObj) return;
        router.push(`/concepts/${conceptObj.slug || id}`);
    };

    const toggleBookmark = (id: string) => {
        setBookmarks((prev) => {
            const updated = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
            localStorage.setItem("vs-bookmarks", JSON.stringify(updated));
            return updated;
        });
    };

    const currentConcept = db.concepts.find((c) => c.id === conceptId);
    if (!currentConcept) return null;

    const getBookCoverage = (cId: string) => {
        const matchingRecipes = db.recipes.filter((r) => r.concepts.includes(cId));
        const coverage: Record<string, string> = {
            cookbook: "No direct recipes",
            playbook: "No direct recipes",
        };
        let cookbookCount = 0;
        let playbookCount = 0;
        matchingRecipes.forEach((r) => {
            if (r.book === "cookbook") cookbookCount++;
            if (r.book === "playbook") playbookCount++;
        });
        if (cookbookCount > 0) coverage.cookbook = `${cookbookCount} Recipe${cookbookCount > 1 ? "s" : ""}`;
        if (playbookCount > 0) coverage.playbook = `${playbookCount} Recipe${playbookCount > 1 ? "s" : ""}`;
        return { coverage, cookbookCount, playbookCount };
    };

    return (
        <ConsoleShell
            activeConceptId={conceptId}
            breadcrumb={["Library", "Concepts", currentConcept.title]}
            onSelectConcept={handleSelectConcept}
        >
            <div className="flex flex-col gap-6 animate-fade-in flex-1">
                <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                    <div>
                        <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Concept Specification</span>
                        <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">{currentConcept.title}</h1>
                    </div>
                    <button onClick={() => toggleBookmark(currentConcept.id)} className="p-2 border border-[#242424] rounded hover:border-[#8a8a8a]" aria-label="Toggle bookmark">
                        <Bookmark className={`w-4 h-4 ${bookmarks.includes(currentConcept.id) ? "fill-[#f5f2eb] text-[#f5f2eb]" : "text-[#8a8a8a]"}`} />
                    </button>
                </div>

                <p className="text-lg text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">{currentConcept.summary}</p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-4">
                    <div className="p-4 border border-[#242424] rounded bg-[#111111]">
                        <h5 className="text-xs font-mono uppercase text-[#8a8a8a] mb-2 font-bold">Dependency Path</h5>
                        <div className="flex flex-col gap-2 text-xs font-mono">
                            <div>
                                <span className="text-[#8a8a8a]">Requires: </span>
                                {currentConcept.requires && currentConcept.requires.length > 0
                                    ? currentConcept.requires.map((x: string) => (
                                        <button key={x} onClick={() => handleSelectConcept(x)} className="text-[#f5f2eb] hover:underline mr-2">#{x}</button>
                                    ))
                                    : "None"}
                            </div>
                            <div>
                                <span className="text-[#8a8a8a]">Used By: </span>
                                {currentConcept.used_by && currentConcept.used_by.length > 0
                                    ? currentConcept.used_by.map((x: string) => (
                                        <button key={x} onClick={() => handleSelectConcept(x)} className="text-[#f5f2eb] hover:underline mr-2">#{x}</button>
                                    ))
                                    : "None"}
                            </div>
                        </div>
                    </div>

                    <div className="p-4 border border-[#242424] rounded bg-[#111111] flex flex-col gap-1 text-xs">
                        <h5 className="text-xs font-mono uppercase text-[#8a8a8a] mb-2 font-bold">Environment Target</h5>
                        <div><span className="text-[#8a8a8a]">Difficulty: </span>{currentConcept.difficulty}</div>
                        <div><span className="text-[#8a8a8a]">Compatibility: </span>{currentConcept.compatible_with}</div>
                        <div><span className="text-[#8a8a8a]">Last Reviewed: </span>{currentConcept.last_reviewed}</div>
                    </div>
                </div>

                <ContentBody body={currentConcept.body} />

                {currentConcept.related && currentConcept.related.length > 0 && (
                    <div className="border-t border-[#242424] pt-6 mt-2">
                        <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">Related Concepts</h4>
                        <div className="flex flex-wrap gap-2">
                            {currentConcept.related.map((relId: string) => {
                                const rel = db.concepts.find((c) => c.id === relId);
                                if (!rel) return null;
                                return (
                                    <button
                                        key={relId}
                                        onClick={() => handleSelectConcept(relId)}
                                        className="px-3 py-1.5 text-xs border border-[#242424] bg-[#161616] rounded hover:border-[#8a8a8a] text-[#f2f2f2] transition-all"
                                    >
                                        {rel.title}
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                )}

                {currentConcept.recipes && currentConcept.recipes.length > 0 && (
                    <div className="border-t border-[#242424] pt-6 mt-2">
                        <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">Recipes ({currentConcept.recipes.length})</h4>
                        <div className="flex flex-col gap-2">
                            {currentConcept.recipes.map((r: any) => (
                                <button
                                    key={r.id}
                                    onClick={() => router.push(`/recipes/${r.slug}`)}
                                    className="text-left p-3 border border-[#242424] bg-[#111111] rounded hover:border-[#8a8a8a] transition-all"
                                >
                                    <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">{r.book}</span>
                                    <span className="text-sm text-[#f2f2f2] block mt-0.5">{r.title}</span>
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                <div className="border-t border-[#242424] pt-6 mt-6">
                    <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">Authoritative System Coverage</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {(() => {
                            const { coverage, cookbookCount, playbookCount } = getBookCoverage(currentConcept.id);
                            return ["cookbook", "playbook"].map((bookId) => {
                                const book = db.books.find((b) => b.id === bookId);
                                const count = bookId === "cookbook" ? cookbookCount : playbookCount;
                                const progress = count > 0 ? (bookId === "playbook" ? "w-full bg-[#f5f2eb]" : "w-2/3 bg-[#8a8a8a]") : "w-0 bg-[#242424]";
                                return (
                                    <div
                                        key={bookId}
                                        onClick={() => router.push(`/books/${bookId}`)}
                                        className="p-4 border border-[#242424] bg-[#161616] rounded cursor-pointer hover:border-[#8a8a8a] transition-all"
                                    >
                                        <h5 className="text-xs font-bold text-[#f2f2f2]">{book?.title}</h5>
                                        <span className="text-[10px] text-[#8a8a8a] mt-0.5 block">{coverage[bookId]}</span>
                                        <div className="w-full bg-[#242424] h-1.5 rounded-full overflow-hidden mt-3">
                                            <div className={`h-full ${progress}`}></div>
                                        </div>
                                    </div>
                                );
                            });
                        })()}
                    </div>
                </div>
            </div>
        </ConsoleShell>
    );
}