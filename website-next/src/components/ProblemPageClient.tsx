"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Bookmark, AlertTriangle, ArrowRight } from "lucide-react";

import ConsoleShell from "./ConsoleShell";
import ContentBody from "./ContentBody";
import db from "../db/knowledge-base.json";

interface ProblemPageClientProps {
    problemId: string;
}

export default function ProblemPageClient({ problemId }: ProblemPageClientProps) {
    const router = useRouter();
    const [bookmarks, setBookmarks] = useState<string[]>([]);

    useEffect(() => {
        const savedBookmarks = localStorage.getItem("vs-bookmarks");
        if (savedBookmarks) setBookmarks(JSON.parse(savedBookmarks));
    }, []);

    const currentProblem = db.problems.find((p) => p.id === problemId);
    if (!currentProblem) return null;

    const severityColor: Record<string, string> = {
        common: "bg-yellow-900/40 text-yellow-300 border-yellow-700",
        rare: "bg-blue-900/40 text-blue-300 border-blue-700",
        critical: "bg-red-900/40 text-red-300 border-red-700",
    };

    return (
        <ConsoleShell
            activeConceptId={currentProblem.concept}
            breadcrumb={["Library", "Problems", currentProblem.title]}
            onSelectConcept={(id: string) => router.push(`/concepts/${id}`)}
        >
            <div className="flex flex-col gap-6 animate-fade-in flex-1">
                <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                    <div className="flex items-center gap-3">
                        <AlertTriangle className="w-5 h-5 text-yellow-400" />
                        <div>
                            <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Error Reference</span>
                            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">{currentProblem.title}</h1>
                        </div>
                    </div>
                </div>

                <div className="flex flex-wrap gap-2">
                    <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono font-bold border ${severityColor[currentProblem.severity] || severityColor.common}`}>
                        {currentProblem.severity}
                    </span>
                    {currentProblem.conceptObject && (
                        <button
                            onClick={() => router.push(`/concepts/${currentProblem.conceptObject!.slug}`)}
                            className="px-2.5 py-0.5 rounded text-[10px] font-mono border border-[#242424] bg-[#161616] text-[#8a8a8a] hover:border-[#8a8a8a] transition-all flex items-center gap-1"
                        >
                            {currentProblem.conceptObject.title}
                            <ArrowRight className="w-3 h-3" />
                        </button>
                    )}
                </div>

                <p className="text-base text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">{currentProblem.description}</p>

                {currentProblem.error_patterns && currentProblem.error_patterns.length > 0 && (
                    <div className="p-4 border border-[#242424] rounded bg-[#111111]">
                        <h5 className="text-xs font-mono uppercase text-[#8a8a8a] mb-2 font-bold">Error Patterns</h5>
                        <div className="flex flex-wrap gap-1.5">
                            {currentProblem.error_patterns.map((pattern: string) => (
                                <code key={pattern} className="text-[11px] bg-[#090909] border border-[#242424] px-2 py-0.5 rounded text-[#f2f2f2]">
                                    {pattern}
                                </code>
                            ))}
                        </div>
                    </div>
                )}

                <ContentBody body={currentProblem.body} />
            </div>
        </ConsoleShell>
    );
}
