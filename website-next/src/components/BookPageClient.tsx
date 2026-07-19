"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Bookmark } from "lucide-react";

import ConsoleShell from "./ConsoleShell";
import ContentBody from "./ContentBody";
import db from "../db/knowledge-base.json";

interface BookPageClientProps {
    bookId: string;
}

export default function BookPageClient({ bookId }: BookPageClientProps) {
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

    const book = db.books.find((b) => b.id === bookId) as any;
    if (!book) return null;

    const recipes = db.recipes.filter((r) => r.book === bookId);
    const bookRecipeCount = recipes.length;
    const totalRecipes = db.recipes.length;
    const coverage = totalRecipes > 0 ? Math.round((bookRecipeCount / totalRecipes) * 100) : 0;

    const conceptsUsed = Array.from(
        new Set(recipes.flatMap((r) => r.concepts || []))
    ).map((id) => db.concepts.find((c) => c.id === id)).filter(Boolean);

    const siblingBooks = db.books.filter((b) => b.id !== bookId);

    return (
        <ConsoleShell
            activeConceptId={null}
            breadcrumb={["Library", "Books", book.title]}
            onSelectConcept={handleSelectConcept}
        >
            <div className="flex flex-col gap-6 animate-fade-in flex-1">
                <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                    <div>
                        <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Book</span>
                        <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">{book.title}</h1>
                    </div>
                    <button onClick={() => toggleBookmark(book.id)} className="p-2 border border-[#242424] rounded hover:border-[#8a8a8a]" aria-label="Toggle bookmark">
                        <Bookmark className={`w-4 h-4 ${bookmarks.includes(book.id) ? "fill-[#f5f2eb] text-[#f5f2eb]" : "text-[#8a8a8a]"}`} />
                    </button>
                </div>

                {book.summary && (
                    <p className="text-lg text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">{book.summary}</p>
                )}

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 border border-[#242424] rounded bg-[#111111]">
                        <h5 className="text-xs font-mono uppercase text-[#8a8a8a] mb-2 font-bold">Recipes</h5>
                        <span className="text-2xl font-bold text-[#f5f2eb]">{bookRecipeCount}</span>
                    </div>
                    <div className="p-4 border border-[#242424] rounded bg-[#111111]">
                        <h5 className="text-xs font-mono uppercase text-[#8a8a8a] mb-2 font-bold">Concepts Touched</h5>
                        <span className="text-2xl font-bold text-[#f5f2eb]">{conceptsUsed.length}</span>
                    </div>
                    <div className="p-4 border border-[#242424] rounded bg-[#111111]">
                        <h5 className="text-xs font-mono uppercase text-[#8a8a8a] mb-2 font-bold">Library Coverage</h5>
                        <span className="text-2xl font-bold text-[#f5f2eb]">{coverage}%</span>
                    </div>
                </div>

                {book.body && <ContentBody body={book.body} />}

                <div className="border-t border-[#242424] pt-6">
                    <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">
                        Recipes ({recipes.length})
                    </h4>
                    <div className="flex flex-col gap-2">
                        {recipes.map((r: any) => (
                            <button
                                key={r.id}
                                onClick={() => router.push(`/recipes/${r.slug}`)}
                                className="text-left p-3 border border-[#242424] bg-[#111111] rounded hover:border-[#8a8a8a] transition-all"
                            >
                                <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">{r.difficulty}</span>
                                <span className="text-sm text-[#f2f2f2] block mt-0.5">{r.title}</span>
                            </button>
                        ))}
                    </div>
                </div>

                {conceptsUsed.length > 0 && (
                    <div className="border-t border-[#242424] pt-6 mt-2">
                        <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">
                            Concepts Covered ({conceptsUsed.length})
                        </h4>
                        <div className="flex flex-wrap gap-2">
                            {conceptsUsed.map((c: any) => (
                                <button
                                    key={c.id}
                                    onClick={() => handleSelectConcept(c.id)}
                                    className="px-3 py-1.5 text-xs border border-[#242424] bg-[#161616] rounded hover:border-[#8a8a8a] text-[#f2f2f2] transition-all"
                                >
                                    {c.title}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {siblingBooks.length > 0 && (
                    <div className="border-t border-[#242424] pt-6 mt-2">
                        <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">Other Books</h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {siblingBooks.map((b: any) => (
                                <div
                                    key={b.id}
                                    onClick={() => router.push(`/books/${b.id}`)}
                                    className="p-4 border border-[#242424] bg-[#161616] rounded cursor-pointer hover:border-[#8a8a8a] transition-all"
                                >
                                    <h5 className="text-xs font-bold text-[#f2f2f2]">{b.title}</h5>
                                    <span className="text-[10px] text-[#8a8a8a] mt-0.5 block">
                                        {db.recipes.filter((r) => r.book === b.id).length} Recipes
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </ConsoleShell>
    );
}