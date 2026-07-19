"use client";

import React, { useState, useEffect } from "react";
import { ExternalLink, Bookmark } from "lucide-react";
import { useRouter } from "next/navigation";

import db from "../db/knowledge-base.json";
import ConsoleShell from "../components/ConsoleShell";
import Navigator from "../components/Navigator";

/**
 * Home — the indexable landing route ("/").
 *
 * Manages active concept/book/recipe state and renders the center content
 * (welcome screen, concept spec, book spec, recipe readout). The surrounding
 * console chrome (header, graph, inspector, footer, command palette) is
 * provided by <ConsoleShell/>, shared with the dedicated /concepts, /recipes
 * and /books routes.
 *
 * Selecting a concept navigates to /concepts/[slug] so each concept has a
 * canonical, indexable URL (better SEO than SPA-style state switching).
 */
export default function Home() {
  const router = useRouter();
  const [activeConceptId, setActiveConceptId] = useState<string | null>(null);
  const [activeBookId, setActiveBookId] = useState<string | null>(null);
  const [activeRecipeId, setActiveRecipeId] = useState<string | null>(null);
  const [breadcrumb, setBreadcrumb] = useState<string[]>(["Welcome"]);
  const [bookmarks, setBookmarks] = useState<string[]>([]);

  useEffect(() => {
    const savedBookmarks = localStorage.getItem("vs-bookmarks");
    if (savedBookmarks) setBookmarks(JSON.parse(savedBookmarks));
  }, []);

  // Navigate to canonical concept route for SEO + shareability.
  const handleSelectConcept = (id: string) => {
    const conceptObj = db.concepts.find((c) => c.id === id);
    if (!conceptObj) return;
    router.push(`/concepts/${conceptObj.slug || id}`);
  };

  const handleSelectBook = (id: string) => {
    setActiveBookId(id);
    setActiveConceptId(null);
    setActiveRecipeId(null);
    const bookObj = db.books.find((b) => b.id === id);
    if (bookObj) setBreadcrumb(["Library", bookObj.title]);
  };

  const handleSelectRecipe = (id: string) => {
    setActiveRecipeId(id);
    setActiveBookId(null);
    setActiveConceptId(null);
    const recipeObj = db.recipes.find((r) => r.id === id);
    if (recipeObj) setBreadcrumb(["Recipes", recipeObj.title]);
  };

  const toggleBookmark = (id: string) => {
    setBookmarks((prev) => {
      const updated = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
      localStorage.setItem("vs-bookmarks", JSON.stringify(updated));
      return updated;
    });
  };

  const getBookCoverage = (conceptId: string) => {
    const matchingRecipes = db.recipes.filter((r) => r.concepts.includes(conceptId));
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

  const currentConcept = db.concepts.find((c) => c.id === activeConceptId);
  const currentBook = db.books.find((b) => b.id === activeBookId);
  const currentRecipe = db.recipes.find((r) => r.id === activeRecipeId);

  return (
    <ConsoleShell
      activeConceptId={activeConceptId}
      activeBookId={activeBookId}
      breadcrumb={breadcrumb}
      onSelectConcept={handleSelectConcept}
    >
      <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col">
        {/* Concept Workspace */}
        {currentConcept && (
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
                      <div key={bookId} onClick={() => handleSelectBook(bookId)} className="p-4 border border-[#242424] bg-[#161616] rounded cursor-pointer hover:border-[#8a8a8a] transition-all">
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

            <p className="text-lg text-[#f2f2f2] leading-relaxed max-w-3xl font-sans font-light">{currentBook.subtitle}</p>

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

            <div className="border-t border-[#242424] pt-6 flex justify-end">
              <a href={currentBook.gumroad_url} target="_blank" rel="noopener noreferrer" className="py-3 px-8 text-sm rounded bg-[#f5f2eb] text-[#090909] font-bold hover:bg-[#e8e4db] transition-all flex items-center gap-2">
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

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-8">
              {db.books.map((book) => (
                <div key={book.id} onClick={() => handleSelectBook(book.id)} className="p-6 border border-[#242424] bg-[#111111] rounded-lg cursor-pointer hover:border-[#8a8a8a] transition-all flex flex-col justify-between">
                  <div>
                    <span className="text-[10px] font-mono text-[#8a8a8a] uppercase tracking-widest">Publication</span>
                    <h3 className="text-md font-bold text-[#f5f2eb] mt-1">{book.title}</h3>
                    <p className="text-xs text-[#8a8a8a] mt-2 font-sans">{book.subtitle}</p>
                  </div>
                  <span className="text-xs font-semibold text-[#f5f2eb] underline mt-6 block">Explore coverage &rarr;</span>
                </div>
              ))}
            </div>

            <Navigator db={db} onSelectConcept={handleSelectConcept} />
          </div>
        )}
      </div>
    </ConsoleShell>
  );
}