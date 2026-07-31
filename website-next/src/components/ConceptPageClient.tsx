"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Bookmark, BookOpen, Bug, ArrowRight, ChevronRight, Code2 } from "lucide-react";

import ConsoleShell from "./ConsoleShell";
import ContentBody from "./ContentBody";
import db from "../db/knowledge-base.json";

interface ConceptPageClientProps {
    conceptId: string;
}

const GROUP_LABELS: Record<string, string> = {
    fundamentals: "Fundamentals",
    detection: "Detection & Evasion",
    infrastructure: "Infrastructure & Scale",
    recovery: "Recovery & Observability",
    general: "Core Concepts",
};

export default function ConceptPageClient({ conceptId }: ConceptPageClientProps) {
    const router = useRouter();
    const [bookmarks, setBookmarks] = useState<string[]>([]);
    const [activeSection, setActiveSection] = useState<string>("overview");

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

    const { coverage, cookbookCount, playbookCount } = getBookCoverage(currentConcept.id);
    const relatedConcepts = (currentConcept.related || []).map((id) =>
        db.concepts.find((c) => c.id === id)
    ).filter(Boolean);

    const problems = db.problems.filter((p) => p.concept === currentConcept.id);
    const recipes = currentConcept.recipes || [];
    const nextSteps = (currentConcept.next_steps || []).map((id) =>
        db.concepts.find((c) => c.id === id)
    ).filter(Boolean);

    const sections = [
        { id: "overview", label: "Overview" },
        { id: "why", label: "Why It Matters" },
        ...(problems.length > 0 ? [{ id: "problems", label: "Common Problems" }] : []),
        ...(recipes.length > 0 ? [{ id: "recipes", label: "Example Recipes" }] : []),
        { id: "coverage", label: "Book Coverage" },
        ...(nextSteps.length > 0 ? [{ id: "next", label: "Next Steps" }] : []),
    ];

    return (
        <ConsoleShell
            activeConceptId={conceptId}
            breadcrumb={["Library", "Concepts", currentConcept.title]}
            onSelectConcept={handleSelectConcept}
        >
            <div className="flex gap-8">
                <nav className="hidden lg:flex flex-col gap-1 w-48 flex-shrink-0 sticky top-8 self-start">
                    <span className="text-[10px] uppercase text-[#8a8a8a] tracking-wider font-bold mb-2">On this page</span>
                    {sections.map((s) => (
                        <button
                            key={s.id}
                            onClick={() => {
                                setActiveSection(s.id);
                                document.getElementById(`section-${s.id}`)?.scrollIntoView({ behavior: "smooth" });
                            }}
                            className={`text-left text-xs py-1.5 px-2 rounded transition-all ${
                                activeSection === s.id
                                    ? "text-[#f5f2eb] bg-[#161616] border-l-2 border-[#f5f2eb]"
                                    : "text-[#8a8a8a] hover:text-[#f2f2f2] border-l-2 border-transparent"
                            }`}
                        >
                            {s.label}
                        </button>
                    ))}
                </nav>

                <div className="flex flex-col gap-8 animate-fade-in flex-1 min-w-0">
                    <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">
                                    {GROUP_LABELS[currentConcept.group] || "Concept"}
                                </span>
                                <span className="text-[#242424]">/</span>
                                <span className="text-[10px] font-mono text-[#8a8a8a]">{currentConcept.difficulty}</span>
                            </div>
                            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">{currentConcept.title}</h1>
                        </div>
                        <button onClick={() => toggleBookmark(currentConcept.id)} className="p-2 border border-[#242424] rounded hover:border-[#8a8a8a] flex-shrink-0" aria-label="Toggle bookmark">
                            <Bookmark className={`w-4 h-4 ${bookmarks.includes(currentConcept.id) ? "fill-[#f5f2eb] text-[#f5f2eb]" : "text-[#8a8a8a]"}`} />
                        </button>
                    </div>

                    <section id="section-overview">
                        <p className="text-lg text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">{currentConcept.summary}</p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
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
                                <div><span className="text-[#8a8a8a]">Compatibility: </span>{currentConcept.compatible_with}</div>
                                <div><span className="text-[#8a8a8a]">Last Reviewed: </span>{currentConcept.last_reviewed}</div>
                                <div><span className="text-[#8a8a8a]">Recipes: </span>{recipes.length} ({cookbookCount} cookbook / {playbookCount} playbook)</div>
                            </div>
                        </div>
                    </section>

                    <section id="section-why" className="border-t border-[#242424] pt-8">
                        <h2 className="text-xl font-bold text-[#f5f2eb] mb-4 flex items-center gap-2">
                            <BookOpen className="w-5 h-5 text-[#8a8a8a]" />
                            Why It Matters
                        </h2>
                        <p className="text-sm text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">
                            {currentConcept.summary}
                            {(currentConcept.aliases && currentConcept.aliases.length > 0) && (
                                <span className="block mt-3 text-[#8a8a8a]">
                                    Also known as: {currentConcept.aliases.join(", ")}.
                                </span>
                            )}
                        </p>
                        {currentConcept.tags && currentConcept.tags.length > 0 && (
                            <div className="flex flex-wrap gap-1.5 mt-4">
                                {currentConcept.tags.map((t: string) => (
                                    <span key={t} className="text-[10px] font-mono bg-[#161616] border border-[#242424] px-2 py-0.5 rounded text-[#8a8a8a]">
                                        {t}
                                    </span>
                                ))}
                            </div>
                        )}
                    </section>

                    {problems.length > 0 && (
                        <section id="section-problems" className="border-t border-[#242424] pt-8">
                            <h2 className="text-xl font-bold text-[#f5f2eb] mb-4 flex items-center gap-2">
                                <Bug className="w-5 h-5 text-yellow-400" />
                                Common Problems
                            </h2>
                            <div className="flex flex-col gap-2">
                                {problems.map((p: any) => (
                                    <button
                                        key={p.id}
                                        onClick={() => router.push(`/problems/${p.slug}`)}
                                        className="text-left p-3 border border-[#242424] bg-[#111111] rounded hover:border-[#8a8a8a] transition-all"
                                    >
                                        <div className="flex items-center gap-2">
                                            <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded uppercase ${
                                                p.severity === "critical" ? "bg-red-900/40 text-red-300" :
                                                p.severity === "common" ? "bg-yellow-900/40 text-yellow-300" :
                                                "bg-blue-900/40 text-blue-300"
                                            }`}>{p.severity}</span>
                                            <span className="text-sm text-[#f2f2f2]">{p.title}</span>
                                            <ArrowRight className="w-3 h-3 text-[#8a8a8a] ml-auto" />
                                        </div>
                                        {p.error_patterns && (
                                            <div className="flex flex-wrap gap-1 mt-2">
                                                {p.error_patterns.slice(0, 3).map((ep: string) => (
                                                    <code key={ep} className="text-[9px] bg-[#090909] px-1.5 py-0.5 rounded text-[#8a8a8a]">{ep}</code>
                                                ))}
                                                {p.error_patterns.length > 3 && (
                                                    <span className="text-[9px] text-[#8a8a8a]">+{p.error_patterns.length - 3} more</span>
                                                )}
                                            </div>
                                        )}
                                    </button>
                                ))}
                            </div>
                            <button
                                onClick={() => router.push(`/problems`)}
                                className="mt-3 text-xs text-[#8a8a8a] hover:text-[#f2f2f2] transition-all flex items-center gap-1"
                            >
                                View all error references <ArrowRight className="w-3 h-3" />
                            </button>
                        </section>
                    )}

                    <ContentBody body={currentConcept.body} />

                    {recipes.length > 0 && (
                        <section id="section-recipes" className="border-t border-[#242424] pt-8">
                            <h2 className="text-xl font-bold text-[#f5f2eb] mb-4 flex items-center gap-2">
                                <Code2 className="w-5 h-5 text-[#8a8a8a]" />
                                Example Recipes
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {recipes.slice(0, 6).map((r: any) => (
                                    <button
                                        key={r.id}
                                        onClick={() => router.push(`/recipes/${r.slug}`)}
                                        className="text-left p-3 border border-[#242424] bg-[#111111] rounded hover:border-[#8a8a8a] transition-all"
                                    >
                                        <span className="text-[9px] font-mono text-[#8a8a8a] uppercase">{r.book}</span>
                                        <span className="text-sm text-[#f2f2f2] block mt-0.5">{r.title}</span>
                                        <span className="text-[10px] text-[#8a8a8a] mt-1 block">{r.difficulty} · {r.environment?.join(", ")}</span>
                                    </button>
                                ))}
                            </div>
                            {recipes.length > 6 && (
                                <p className="text-xs text-[#8a8a8a] mt-3">+{recipes.length - 6} more recipes in the knowledge base</p>
                            )}
                        </section>
                    )}

                    <section id="section-coverage" className="border-t border-[#242424] pt-8">
                        <h2 className="text-xl font-bold text-[#f5f2eb] mb-4">Book Coverage</h2>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {["cookbook", "playbook"].map((bookId) => {
                                const book = db.books.find((b) => b.id === bookId);
                                const count = bookId === "cookbook" ? cookbookCount : playbookCount;
                                const progress = count > 0
                                    ? bookId === "playbook"
                                        ? "w-full bg-[#f5f2eb]"
                                        : "w-2/3 bg-[#8a8a8a]"
                                    : "w-0 bg-[#242424]";
                                return (
                                    <div
                                        key={bookId}
                                        onClick={() => router.push(`/books/${bookId}`)}
                                        className="p-4 border border-[#242424] bg-[#161616] rounded cursor-pointer hover:border-[#8a8a8a] transition-all"
                                    >
                                        <h5 className="text-sm font-bold text-[#f2f2f2]">{book?.title}</h5>
                                        <span className="text-[10px] text-[#8a8a8a] mt-0.5 block">
                                            {count > 0
                                                ? `${count} recipe${count > 1 ? "s" : ""} covering this concept`
                                                : "No direct recipes"
                                            }
                                        </span>
                                        <div className="w-full bg-[#242424] h-1.5 rounded-full overflow-hidden mt-3">
                                            <div className={`h-full ${progress}`}></div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </section>

                    {nextSteps.length > 0 && (
                        <section id="section-next" className="border-t border-[#242424] pt-8">
                            <h2 className="text-xl font-bold text-[#f5f2eb] mb-4 flex items-center gap-2">
                                <ArrowRight className="w-5 h-5 text-[#8a8a8a]" />
                                Next Steps
                            </h2>
                            <div className="flex flex-wrap gap-2">
                                {nextSteps.map((c: any) => (
                                    <button
                                        key={c.id}
                                        onClick={() => handleSelectConcept(c.id)}
                                        className="px-3 py-2 border border-[#242424] bg-[#161616] rounded hover:border-[#8a8a8a] text-left transition-all"
                                    >
                                        <span className="text-xs font-semibold text-[#f2f2f2] block">{c.title}</span>
                                        <span className="text-[10px] text-[#8a8a8a] mt-0.5 block">{c.difficulty}</span>
                                    </button>
                                ))}
                            </div>
                        </section>
                    )}

                    {relatedConcepts.length > 0 && (
                        <section className="border-t border-[#242424] pt-8">
                            <h2 className="text-xl font-bold text-[#f5f2eb] mb-4">Related Concepts</h2>
                            <div className="flex flex-wrap gap-2">
                                {relatedConcepts.map((rel: any) => (
                                    <button
                                        key={rel.id}
                                        onClick={() => handleSelectConcept(rel.id)}
                                        className="px-3 py-1.5 text-xs border border-[#242424] bg-[#161616] rounded hover:border-[#8a8a8a] text-[#f2f2f2] transition-all"
                                    >
                                        {rel.title}
                                    </button>
                                ))}
                            </div>
                        </section>
                    )}
                </div>
            </div>
        </ConsoleShell>
    );
}
