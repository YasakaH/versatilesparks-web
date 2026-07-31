"use client";

import React, { useEffect, useState, useRef } from "react";
import { Search, BookOpen, Terminal, Code, Settings } from "lucide-react";
import type { Concept, Recipe, Book, Problem } from "../types/knowledge";

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectAction: (actionId: string, param?: string) => void;
  db: {
    concepts: Concept[];
    recipes: Recipe[];
    books: Book[];
    problems: Problem[];
  };
}

export default function CommandPalette({ isOpen, onClose, onSelectAction, db }: CommandPaletteProps) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setQuery("");
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        if (isOpen) onClose();
        else onSelectAction("open-palette");
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose, onSelectAction]);

  if (!isOpen) return null;

  // Build searchable items
  const defaultActions = [
    { id: "mode-explore", title: "Switch to Explore Mode", subtitle: "Rich grid view with graph", category: "System", icon: Settings },
    { id: "mode-study", title: "Switch to Study Mode", subtitle: "Calm, focused reading workspace", category: "System", icon: Settings },
    { id: "mode-reference", title: "Switch to Reference Mode", subtitle: "Dense DevDocs style registry", category: "System", icon: Settings },
    { id: "toggle-workspace", title: "Toggle Workspace Mode (Shift+Space)", subtitle: "Toggle absolute fullscreen", category: "System", icon: Settings },
    { id: "download-v1", title: "Download Cookbook Sample PDF", subtitle: "Free preview including Recipe 1", category: "Downloads", icon: BookOpen },
    { id: "download-v2", title: "Download Playbook Sample PDF", subtitle: "Free preview including Chapter 1 & 2", category: "Downloads", icon: BookOpen },
  ];

  const conceptActions = db.concepts.map(c => ({
    id: `concept-${c.id}`,
    title: `Go to Concept: ${c.title}`,
    subtitle: c.summary,
    category: "Concepts",
    icon: Terminal
  }));

  const recipeActions = db.recipes.map(r => ({
    id: `recipe-${r.id}`,
    title: `Go to Recipe: ${r.title}`,
    subtitle: `${r.book === "cookbook" ? "Cookbook" : "Playbook"} • ${r.difficulty} • ${r.environment.join(", ")}`,
    category: "Recipes",
    icon: Code
  }));

  const problemActions = (db.problems || []).map(p => ({
    id: `problem-${p.id}`,
    title: `Error: ${p.title}`,
    subtitle: p.description,
    category: "Errors",
    icon: Terminal
  }));

  const allItems = [...defaultActions, ...conceptActions, ...recipeActions, ...problemActions];

  const filteredItems = allItems.filter(item => {
    const searchString = `${item.title} ${item.subtitle} ${item.category}`.toLowerCase();
    return searchString.includes(query.toLowerCase());
  });

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex(prev => (prev + 1) % Math.max(1, filteredItems.length));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex(prev => (prev - 1 + filteredItems.length) % Math.max(1, filteredItems.length));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (filteredItems[selectedIndex]) {
        const item = filteredItems[selectedIndex];
        onSelectAction(item.id);
        onClose();
      }
    } else if (e.key === "Escape") {
      e.preventDefault();
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4 bg-black/60 backdrop-blur-sm">
      <div
        className="w-full max-w-2xl bg-[#111111] border border-[#242424] rounded-lg shadow-2xl overflow-hidden"
        onKeyDown={handleKeyDown}
      >
        <div className="flex items-center px-4 border-b border-[#242424]">
          <Search className="w-5 h-5 text-[#8a8a8a] mr-3" />
          <input
            ref={inputRef}
            type="text"
            className="w-full py-4 bg-transparent text-[#f2f2f2] placeholder-[#8a8a8a] focus:outline-none text-md"
            placeholder="Type a command or search concepts (e.g. proxy, session)..."
            value={query}
            onChange={e => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
          />
          <kbd className="hidden sm:inline-flex items-center gap-1 px-2 py-1 rounded bg-[#161616] border border-[#242424] text-[10px] text-[#8a8a8a]">
            ESC
          </kbd>
        </div>

        <div className="max-h-[350px] overflow-y-auto p-2">
          {filteredItems.length === 0 ? (
            <div className="py-8 text-center text-sm text-[#8a8a8a]">
              No matches found for "{query}"
            </div>
          ) : (
            filteredItems.map((item, index) => {
              const Icon = item.icon;
              const isSelected = index === selectedIndex;
              return (
                <div
                  key={item.id}
                  className={`flex items-center justify-between px-3 py-3 rounded-md cursor-pointer transition-colors ${isSelected ? "bg-[#161616]" : ""
                    }`}
                  onClick={() => {
                    onSelectAction(item.id);
                    onClose();
                  }}
                  onMouseEnter={() => setSelectedIndex(index)}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <Icon className={`w-4 h-4 flex-shrink-0 ${isSelected ? "text-[#f5f2eb]" : "text-[#8a8a8a]"}`} />
                    <div className="min-w-0">
                      <p className={`text-sm font-semibold truncate ${isSelected ? "text-[#f5f2eb]" : "text-[#f2f2f2]"}`}>
                        {item.title}
                      </p>
                      <p className="text-xs text-[#8a8a8a] truncate mt-0.5">{item.subtitle}</p>
                    </div>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded border ${isSelected ? "bg-[#242424] border-[#8a8a8a] text-[#f2f2f2]" : "bg-transparent border-[#242424] text-[#8a8a8a]"
                    }`}>
                    {item.category}
                  </span>
                </div>
              );
            })
          )}
        </div>
        <div className="flex items-center justify-between px-4 py-2 bg-[#161616] border-t border-[#242424] text-[11px] text-[#8a8a8a]">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <kbd className="px-1.5 py-0.5 rounded bg-[#111111] border border-[#242424]">↑↓</kbd> Navigate
            </span>
            <span className="flex items-center gap-1">
              <kbd className="px-1.5 py-0.5 rounded bg-[#111111] border border-[#242424]">Enter</kbd> Select
            </span>
          </div>
          <span>Command Palette</span>
        </div>
      </div>
    </div>
  );
}