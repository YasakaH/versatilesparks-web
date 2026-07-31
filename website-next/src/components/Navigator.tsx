"use client";

import React, { useState } from "react";
import { Filter } from "lucide-react";
import type { Concept, Recipe } from "../types/knowledge";

interface NavigatorProps {
  db: {
    recipes: Recipe[];
    concepts: Concept[];
  };
  onSelectConcept: (id: string) => void;
}

export default function Navigator({ db, onSelectConcept }: NavigatorProps) {
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>("all");
  const [selectedConcept, setSelectedConcept] = useState<string>("all");
  const [selectedEnvironment, setSelectedEnvironment] = useState<string>("all");

  const difficulties = ["all", "Beginner", "Intermediate", "Advanced"];
  const environments = ["all", "Python", "nodriver"];

  const filteredRecipes = db.recipes.filter(recipe => {
    const diffMatch = selectedDifficulty === "all" || recipe.difficulty === selectedDifficulty;
    const envMatch = selectedEnvironment === "all" || recipe.environment.includes(selectedEnvironment);
    const conceptMatch = selectedConcept === "all" || recipe.concepts.includes(selectedConcept);
    return diffMatch && envMatch && conceptMatch;
  });

  return (
    <div className="bg-[#111111] border border-[#242424] rounded-lg p-6 flex flex-col gap-6">
      <div className="flex items-center justify-between border-b border-[#242424] pb-3">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-[#f5f2eb]" />
          <span className="text-xs uppercase tracking-widest font-mono text-[#8a8a8a]">Knowledge Explorer</span>
        </div>
        <span className="text-[10px] font-mono text-[#8a8a8a] bg-[#161616] px-2 py-0.5 rounded border border-[#242424]">
          {filteredRecipes.length} Matches
        </span>
      </div>

      {/* Filter Rails */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Difficulty */}
        <div>
          <label className="block text-[11px] font-mono uppercase text-[#8a8a8a] mb-2">Difficulty</label>
          <div className="flex flex-wrap gap-1.5">
            {difficulties.map(diff => (
              <button
                key={diff}
                onClick={() => setSelectedDifficulty(diff)}
                className={`text-xs px-2.5 py-1 rounded font-mono border transition-all ${selectedDifficulty === diff
                    ? "bg-[#f5f2eb] border-[#f5f2eb] text-[#090909]"
                    : "bg-[#161616] border-[#242424] text-[#8a8a8a] hover:text-[#f2f2f2]"
                  }`}
              >
                {diff}
              </button>
            ))}
          </div>
        </div>

        {/* Concept Filter */}
        <div>
          <label className="block text-[11px] font-mono uppercase text-[#8a8a8a] mb-2">Concept Area</label>
          <select
            value={selectedConcept}
            onChange={e => setSelectedConcept(e.target.value)}
            className="w-full bg-[#161616] border border-[#242424] text-xs text-[#f2f2f2] rounded px-2.5 py-1.5 focus:outline-none focus:border-[#8a8a8a]"
          >
            <option value="all">All Concepts</option>
            {db.concepts.map(c => (
              <option key={c.id} value={c.id}>{c.title}</option>
            ))}
          </select>
        </div>

        {/* Environment */}
        <div>
          <label className="block text-[11px] font-mono uppercase text-[#8a8a8a] mb-2">Environment</label>
          <div className="flex flex-wrap gap-1.5">
            {environments.map(env => (
              <button
                key={env}
                onClick={() => setSelectedEnvironment(env)}
                className={`text-xs px-2.5 py-1 rounded font-mono border transition-all ${selectedEnvironment === env
                    ? "bg-[#f5f2eb] border-[#f5f2eb] text-[#090909]"
                    : "bg-[#161616] border-[#242424] text-[#8a8a8a] hover:text-[#f2f2f2]"
                  }`}
              >
                {env}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Recipes Output */}
      <div className="flex flex-col gap-3 max-h-[300px] overflow-y-auto pr-1">
        {filteredRecipes.length === 0 ? (
          <div className="text-center py-6 text-xs text-[#8a8a8a] border border-dashed border-[#242424] rounded-lg">
            No recipes matching the active filter criteria.
          </div>
        ) : (
          filteredRecipes.map(recipe => (
            <div
              key={recipe.id}
              className="bg-[#161616] border border-[#242424] rounded-md p-4 flex flex-col gap-2 hover:border-[#8a8a8a] transition-all"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <span className="text-[10px] font-mono uppercase tracking-wider text-[#8a8a8a]">
                    Recipe {recipe.id.replace("recipe-", "")}
                  </span>
                  <h4 className="text-sm font-semibold text-[#f2f2f2] mt-0.5">{recipe.title}</h4>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded border border-[#242424] bg-[#111111] text-[#8a8a8a] whitespace-nowrap">
                  {recipe.book === "cookbook" ? "Cookbook" : "Playbook"}
                </span>
              </div>
              <p className="text-xs text-[#8a8a8a] line-clamp-2 mt-1">{recipe.body.split("\n\n")[0]}</p>

              <div className="flex items-center justify-between border-t border-[#242424] pt-3 mt-1">
                <div className="flex items-center gap-1.5">
                  {recipe.concepts.map((cid: string) => {
                    const concept = db.concepts.find(c => c.id === cid);
                    return (
                      <button
                        key={cid}
                        onClick={() => onSelectConcept(cid)}
                        className="text-[10px] font-mono text-[#f5f2eb] hover:underline"
                      >
                        #{concept?.title || cid}
                      </button>
                    );
                  })}
                </div>
                <span className="text-[10px] font-mono text-[#8a8a8a]">
                  {recipe.environment.join(" + ")}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
