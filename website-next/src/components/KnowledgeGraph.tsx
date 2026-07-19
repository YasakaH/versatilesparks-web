"use client";

import React, { useRef, useState, useCallback, useEffect } from "react";
import { Terminal, ZoomIn, ZoomOut, Maximize } from "lucide-react";

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

const MIN_ZOOM = 0.4;
const MAX_ZOOM = 3;
const ZOOM_STEP = 0.15;

export default function KnowledgeGraph({ activeConceptId, onSelectConcept, db }: KnowledgeGraphProps) {
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const panStart = useRef({ x: 0, y: 0, panX: 0, panY: 0, moved: false });
  const svgRef = useRef<SVGSVGElement | null>(null);

  // Position coordinates inside an 800x860 viewBox
  const nodes: Node[] = [
    { id: "authentication", title: "Authentication", x: 400, y: 60, requires: [], used_by: ["cookies", "sessions"] },
    { id: "cookies", title: "Cookies", x: 230, y: 170, requires: ["authentication"], used_by: ["sessions"] },
    { id: "sessions", title: "Persistent Sessions", x: 570, y: 170, requires: ["cookies", "authentication"], used_by: ["anti-detection"] },
    { id: "anti-detection", title: "Anti Detection", x: 400, y: 280, requires: ["sessions"], used_by: ["fingerprints", "profiles", "proxies"] },
    { id: "fingerprints", title: "Fingerprinting", x: 150, y: 400, requires: ["anti-detection"], used_by: ["cdp"] },
    { id: "proxies", title: "Proxies & IP Rotation", x: 400, y: 400, requires: ["anti-detection"], used_by: ["cdp", "network-interception"] },
    { id: "profiles", title: "Browser Profiles", x: 650, y: 400, requires: ["anti-detection"], used_by: ["cdp"] },
    { id: "cdp", title: "Chrome DevTools Protocol", x: 400, y: 520, requires: ["fingerprints", "profiles", "proxies"], used_by: ["network-interception"] },
    { id: "network-interception", title: "Network Interception", x: 400, y: 620, requires: ["cdp", "proxies"], used_by: ["scaling"] },
    { id: "scaling", title: "Scaling & Orchestration", x: 400, y: 720, requires: ["network-interception"], used_by: ["observability"] },
    { id: "observability", title: "Observability", x: 400, y: 810, requires: ["scaling"], used_by: ["recovery"] },
    { id: "recovery", title: "Self-Healing & Recovery", x: 400, y: 890, requires: ["observability"], used_by: [] }
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

  // ---- Zoom helpers ----
  const clampZoom = (z: number) => Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, z));

  const zoomBy = useCallback((factor: number, centerSvg?: { x: number; y: number }) => {
    setZoom(prevZoom => {
      const next = clampZoom(prevZoom * factor);
      if (centerSvg && svgRef.current && next !== prevZoom) {
        // Keep cursor-centered zoom: shift pan so the same viewBox point stays under cursor.
        // viewBox coords of cursor = (centerSvg - pan) / prevZoom
        // After zoom we want: viewBox coord * nextZoom + newPan = centerSvg
        // => newPan = centerSvg - viewBoxCoord * nextZoom
        const vbX = (centerSvg.x - pan.x) / prevZoom;
        const vbY = (centerSvg.y - pan.y) / prevZoom;
        setPan({
          x: centerSvg.x - vbX * next,
          y: centerSvg.y - vbY * next
        });
      }
      return next;
    });
  }, [pan.x, pan.y]);

  const handleWheel = (e: React.WheelEvent<SVGSVGElement>) => {
    // Only zoom when pointer is over the SVG, never hijack the whole page.
    e.preventDefault();
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    const cursor = { x: e.clientX - rect.left, y: e.clientY - rect.top };
    const factor = e.deltaY < 0 ? 1 + ZOOM_STEP : 1 - ZOOM_STEP;
    zoomBy(factor, cursor);
  };

  // ---- Pan helpers ----
  const onPointerDown = (e: React.PointerEvent<SVGSVGElement>) => {
    // Only initiate pan with primary button; ignore when starting on a node (let node onClick fire).
    if (e.button !== 0) return;
    (e.target as Element).setPointerCapture?.(e.pointerId);
    panStart.current = {
      x: e.clientX,
      y: e.clientY,
      panX: pan.x,
      panY: pan.y,
      moved: false
    };
    setIsPanning(true);
  };

  const onPointerMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!isPanning) return;
    const dx = e.clientX - panStart.current.x;
    const dy = e.clientY - panStart.current.y;
    if (Math.abs(dx) + Math.abs(dy) > 3) panStart.current.moved = true;
    setPan({ x: panStart.current.panX + dx, y: panStart.current.panY + dy });
  };

  const onPointerUp = (e: React.PointerEvent<SVGSVGElement>) => {
    (e.target as Element).releasePointerCapture?.(e.pointerId);
    setIsPanning(false);
  };

  const resetView = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  // Keyboard zoom (when graph panel is focused)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "+" || e.key === "=") zoomBy(1 + ZOOM_STEP);
    else if (e.key === "-" || e.key === "_") zoomBy(1 - ZOOM_STEP);
    else if (e.key === "0") resetView();
  };

  // Cursor styling
  const [cursorStyle, setCursorStyle] = useState<"grab" | "grabbing" | "default">("grab");
  useEffect(() => {
    setCursorStyle(isPanning ? "grabbing" : "grab");
  }, [isPanning]);

  return (
    <div className="w-full flex flex-col bg-[#111111] border border-[#242424] rounded-lg p-6">
      <div className="flex items-center justify-between mb-4 border-b border-[#242424] pb-3">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-[#f5f2eb]" />
          <span className="text-xs uppercase tracking-widest font-mono text-[#8a8a8a]">Dependency Engine Map</span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => zoomBy(1 - ZOOM_STEP)}
            className="p-1.5 rounded border border-[#242424] bg-[#161616] text-[#8a8a8a] hover:text-[#f2f2f2] hover:border-[#8a8a8a] transition-all"
            title="Zoom out (−)"
            aria-label="Zoom out"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <span className="text-[10px] font-mono text-[#8a8a8a] tabular-nums w-10 text-center" aria-live="polite">
            {Math.round(zoom * 100)}%
          </span>
          <button
            onClick={() => zoomBy(1 + ZOOM_STEP)}
            className="p-1.5 rounded border border-[#242424] bg-[#161616] text-[#8a8a8a] hover:text-[#f2f2f2] hover:border-[#8a8a8a] transition-all"
            title="Zoom in (+)"
            aria-label="Zoom in"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={resetView}
            className="p-1.5 rounded border border-[#242424] bg-[#161616] text-[#8a8a8a] hover:text-[#f2f2f2] hover:border-[#8a8a8a] transition-all ml-1"
            title="Reset view (0)"
            aria-label="Reset view"
          >
            <Maximize className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      <div
        className="relative overflow-hidden rounded border border-[#1a1a1a]"
        style={{ height: 560 }}
        tabIndex={0}
        onKeyDown={handleKeyDown}
        role="group"
        aria-label="Dependency engine map. Use plus and minus to zoom, zero to reset. Tab to focus concept nodes, Enter or Space to open."
      >
        <span className="sr-only">
          Interactive dependency graph of {nodes.length} browser engineering concepts.
          Each node is a button that opens the concept page. Hover or focus a node to highlight its prerequisites and dependents.
        </span>
        <svg
          ref={svgRef}
          viewBox="0 0 800 960"
          className="w-full h-full select-none"
          style={{ cursor: cursorStyle, touchAction: "none" }}
          onWheel={handleWheel}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerLeave={onPointerUp}
          role="presentation"
          aria-hidden="true"
        >
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX={26} refY={5} markerWidth={7} markerHeight={7} orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#242424" />
            </marker>
            <marker id="arrow-active" viewBox="0 0 10 10" refX={26} refY={5} markerWidth={7} markerHeight={7} orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#f5f2eb" />
            </marker>
          </defs>

          <g transform={`translate(${pan.x} ${pan.y}) scale(${zoom})`}>
            {/* Connection lines */}
            {connections.map(conn => {
              const highlight = getLineHighlight(conn.from.id, conn.to.id);
              let strokeColor = "#242424";
              let strokeWidth = 1.6;
              let classVal = "";

              if (highlight === "outgoing") {
                strokeColor = "#f5f2eb";
                strokeWidth = 2.2;
                classVal = "dependency-line";
              } else if (highlight === "incoming") {
                strokeColor = "#8a8a8a";
                strokeWidth = 2.2;
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
                  vectorEffect="non-scaling-stroke"
                  markerEnd={highlight === "outgoing" || highlight === "incoming" ? "url(#arrow-active)" : "url(#arrow)"}
                />
              );
            })}

            {/* Nodes */}
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
                strokeWidth = 1.6;
              } else if (status === "dependent") {
                borderColor = "#f5f2eb";
                textColor = "#f2f2f2";
                strokeWidth = 1.6;
              } else if (status === "normal") {
                textColor = "#f2f2f2";
              }

              return (
                <g
                  key={node.id}
                  style={{ cursor: "pointer" }}
                  onClick={(e) => {
                    // Only fire concept selection if the user didn't pan to this node.
                    e.stopPropagation();
                    if (!panStart.current.moved) onSelectConcept(node.id);
                  }}
                  onMouseEnter={() => setHoveredNodeId(node.id)}
                  onMouseLeave={() => setHoveredNodeId(null)}
                >
                  <rect
                    x={node.x - 130}
                    y={node.y - 28}
                    width={260}
                    height={56}
                    rx={8}
                    fill={bgColor}
                    stroke={borderColor}
                    strokeWidth={strokeWidth}
                    vectorEffect="non-scaling-stroke"
                    className="transition-all duration-200"
                  />
                  <text
                    x={node.x}
                    y={node.y + 5.5}
                    textAnchor="middle"
                    className="font-mono font-semibold"
                    style={{ fontSize: "16px", userSelect: "none" }}
                    fill={textColor}
                  >
                    {node.title}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>

        {/* Hint footer */}
        <div className="absolute bottom-2 right-3 text-[10px] font-mono text-[#5a5a5a] pointer-events-none">
          scroll = zoom • drag = pan
        </div>

        {/* Keyboard/screen-reader accessible list of concept nodes */}
        <ul className="sr-only">
          {nodes.map(node => (
            <li key={node.id}>
              <button
                type="button"
                onClick={() => onSelectConcept(node.id)}
                onFocus={() => setHoveredNodeId(node.id)}
                onBlur={() => setHoveredNodeId(null)}
                aria-label={`Open concept: ${node.title}${node.requires.length > 0 ? `. Requires: ${node.requires.join(", ")}.` : ""
                  }${node.used_by.length > 0 ? ` Used by: ${node.used_by.join(", ")}.` : ""}`}
              >
                {node.title}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
