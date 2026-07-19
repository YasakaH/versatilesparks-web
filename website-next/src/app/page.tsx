"use client";

import React, { useState, useEffect } from "react";
import { Terminal, Search, Command, BookOpen, Code, ChevronRight, Bookmark, History, Layers, ExternalLink, Minimize2, Maximize2 } from "lucide-react";

import db from "../db/knowledge-base.json";
import KnowledgeGraph from "../components/KnowledgeGraph";
import Navigator from "../components/Navigator";
import CommandPalette from "../components/CommandPalette";

export default function Home() {
  const [activeConceptId, setActiveConceptId] = useState<string | null>(null);
  const [activeBookId, setActiveBookId] = useState<string | null>(null);
  const [activeRecipeId, setActiveRecipeId] = useState<string | null>(null);
  
  const [workspaceMode, setWorkspaceMode] = useState<"explore" | "study" | "reference">("explore");
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isPaletteOpen, setIsPaletteOpen] = useState(false);

  const [bookmarks, setBookmarks] = useState<string[]>([]);
  const [recentlyViewed, setRecentlyViewed] = useState<string[]>([]);
  const [breadcrumb, setBreadcrumb] = useState<string[]>(["Welcome"]);
  const [searchQuery, setSearchQuery] = useState("");

  // Load bookmarks & recently viewed on mount
  useEffect(() => {
    const savedBookmarks = localStorage.getItem("vs-bookmarks");
    if (savedBookmarks) setBookmarks(JSON.parse(savedBookmarks));

    const savedRecent = localStorage.getItem("vs-recent");
    if (savedRecent) setRecentlyViewed(JSON.parse(savedRecent));
  }, []);

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Shift+Space for Fullscreen Workspace Mode
      if (e.shiftKey && e.code === "Space") {
        e.preventDefault();
        setIsFullscreen(prev => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleSelectConcept = (id: string) => {
    setActiveConceptId(id);
    setActiveBookId(null);
    setActiveRecipeId(null);

    // Update history / breadcrumb path
    const conceptObj = db.concepts.find(c => c.id === id);
    if (conceptObj) {
      // Build logical trail based on requirements
      const trail = [];
      if (conceptObj.requires && conceptObj.requires.length > 0) {
        const parentId = conceptObj.requires[0];
        const parentObj = db.concepts.find(p => p.id === parentId);
        if (parentObj) trail.push(parentObj.title);
      }
      trail.push(conceptObj.title);
      setBreadcrumb(trail);

      // Add to recently viewed
      setRecentlyViewed(prev => {
        const filtered = prev.filter(x => x !== id);
        const updated = [id, ...filtered].slice(0, 5);
        localStorage.setItem("vs-recent", JSON.stringify(updated));
        return updated;
      });
    }
  };

  const handleSelectBook = (id: string) => {
    setActiveBookId(id);
    setActiveConceptId(null);
    setActiveRecipeId(null);
    const bookObj = db.books.find(b => b.id === id);
    if (bookObj) setBreadcrumb(["Library", bookObj.title]);
  };

  const handleSelectRecipe = (id: string) => {
    setActiveRecipeId(id);
    setActiveBookId(null);
    setActiveConceptId(null);
    const recipeObj = db.recipes.find(r => r.id === id);
    if (recipeObj) setBreadcrumb(["Recipes", recipeObj.title]);
  };

  const toggleBookmark = (id: string) => {
    setBookmarks(prev => {
      const updated = prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id];
      localStorage.setItem("vs-bookmarks", JSON.stringify(updated));
      return updated;
    });
  };

  const handleCommandPaletteAction = (actionId: string) => {
    if (actionId === "open-palette") {
      setIsPaletteOpen(true);
    } else if (actionId === "mode-explore") {
      setWorkspaceMode("explore");
    } else if (actionId === "mode-study") {
      setWorkspaceMode("study");
    } else if (actionId === "mode-reference") {
      setWorkspaceMode("reference");
    } else if (actionId === "toggle-workspace") {
      setIsFullscreen(prev => !prev);
    } else if (actionId === "download-v1") {
      window.open("/downloads/python-browser-automation-cookbook-sample.pdf");
    } else if (actionId === "download-v2") {
      window.open("/downloads/browser-automation-playbook-sample.pdf");
    } else if (actionId.startsWith("concept-")) {
      const cid = actionId.replace("concept-", "");
      handleSelectConcept(cid);
    } else if (actionId.startsWith("recipe-")) {
      const rid = actionId.replace("recipe-", "");
      handleSelectRecipe(rid);
    }
  };

  const getBookCoverage = (conceptId: string) => {
    const matchingRecipes = db.recipes.filter(r => r.concepts.includes(conceptId));
    const coverage: Record<string, string> = {
      cookbook: "No direct recipes",
      playbook: "No direct recipes"
    };

    let cookbookCount = 0;
    let playbookCount = 0;

    matchingRecipes.forEach(r => {
      if (r.book === "cookbook") cookbookCount++;
      if (r.book === "playbook") playbookCount++;
    });

    if (cookbookCount > 0) {
      coverage.cookbook = `${cookbookCount} Recipe${cookbookCount > 1 ? "s" : ""}`;
    }
    if (playbookCount > 0) {
      coverage.playbook = `${playbookCount} Recipe${playbookCount > 1 ? "s" : ""}`;
    }

    return { coverage, cookbookCount, playbookCount };
  };

  // Find active data objects
  const currentConcept = db.concepts.find(c => c.id === activeConceptId);
  const currentBook = db.books.find(b => b.id === activeBookId);
  const currentRecipe = db.recipes.find(r => r.id === activeRecipeId);

  // Search Results
  const searchResults = searchQuery ? [
    ...db.concepts.filter(c => 
      c.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      c.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (c.aliases && c.aliases.some((a: string) => a.toLowerCase().includes(searchQuery.toLowerCase())))
    ).map(c => ({ id: c.id, title: c.title, type: "concept" })),
    
    ...db.recipes.filter(r => 
      r.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.body.toLowerCase().includes(searchQuery.toLowerCase())
    ).map(r => ({ id: r.id, title: r.title, type: "recipe" }))
  ] : [];

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-[#090909] text-[#f2f2f2] font-mono selection:bg-[#f5f2eb] selection:text-[#090909]">
      
      {/* 1. Header Toolbar */}
      {!isFullscreen && (
        <header className="flex items-center justify-between border-b border-[#242424] bg-[#111111] px-6 py-3 select-none flex-shrink-0">
          <div className="flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-[#f5f2eb]"></span>
            <span className="text-xs font-bold tracking-widest uppercase">Browser Infrastructure Browser</span>
          </div>

          {/* Breadcrumbs */}
          <div className="hidden md:flex items-center gap-2 text-xs text-[#8a8a8a] max-w-lg truncate">
            {breadcrumb.map((crumb, idx) => (
              <React.Fragment key={idx}>
                {idx > 0 && <ChevronRight className="w-3.5 h-3.5" />}
                <span className={idx === breadcrumb.length - 1 ? "text-[#f2f2f2] font-semibold" : ""}>{crumb}</span>
              </React.Fragment>
            ))}
          </div>

          <div className="flex items-center gap-4">
            {/* Search Input bar */}
            <div className="relative">
              <Search className="absolute left-2.5 top-1.5 w-4 h-4 text-[#8a8a8a]" />
              <input
                type="text"
                placeholder="Search..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="w-[180px] bg-[#161616] border border-[#242424] text-xs px-8 py-1.5 rounded focus:outline-none focus:border-[#8a8a8a] text-[#f2f2f2] placeholder-[#8a8a8a]"
              />
              {searchQuery && (
                <button onClick={() => setSearchQuery("")} className="absolute right-2 top-1.5 text-xs text-[#8a8a8a] hover:text-[#f2f2f2]">✕</button>
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

      {/* 2. Main Workspace Layout */}
      <div className="flex-1 flex overflow-hidden relative">
        
        {/* Left Knowledge Graph */}
        {!isFullscreen && workspaceMode === "explore" && (
          <aside className="w-[320px] border-r border-[#242424] bg-[#0c0c0c] p-4 overflow-y-auto flex-shrink-0 select-none">
            <KnowledgeGraph 
              activeConceptId={activeConceptId} 
              onSelectConcept={handleSelectConcept} 
              db={db}
            />
            
            {/* Mode Picker */}
            <div className="mt-6 border-t border-[#242424] pt-4 flex flex-col gap-2">
              <span className="text-[10px] uppercase text-[#8a8a8a] tracking-wider font-bold">Workspace Mode</span>
              <div className="grid grid-cols-3 gap-1 bg-[#111111] p-1 border border-[#242424] rounded">
                {(["explore", "study", "reference"] as const).map(m => (
                  <button
                    key={m}
                    onClick={() => setWorkspaceMode(m)}
                    className={`text-[10px] py-1 capitalize rounded transition-all font-mono font-semibold ${
                      workspaceMode === m ? "bg-[#f5f2eb] text-[#090909]" : "text-[#8a8a8a] hover:text-[#f2f2f2]"
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>
          </aside>
        )}

        {/* Center Panel (Active Content Panel) */}
        <main className="flex-1 flex flex-col overflow-y-auto bg-[#090909] p-8 md:p-12 relative min-w-0">
          
          {/* Fullscreen indicator */}
          <button 
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="absolute top-6 right-6 text-[#8a8a8a] hover:text-[#f2f2f2] p-1.5 rounded bg-[#161616] border border-[#242424] z-10"
            title="Toggle Focus Workspace (Shift+Space)"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>

          {/* Search Overlay list */}
          {searchQuery ? (
            <div className="flex flex-col gap-6 max-w-3xl">
              <h2 className="text-2xl font-bold tracking-tight border-b border-[#242424] pb-2 text-[#f5f2eb]">
                Search Index Results
              </h2>
              <div className="flex flex-col gap-3">
                {searchResults.length === 0 ? (
                  <p className="text-sm text-[#8a8a8a]">No index entries found matching "{searchQuery}"</p>
                ) : (
                  searchResults.map(res => (
                    <div 
                      key={res.id}
                      onClick={() => {
                        setSearchQuery("");
                        if (res.type === "concept") handleSelectConcept(res.id);
                        else handleSelectRecipe(res.id);
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
            <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col">
              
              {/* Concept Workspace */}
              {currentConcept && (
                <div className="flex flex-col gap-6 animate-fade-in flex-1">
                  <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                    <div>
                      <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Concept Specification</span>
                      <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">
                        {currentConcept.title}
                      </h1>
                    </div>
                    <button 
                      onClick={() => toggleBookmark(currentConcept.id)}
                      className="p-2 border border-[#242424] rounded hover:border-[#8a8a8a]"
                    >
                      <Bookmark className={`w-4 h-4 ${bookmarks.includes(currentConcept.id) ? "fill-[#f5f2eb] text-[#f5f2eb]" : "text-[#8a8a8a]"}`} />
                    </button>
                  </div>

                  <p className="text-lg text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">
                    {currentConcept.summary}
                  </p>

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

                  {/* Long form text */}
                  <div className="prose prose-invert max-w-none text-[#8a8a8a] leading-relaxed text-sm md:text-md space-y-4 font-sans py-4 border-t border-[#242424]">
                    {currentConcept.body.split("\n\n").map((para: string, idx: number) => {
                      if (para.startsWith("###")) {
                        return <h3 key={idx} className="text-lg font-bold text-[#f2f2f2] mt-6 mb-2 font-mono">{para.replace("###", "").trim()}</h3>;
                      }
                      if (para.startsWith("1.")) {
                        return (
                          <ol key={idx} className="list-decimal pl-5 space-y-2">
                            {para.split("\n").map((li, lidx) => (
                              <li key={lidx}>{li.replace(/^\d+\.\s*/, "")}</li>
                            ))}
                          </ol>
                        );
                      }
                      return <p key={idx}>{para}</p>;
                    })}
                  </div>

                  {/* Authorship Evidence */}
                  <div className="border-t border-[#242424] pt-6 mt-6">
                    <h4 className="text-xs uppercase text-[#8a8a8a] font-bold tracking-wider mb-4">Authoritative System Coverage</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {(() => {
                        const { coverage, cookbookCount, playbookCount } = getBookCoverage(currentConcept.id);
                        return ["cookbook", "playbook"].map(bookId => {
                          const book = db.books.find(b => b.id === bookId);
                          const count = bookId === "cookbook" ? cookbookCount : playbookCount;
                          const progress = count > 0 ? (bookId === "playbook" ? "w-full bg-[#f5f2eb]" : "w-2/3 bg-[#8a8a8a]") : "w-0 bg-[#242424]";
                          return (
                            <div 
                              key={bookId} 
                              onClick={() => handleSelectBook(bookId)}
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
              )}

              {/* Book Workspace */}
              {currentBook && (
                <div className="flex flex-col gap-6 animate-fade-in flex-1">
                  <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                    <div>
                      <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Handbook Specification</span>
                      <h1 className="text-3xl font-extrabold tracking-tight mt-1 text-[#f5f2eb]">{currentBook.title}</h1>
                    </div>
                  </div>

                  <p className="text-lg text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">
                    {currentBook.subtitle}
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-4">
                    <div className="p-6 border border-[#242424] rounded bg-[#111111] flex flex-col justify-between">
                      <div>
                        <span className="text-xs uppercase text-[#8a8a8a] font-bold">Specifications</span>
                        <ul className="text-xs text-[#8a8a8a] mt-3 space-y-2">
                          {currentBook.formats.map((f: string, idx: number) => (
                            <li key={idx}>✓ {f}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="border-t border-[#242424] pt-4 mt-6">
                        <span className="text-2xl font-bold text-[#f2f2f2]">${currentBook.price_usd} USD</span>
                        <span className="text-[10px] text-[#8a8a8a] block mt-1">Free rolling updates</span>
                      </div>
                    </div>

                    <div className="p-6 border border-[#242424] rounded bg-[#111111] flex flex-col justify-between">
                      <div>
                        <span className="text-xs uppercase text-[#8a8a8a] font-bold">Free Preview</span>
                        <p className="text-xs text-[#8a8a8a] mt-3 leading-relaxed">
                          Get immediate access to the Table of Contents, Introduction, and the first complete recipe.
                        </p>
                      </div>
                      <a 
                        href={`/downloads/${currentBook.id === "cookbook" ? "python-browser-automation-cookbook-sample.pdf" : "browser-automation-playbook-sample.pdf"}`}
                        className="w-full text-center py-2.5 text-xs rounded border border-[#f5f2eb] hover:bg-[#f5f2eb] hover:text-[#090909] text-[#f5f2eb] font-semibold transition-all mt-6"
                        download
                      >
                        Download Sample PDF
                      </a>
                    </div>
                  </div>

                  <div className="prose prose-invert max-w-none text-[#8a8a8a] leading-relaxed text-sm md:text-md space-y-4 font-sans py-4 border-t border-[#242424]">
                    {currentBook.body.split("\n\n").map((para: string, idx: number) => (
                      <p key={idx}>{para}</p>
                    ))}
                  </div>

                  {/* Buy Button Container */}
                  <div className="border-t border-[#242424] pt-6 flex justify-end">
                    <a 
                      href={currentBook.gumroad_url} 
                      target="_blank"
                      className="py-3 px-8 text-sm rounded bg-[#f5f2eb] text-[#090909] font-bold hover:bg-[#e8e4db] transition-all flex items-center gap-2"
                    >
                      <span>Acquire Handbook</span>
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                </div>
              )}

              {/* Recipe Workspace */}
              {currentRecipe && (
                <div className="flex flex-col gap-6 animate-fade-in flex-1">
                  <div className="flex items-center justify-between border-b border-[#242424] pb-4">
                    <div>
                      <span className="text-xs uppercase text-[#8a8a8a] font-semibold tracking-widest">Recipe File Readout</span>
                      <h1 className="text-2xl font-bold tracking-tight mt-1 text-[#f5f2eb]">{currentRecipe.title}</h1>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 text-xs font-mono">
                    <div className="p-3 border border-[#242424] bg-[#111111] rounded">
                      <span className="text-[#8a8a8a] block mb-1">Difficulty</span>
                      <span className="font-semibold text-[#f2f2f2]">{currentRecipe.difficulty}</span>
                    </div>
                    <div className="p-3 border border-[#242424] bg-[#111111] rounded">
                      <span className="text-[#8a8a8a] block mb-1">Source Handbook</span>
                      <span className="font-semibold text-[#f2f2f2] capitalize">{currentRecipe.book}</span>
                    </div>
                    <div className="p-3 border border-[#242424] bg-[#111111] rounded">
                      <span className="text-[#8a8a8a] block mb-1">Runtime Env</span>
                      <span className="font-semibold text-[#f2f2f2]">{currentRecipe.environment.join(" + ")}</span>
                    </div>
                  </div>

                  <div className="prose prose-invert max-w-none text-[#8a8a8a] leading-relaxed text-sm md:text-md space-y-4 font-sans py-4 border-t border-[#242424]">
                    {currentRecipe.body.split("\n\n").map((para: string, idx: number) => {
                      if (para.startsWith("```")) {
                        const code = para.replace(/```python|```/g, "").trim();
                        return (
                          <pre key={idx} className="bg-[#111111] border border-[#242424] p-4 rounded text-xs font-mono text-[#f2f2f2] overflow-x-auto my-4">
                            <code>{code}</code>
                          </pre>
                        );
                      }
                      return <p key={idx}>{para}</p>;
                    })}
                  </div>
                </div>
              )}

              {/* Default Welcome / Map Landing Page */}
              {!activeConceptId && !activeBookId && !activeRecipeId && (
                <div className="flex-1 flex flex-col justify-between">
                  <div className="flex flex-col gap-6 py-6 max-w-2xl">
                    <h1 className="text-5xl font-extrabold tracking-tight text-[#f5f2eb] leading-tight select-none">
                      Build<br />
                      Browser<br />
                      Infrastructure.
                    </h1>
                    <p className="text-md text-[#8a8a8a] leading-relaxed font-sans mt-2">
                      An interactive knowledge system for production browser engineering. Skip standard WebDriver bot traps. Master CDP interception, self-healing daemons, and TLS fingerprinting pool orchestration.
                    </p>
                  </div>

                  {/* Inline Library Cards */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-8">
                    {db.books.map(book => (
                      <div 
                        key={book.id}
                        onClick={() => handleSelectBook(book.id)}
                        className="p-6 border border-[#242424] bg-[#111111] rounded-lg cursor-pointer hover:border-[#8a8a8a] transition-all flex flex-col justify-between"
                      >
                        <div>
                          <span className="text-[10px] font-mono text-[#8a8a8a] uppercase tracking-widest">Publication</span>
                          <h3 className="text-md font-bold text-[#f5f2eb] mt-1">{book.title}</h3>
                          <p className="text-xs text-[#8a8a8a] mt-2 font-sans">{book.subtitle}</p>
                        </div>
                        <span className="text-xs font-semibold text-[#f5f2eb] underline mt-6 block">Explore coverage &rarr;</span>
                      </div>
                    ))}
                  </div>

                  {/* Knowledge Explorer / Navigator */}
                  <Navigator db={db} onSelectConcept={handleSelectConcept} />
                </div>
              )}

            </div>
          )}
        </main>

        {/* Right Reference Coverage Inspector */}
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

            {/* Quick Actions / Local Bookmarks */}
            <div className="border-t border-[#242424] pt-6 mt-6 flex flex-col gap-4">
              <div>
                <span className="text-[10px] font-mono text-[#8a8a8a] uppercase tracking-wider block mb-2">Bookmarks</span>
                {bookmarks.length === 0 ? (
                  <span className="text-[10px] text-[#8a8a8a]">No local bookmarks saved.</span>
                ) : (
                  <div className="flex flex-col gap-1.5 max-h-[120px] overflow-y-auto">
                    {bookmarks.map(bid => {
                      const concept = db.concepts.find(c => c.id === bid);
                      return (
                        <button
                          key={bid}
                          onClick={() => handleSelectConcept(bid)}
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

      {/* 3. Bottom Activity Log / History Strip */}
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
                recentlyViewed.map(rid => {
                  const concept = db.concepts.find(c => c.id === rid);
                  return (
                    <button 
                      key={rid} 
                      onClick={() => handleSelectConcept(rid)}
                      className="text-[#f2f2f2] hover:underline"
                    >
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

      {/* 4. Command Palette Modal */}
      <CommandPalette 
        isOpen={isPaletteOpen} 
        onClose={() => setIsPaletteOpen(false)} 
        onSelectAction={handleCommandPaletteAction} 
        db={db}
      />

    </div>
  );
}
