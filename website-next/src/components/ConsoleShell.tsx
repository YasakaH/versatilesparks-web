"use client";

import React, { useState, useEffect, useCallback } from "react";
import {
    Terminal,
    Search,
    Command,
    ChevronRight,
    Layers,
    Bookmark,
    Minimize2,
    Maximize2,
} from "lucide-react";

import db from "../db/knowledge-base.json";
import KnowledgeGraph from "./KnowledgeGraph";
import CommandPalette from "./CommandPalette";

interface ConsoleShellProps {
    activeConceptId: string | null;
    activeBookId?: string | null;
    breadcrumb: string[];
    onSelectConcept: (id: string) => void;
    children: React.ReactNode;
}

/**
 * ConsoleShell — the shared "Browser Infrastructure Browser" console chrome
 * (header toolbar, left knowledge graph, right system inspector, footer
 * activity log, command palette). Extracted from page.tsx so that the home
 * page and the /concepts /recipes /books routes can all reuse the same shell
 * without duplicating ~400 lines of layout code.
 *
 * The main content area is supplied as `children`, so each route owns its own
 * markup and SEO metadata while the shell stays consistent.
 */
export default function ConsoleShell({
    activeConceptId,
    activeBookId = null,
    breadcrumb,
    onSelectConcept,
    children,
}: ConsoleShellProps) {
    const [workspaceMode, setWorkspaceMode] = useState<"explore" | "study" | "reference">("explore");
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [isPaletteOpen, setIsPaletteOpen] = useState(false);
    const [bookmarks, setBookmarks] = useState<string[]>([]);
    const [recentlyViewed, setRecentlyViewed] = useState<string[]>([]);
    const [searchQuery, setSearchQuery] = useState("");

    useEffect(() => {
        const savedBookmarks = localStorage.getItem("vs-bookmarks");
        if (savedBookmarks) setBookmarks(JSON.parse(savedBookmarks));
        const savedRecent = localStorage.getItem("vs-recent");
        if (savedRecent) setRecentlyViewed(JSON.parse(savedRecent));
    }, []);

    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.shiftKey && e.code === "Space") {
                e.preventDefault();
                setIsFullscreen((prev) => !prev);
            }
        };
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, []);

    const toggleBookmark = useCallback((id: string) => {
        setBookmarks((prev) => {
            const updated = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
            localStorage.setItem("vs-bookmarks", JSON.stringify(updated));
            return updated;
        });
    }, []);

    const handleCommandPaletteAction = useCallback(
        (actionId: string) => {
            if (actionId === "open-palette") setIsPaletteOpen(true);
            else if (actionId === "mode-explore") setWorkspaceMode("explore");
            else if (actionId === "mode-study") setWorkspaceMode("study");
            else if (actionId === "mode-reference") setWorkspaceMode("reference");
            else if (actionId === "toggle-workspace") setIsFullscreen((prev) => !prev);
            else if (actionId === "download-v1")
                window.open("/downloads/python-browser-automation-cookbook-sample.pdf");
            else if (actionId === "download-v2")
                window.open("/downloads/browser-automation-playbook-sample.pdf");
            else if (actionId.startsWith("concept-")) onSelectConcept(actionId.replace("concept-", ""));
        },
        [onSelectConcept]
    );

    const currentConcept = db.concepts.find((c) => c.id === activeConceptId);
    const currentBook = db.books.find((b) => b.id === activeBookId);

    const q = searchQuery.trim().toLowerCase();
    type Scored = { id: string; title: string; type: "concept" | "recipe"; score: number };
    const searchResults: Scored[] = q
        ? (() => {
            const results: Scored[] = [];
            db.concepts.forEach((c) => {
                const title = (c.title || "").toLowerCase();
                const summary = (c.summary || "").toLowerCase();
                const body = (c.body || "").toLowerCase();
                const tags: string[] = c.tags || [];
                const aliases: string[] = c.aliases || [];
                let score = 0;
                if (title.includes(q)) score = Math.max(score, 100 + (title === q ? 50 : 0));
                if (aliases.some((a) => a.toLowerCase().includes(q))) score = Math.max(score, 90);
                if (summary.includes(q)) score = Math.max(score, 50);
                if (tags.some((t) => t.toLowerCase().includes(q))) score = Math.max(score, 40);
                if (body.includes(q)) score = Math.max(score, 10);
                if (score > 0) results.push({ id: c.id, title: c.title, type: "concept", score });
            });
            db.recipes.forEach((r) => {
                const title = (r.title || "").toLowerCase();
                const body = (r.body || "").toLowerCase();
                let score = 0;
                if (title.includes(q)) score = Math.max(score, 80);
                if (body.includes(q)) score = Math.max(score, 10);
                if (score > 0) results.push({ id: r.id, title: r.title, type: "recipe", score });
            });
            return results.sort((a, b) => {
                if (a.type !== b.type) return a.type === "concept" ? -1 : 1;
                if (b.score !== a.score) return b.score - a.score;
                return a.title.localeCompare(b.title);
            });
        })()
        : [];

    return (
        <div className="h-screen flex flex-col overflow-hidden bg-[#090909] text-[#f2f2f2] font-mono selection:bg-[#f5f2eb] selection:text-[#090909]">
            {!isFullscreen && (
                <header className="flex items-center justify-between border-b border-[#242424] bg-[#111111] px-6 py-3 select-none flex-shrink-0">
                    <div className="flex items-center gap-3">
                        <span className="w-2.5 h-2.5 rounded-full bg-[#f5f2eb]"></span>
                        <span className="text-xs font-bold tracking-widest uppercase">Browser Infrastructure Browser</span>
                    </div>
                    <div className="hidden md:flex items-center gap-2 text-xs text-[#8a8a8a] max-w-lg truncate">
                        {breadcrumb.map((crumb, idx) => (
                            <React.Fragment key={idx}>
                                {idx > 0 && <ChevronRight className="w-3.5 h-3.5" />}
                                <span className={idx === breadcrumb.length - 1 ? "text-[#f2f2f2] font-semibold" : ""}>{crumb}</span>
                            </React.Fragment>
                        ))}
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="relative">
                            <Search className="absolute left-2.5 top-1.5 w-4 h-4 text-[#8a8a8a]" />
                            <input
                                type="text"
                                placeholder="Search..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                aria-label="Search knowledge base"
                                className="w-[180px] bg-[#161616] border border-[#242424] text-xs px-8 py-1.5 rounded focus:outline-none focus:border-[#8a8a8a] text-[#f2f2f2] placeholder-[#8a8a8a]"
                            />
                            {searchQuery && (
                                <button
                                    onClick={() => setSearchQuery("")}
                                    className="absolute right-2 top-1.5 text-xs text-[#8a8a8a] hover:text-[#f2f2f2]"
                                    aria-label="Clear search"
                                >
                                    ✕
                                </button>
                            )}
                        </div>
                        <button
                            onClick={() => setIsPaletteOpen(true)}
                            className="flex items-center gap-1.5 text-xs bg-[#161616] border border-[#242424] px-3 py-1.5 rounded hover:text-[#f5f2eb] transition-all"
                        >
                            <Command className="w-3.5 h-3.5" />
                            <span>⌘K</span>
                        </button>
                    </div>
                </header>
            )}

            <div className="flex-1 flex overflow-hidden relative">
                {!isFullscreen && workspaceMode === "explore" && (
                    <aside className="w-[320px] border-r border-[#242424] bg-[#0c0c0c] p-4 overflow-y-auto flex-shrink-0 select-none">
                        <KnowledgeGraph activeConceptId={activeConceptId} onSelectConcept={onSelectConcept} db={db} />
                        <div className="mt-6 border-t border-[#242424] pt-4 flex flex-col gap-2">
                            <span className="text-[10px] uppercase text-[#8a8a8a] tracking-wider font-bold">Workspace Mode</span>
                            <div className="grid grid-cols-3 gap-1 bg-[#111111] p-1 border border-[#242424] rounded" role="tablist" aria-label="Workspace mode">
                                {(["explore", "study", "reference"] as const).map((m) => (
                                    <button
                                        key={m}
                                        onClick={() => setWorkspaceMode(m)}
                                        role="tab"
                                        aria-selected={workspaceMode === m}
                                        className={`text-[10px] py-1 capitalize rounded transition-all font-mono font-semibold ${workspaceMode === m ? "bg-[#f5f2eb] text-[#090909]" : "text-[#8a8a8a] hover:text-[#f2f2f2]"
                                            }`}
                                    >
                                        {m}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </aside>
                )}

                <main className="flex-1 flex flex-col overflow-y-auto bg-[#090909] p-8 md:p-12 relative min-w-0">
                    <button
                        onClick={() => setIsFullscreen(!isFullscreen)}
                        className="absolute top-6 right-6 text-[#8a8a8a] hover:text-[#f2f2f2] p-1.5 rounded bg-[#161616] border border-[#242424] z-10"
                        title="Toggle Focus Workspace (Shift+Space)"
                        aria-label={isFullscreen ? "Exit focus workspace" : "Enter focus workspace"}
                    >
                        {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                    </button>

                    {searchQuery ? (
                        <div className="flex flex-col gap-6 max-w-3xl">
                            <h2 className="text-2xl font-bold tracking-tight border-b border-[#242424] pb-2 text-[#f5f2eb]">
                                Search Index Results
                            </h2>
                            <div className="flex flex-col gap-3">
                                {searchResults.length === 0 ? (
                                    <p className="text-sm text-[#8a8a8a]">No index entries found matching "{searchQuery}"</p>
                                ) : (
                                    searchResults.map((res) => (
                                        <div
                                            key={res.id}
                                            onClick={() => {
                                                setSearchQuery("");
                                                if (res.type === "concept") onSelectConcept(res.id);
                                            }}
                                            className="p-4 rounded border border-[#242424] bg-[#111111] hover:border-[#8a8a8a] cursor-pointer transition-all"
                                        >
                                            <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">{res.type}</span>
                                            <h4 className="text-md font-semibold text-[#f2f2f2] mt-0.5">{res.title}</h4>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    ) : (
                        children
                    )}
                </main>

                {!isFullscreen && (
                    <aside className="w-[300px] border-l border-[#242424] bg-[#0c0c0c] p-6 overflow-y-auto flex-shrink-0 select-none hidden lg:flex flex-col justify-between">
                        <div>
                            <div className="flex items-center gap-2 mb-6 border-b border-[#242424] pb-3">
                                <Layers className="w-4 h-4 text-[#f5f2eb]" />
                                <span className="text-xs uppercase tracking-widest font-mono text-[#8a8a8a]">System Inspector</span>
                            </div>
                            {currentConcept ? (
                                <div className="flex flex-col gap-5">
                                    <div>
                                        <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">Active Scope</span>
                                        <h3 className="text-md font-bold text-[#f5f2eb] mt-1">{currentConcept.title}</h3>
                                    </div>
                                    <div>
                                        <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">Difficulty Rank</span>
                                        <span className="text-xs block mt-1 font-semibold text-[#f2f2f2]">{currentConcept.difficulty}</span>
                                    </div>
                                    {currentConcept.tags && (
                                        <div>
                                            <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">Indexer Tags</span>
                                            <div className="flex flex-wrap gap-1 mt-2">
                                                {currentConcept.tags.map((t: string) => (
                                                    <span key={t} className="text-[9px] font-mono bg-[#161616] border border-[#242424] px-1.5 py-0.5 rounded text-[#8a8a8a]">
                                                        {t}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                    {currentConcept.aliases && (
                                        <div>
                                            <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">Keywords / Aliases</span>
                                            <p className="text-xs text-[#8a8a8a] mt-1 leading-relaxed">{currentConcept.aliases.join(", ")}</p>
                                        </div>
                                    )}
                                </div>
                            ) : currentBook ? (
                                <div className="flex flex-col gap-5">
                                    <div>
                                        <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">Product Catalog</span>
                                        <h3 className="text-md font-bold text-[#f5f2eb] mt-1">{currentBook.title}</h3>
                                    </div>
                                    <div>
                                        <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">Version Revision</span>
                                        <span className="text-xs block mt-1 font-semibold text-[#f2f2f2]">v{currentBook.version}</span>
                                    </div>
                                    <div>
                                        <span className="text-[10px] font-mono text-[#8a8a8a] uppercase">Acquisition Cost</span>
                                        <span className="text-sm block mt-1 font-bold text-[#f5f2eb]">${currentBook.price_usd} USD</span>
                                    </div>
                                </div>
                            ) : (
                                <div className="flex flex-col gap-3 text-xs text-[#8a8a8a] leading-relaxed">
                                    <p>Select a node in the graph map or search a concept to inspect low-level relationships, difficulty scores, and book code coverage indexes.</p>
                                </div>
                            )}
                        </div>
                        <div className="border-t border-[#242424] pt-6 mt-6 flex flex-col gap-4">
                            <div>
                                <span className="text-[10px] font-mono text-[#8a8a8a] uppercase tracking-wider block mb-2">Bookmarks</span>
                                {bookmarks.length === 0 ? (
                                    <span className="text-[10px] text-[#8a8a8a]">No local bookmarks saved.</span>
                                ) : (
                                    <div className="flex flex-col gap-1.5 max-h-[120px] overflow-y-auto">
                                        {bookmarks.map((bid) => {
                                            const concept = db.concepts.find((c) => c.id === bid);
                                            return (
                                                <button
                                                    key={bid}
                                                    onClick={() => onSelectConcept(bid)}
                                                    className="text-left text-[10px] text-[#f2f2f2] hover:text-[#f5f2eb] truncate flex items-center gap-1 font-mono hover:underline"
                                                >
                                                    <Bookmark className="w-2.5 h-2.5 fill-[#f5f2eb] text-[#f5f2eb]" />
                                                    <span>{concept?.title || bid}</span>
                                                </button>
                                            );
                                        })}
                                    </div>
                                )}
                            </div>
                            <div className="flex justify-between items-center text-[10px] text-[#8a8a8a] border-t border-[#242424] pt-3">
                                <span className="flex items-center gap-1"><Command className="w-3 h-3" /> Shift+Space</span>
                                <span>Workspace Toggle</span>
                            </div>
                        </div>
                    </aside>
                )}
            </div>

            {!isFullscreen && (
                <footer className="border-t border-[#242424] bg-[#0c0c0c] px-6 py-2.5 flex justify-between items-center text-xs text-[#8a8a8a] select-none flex-shrink-0">
                    <div className="flex items-center gap-3">
                        <Terminal className="w-3.5 h-3.5 text-[#f5f2eb]" />
                        <span>SYS: ACTIVE</span>
                        <span>•</span>
                        <span>VER: v2.0.0</span>
                    </div>
                    <div className="hidden sm:flex items-center gap-4">
                        <span>Recently Viewed:</span>
                        <div className="flex items-center gap-2">
                            {recentlyViewed.length === 0 ? (
                                <span>None</span>
                            ) : (
                                recentlyViewed.map((rid) => {
                                    const concept = db.concepts.find((c) => c.id === rid);
                                    return (
                                        <button key={rid} onClick={() => onSelectConcept(rid)} className="text-[#f2f2f2] hover:underline">
                                            {concept?.title || rid}
                                        </button>
                                    );
                                })
                            )}
                        </div>
                    </div>
                    <div>
                        <span>SYSTEM OK</span>
                    </div>
                </footer>
            )}

            <CommandPalette isOpen={isPaletteOpen} onClose={() => setIsPaletteOpen(false)} onSelectAction={handleCommandPaletteAction} db={db} />
        </div>
    );
}