"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Bookmark } from "lucide-react";

import ConsoleShell from "./ConsoleShell";
import ContentBody from "./ContentBody";
import db from "../db/knowledge-base.json";

interface RecipePageClientProps {
    recipeId: string;
}

export default function RecipePageClient({ recipeId }: RecipePageClientProps) {
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

    const recipe = db.recipes.find((r) => r.id === recipeId) as any;
    if (!recipe) return null;

    const book = db.books.find((b) => b.id === recipe.book);
    const relatedRecipes = db.recipes.filter(
        (r) => r.book === recipe.book && r.id !== recipe.id && r.concepts.some((c: string) => recipe.concepts.includes(c))
    );

    return (
        <ConsoleShell
            activeConceptId={null}
            breadcrumb={["Library", book?.title || "Recipes", recipe.title]}
            onSelectConcept={handleSelectConcept}
        >
            <div className="flex flex-col gap-6 animate-fade-in flex-1">
                <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                    <div>
                        <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">
                            Recipe {recipe.chapter ? `· Ch. ${recipe.chapter}` : ""} · {book?.title}
                        </span>
                        <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">{recipe.title}</h1>
                    </div>
                    <button onClick={() => toggleBookmark(recipe.id)} className="p-2 border border-[#242424] rounded hover:border-[#8a8a8a]" aria-label="Toggle bookmark">
                        <Bookmark className={`w-4 h-4 ${bookmarks.includes(recipe.id) ? "fill-[#f5f2eb] text-[#f5f2eb]" : "text-[#8a8a8a]"}`} />
                    </button>
                </div>

                {recipe.summary && (
                    <p className="text-lg text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">{recipe.summary}</p>
                )}

                <div className="p-4 border border-[#242424] rounded bg-[#111111]">
                    <h5 className="text-xs font-mono uppercase text-[#8a8a8a] mb-3 font-bold">Concepts Covered</h5>
                    <div className="flex flex-wrap gap-2">
                        {recipe.concepts && recipe.concepts.length > 0 ? (
                            recipe.concepts.map((cId: string) => {
                                const concept = db.concepts.find((c) => c.id === cId);
                                if (!concept) return null;
                                return (
                                    <button
                                        key={cId}
                                        onClick={() => handleSelectConcept(cId)}
                                        className="px-3 py-1.5 text-xs border border-[#242424] bg-[#161616] rounded hover:border-[#8a8a8a] text-[#f2f2f2] transition-all"
                                    >
                                        {concept.title}
                                    </button>
                                );
                            })
                        ) : (
                            <span className="text-xs text-[#8a8a8a]">None</span>
                        )}
                    </div>
                </div>

                <ContentBody body={recipe.body || ""} />

                <div className="border-t border-[#242424] pt-6">
                    <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">
                        Source: {book?.title}
                    </h4>
                    <button
                        onClick={() => router.push(`/books/${recipe.book}`)}
                        className="text-left p-4 border border-[#242424] bg-[#161616] rounded hover:border-[#8a8a8a] transition-all"
                    >
                        <span className="text-xs text-[#8a8a8a] font-mono uppercase">View Book</span>
                        <span className="block text-sm text-[#f2f2f2] mt-1">{book?.title}</span>
                    </button>
                </div>

                {relatedRecipes.length > 0 && (
                    <div className="border-t border-[#242424] pt-6 mt-2">
                        <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">Related Recipes ({relatedRecipes.length})</h4>
                        <div className="flex flex-col gap-2">
                            {relatedRecipes.slice(0, 8).map((r: any) => (
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
            </div>
        </ConsoleShell>
    );
}