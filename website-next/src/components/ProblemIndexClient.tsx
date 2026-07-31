"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, AlertTriangle, ChevronRight } from "lucide-react";

import ConsoleShell from "./ConsoleShell";

interface ProblemIndexClientProps {
    problems: any[];
    grouped: Record<string, any[]>;
}

export default function ProblemIndexClient({ problems, grouped }: ProblemIndexClientProps) {
    const router = useRouter();
    const [query, setQuery] = useState("");

    const q = query.trim().toLowerCase();
    const filtered = q
        ? problems.filter((p) =>
            p.title.toLowerCase().includes(q) ||
            p.description.toLowerCase().includes(q) ||
            (p.error_patterns || []).some((ep: string) => ep.toLowerCase().includes(q))
        )
        : null;

    return (
        <ConsoleShell
            activeConceptId={null}
            breadcrumb={["Library", "Problems"]}
            onSelectConcept={(id: string) => router.push(`/concepts/${id}`)}
        >
            <div className="flex flex-col gap-6 animate-fade-in flex-1 max-w-4xl">
                <div className="border-b border-[#242424] pb-4">
                    <div className="flex items-center gap-3 mb-2">
                        <AlertTriangle className="w-6 h-6 text-yellow-400" />
                        <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Error Reference</span>
                    </div>
                    <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#f5f2eb]">Browser Automation Error Reference</h1>
                    <p className="text-sm text-[#8a8a8a] mt-2 max-w-2xl">
                        Search by error message, symptom, or concept. Each entry links to the relevant concept and recipe.
                    </p>
                </div>

                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#8a8a8a]" />
                    <input
                        type="text"
                        placeholder="Search errors by message, pattern, or concept..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="w-full bg-[#111111] border border-[#242424] text-sm px-10 py-2.5 rounded focus:outline-none focus:border-[#8a8a8a] text-[#f2f2f2] placeholder-[#8a8a8a]"
                    />
                    {query && (
                        <button onClick={() => setQuery("")} className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[#8a8a8a] hover:text-[#f2f2f2]">
                            Clear
                        </button>
                    )}
                </div>

                {filtered !== null ? (
                    <div className="flex flex-col gap-2">
                        {filtered.length === 0 ? (
                            <p className="text-sm text-[#8a8a8a]">No errors matching "{query}"</p>
                        ) : (
                            filtered.map((p: any) => (
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
                                        {p.conceptObject && (
                                            <span className="text-[10px] text-[#8a8a8a] ml-auto">{p.conceptObject.title}</span>
                                        )}
                                    </div>
                                    {p.error_patterns && (
                                        <div className="flex flex-wrap gap-1 mt-2">
                                            {p.error_patterns.slice(0, 4).map((ep: string) => (
                                                <code key={ep} className="text-[9px] bg-[#090909] px-1.5 py-0.5 rounded text-[#8a8a8a]">{ep}</code>
                                            ))}
                                        </div>
                                    )}
                                </button>
                            ))
                        )}
                    </div>
                ) : (
                    <div className="flex flex-col gap-8">
                        {Object.entries(grouped).map(([concept, probs]) => (
                            <div key={concept}>
                                <h3 className="text-sm font-bold text-[#f5f2eb] mb-3 flex items-center gap-2">
                                    <ChevronRight className="w-3 h-3 text-[#8a8a8a]" />
                                    {concept}
                                    <span className="text-[10px] text-[#8a8a8a] font-normal">({probs.length})</span>
                                </h3>
                                <div className="flex flex-col gap-2">
                                    {probs.map((p: any) => (
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
                                            </div>
                                            {p.error_patterns && (
                                                <div className="flex flex-wrap gap-1 mt-2">
                                                    {p.error_patterns.slice(0, 3).map((ep: string) => (
                                                        <code key={ep} className="text-[9px] bg-[#090909] px-1.5 py-0.5 rounded text-[#8a8a8a]">{ep}</code>
                                                    ))}
                                                </div>
                                            )}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </ConsoleShell>
    );
}
