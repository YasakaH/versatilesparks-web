"use client";

import React, { useState } from "react";
import { Terminal } from "lucide-react";

interface Node {
  id: string;
  title: string;
  x: number;
  y: number;
  requires: string[];
  used_by: string[];
}

interface KnowledgeGraphProps {
  activeConceptId: string | null;
  onSelectConcept: (id: string) => void;
  db: {
    concepts: any[];
  };
}

export default function KnowledgeGraph({ activeConceptId, onSelectConcept, db }: KnowledgeGraphProps) {
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);

  // Position coordinates inside an 800x820 viewBox
  const nodes: Node[] = [
    { id: "authentication", title: "Authentication", x: 400, y: 60, requires: [], used_by: ["cookies", "sessions"] },
    { id: "cookies", title: "Cookies", x: 250, y: 150, requires: ["authentication"], used_by: ["sessions"] },
    { id: "sessions", title: "Persistent Sessions", x: 550, y: 150, requires: ["cookies", "authentication"], used_by: ["anti-detection"] },
    { id: "anti-detection", title: "Anti Detection", x: 400, y: 250, requires: ["sessions"], used_by: ["fingerprints", "profiles"] },
    { id: "fingerprints", title: "Fingerprinting", x: 250, y: 350, requires: ["anti-detection"], used_by: ["cdp"] },
    { id: "profiles", title: "Browser Profiles", x: 550, y: 350, requires: ["anti-detection"], used_by: ["cdp"] },
    { id: "cdp", title: "CDP Direct Access", x: 400, y: 450, requires: ["fingerprints", "profiles"], used_by: ["network-interception"] },
    { id: "network-interception", title: "Network Interception", x: 400, y: 540, requires: ["cdp"], used_by: ["scaling"] },
    { id: "scaling", title: "Scaling & Orchestration", x: 400, y: 630, requires: ["network-interception"], used_by: ["observability"] },
    { id: "observability", title: "Observability", x: 400, y: 720, requires: ["scaling"], used_by: ["recovery"] },
    { id: "recovery", title: "Self-Healing Recovery", x: 400, y: 800, requires: ["observability"], used_by: [] }
  ];

  // Helper to determine highlight status
  const getHighlightStatus = (nodeId: string) => {
    const focusId = hoveredNodeId || activeConceptId;
    if (!focusId) return "normal";
    
    if (nodeId === focusId) return "active";
    
    const focusNode = nodes.find(n => n.id === focusId);
    if (!focusNode) return "dimmed";

    if (focusNode.requires.includes(nodeId)) return "prerequisite";
    if (focusNode.used_by.includes(nodeId)) return "dependent";
    
    return "dimmed";
  };

  // Compile connections
  const connections: { from: Node; to: Node; id: string }[] = [];
  nodes.forEach(node => {
    node.used_by.forEach(depId => {
      const depNode = nodes.find(n => n.id === depId);
      if (depNode) {
        connections.push({
          from: node,
          to: depNode,
          id: `${node.id}-${depNode.id}`
        });
      }
    });
  });

  const getLineHighlight = (fromId: string, toId: string) => {
    const focusId = hoveredNodeId || activeConceptId;
    if (!focusId) return "normal";

    if (fromId === focusId || toId === focusId) {
      if (fromId === focusId) return "outgoing";
      return "incoming";
    }

    return "dimmed";
  };

  return (
    <div className="w-full flex flex-col bg-[#111111] border border-[#242424] rounded-lg p-6">
      <div className="flex items-center gap-2 mb-4 border-b border-[#242424] pb-3">
        <Terminal className="w-4 h-4 text-[#f5f2eb]" />
        <span className="text-xs uppercase tracking-widest font-mono text-[#8a8a8a]">Dependency Engine Map</span>
      </div>

      <div className="relative overflow-auto max-h-[650px] flex justify-center">
        <svg 
          viewBox="0 0 800 850" 
          className="w-full max-w-[650px] h-auto select-none"
        >
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#242424" />
            </marker>
            <marker id="arrow-active" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#f5f2eb" />
            </marker>
          </defs>

          {/* Draw Connection Lines */}
          {connections.map(conn => {
            const highlight = getLineHighlight(conn.from.id, conn.to.id);
            let strokeColor = "#242424";
            let strokeWidth = 1.5;
            let classVal = "";

            if (highlight === "outgoing") {
              strokeColor = "#f5f2eb";
              strokeWidth = 2;
              classVal = "dependency-line";
            } else if (highlight === "incoming") {
              strokeColor = "#8a8a8a";
              strokeWidth = 2;
              classVal = "dependency-line";
            } else if (hoveredNodeId || activeConceptId) {
              strokeColor = "#141414";
            }

            return (
              <line
                key={conn.id}
                x1={conn.from.x}
                y1={conn.from.y}
                x2={conn.to.x}
                y2={conn.to.y}
                stroke={strokeColor}
                strokeWidth={strokeWidth}
                className={classVal}
                markerEnd={highlight === "outgoing" || highlight === "incoming" ? "url(#arrow-active)" : "url(#arrow)"}
              />
            );
          })}

          {/* Draw Nodes */}
          {nodes.map(node => {
            const status = getHighlightStatus(node.id);
            let bgColor = "#161616";
            let borderColor = "#242424";
            let textColor = "#8a8a8a";
            let strokeWidth = 1;

            if (status === "active") {
              bgColor = "#f5f2eb";
              borderColor = "#f5f2eb";
              textColor = "#090909";
              strokeWidth = 2;
            } else if (status === "prerequisite") {
              borderColor = "#8a8a8a";
              textColor = "#f2f2f2";
              strokeWidth = 1.5;
            } else if (status === "dependent") {
              borderColor = "#f5f2eb";
              textColor = "#f2f2f2";
              strokeWidth = 1.5;
            } else if (status === "normal") {
              textColor = "#f2f2f2";
            }

            return (
              <g
                key={node.id}
                className="cursor-pointer"
                onClick={() => onSelectConcept(node.id)}
                onMouseEnter={() => setHoveredNodeId(node.id)}
                onMouseLeave={() => setHoveredNodeId(null)}
              >
                {/* Node Box */}
                <rect
                  x={node.x - 90}
                  y={node.y - 20}
                  width={180}
                  height={40}
                  rx={4}
                  fill={bgColor}
                  stroke={borderColor}
                  strokeWidth={strokeWidth}
                  className="transition-all duration-200"
                />
                {/* Node text */}
                <text
                  x={node.x}
                  y={node.y + 4}
                  textAnchor="middle"
                  className="text-xs font-mono font-semibold"
                  fill={textColor}
                >
                  {node.title}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
}
