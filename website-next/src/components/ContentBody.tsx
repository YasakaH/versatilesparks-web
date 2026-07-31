import React from "react";

interface ContentBodyProps {
    body: string;
    className?: string;
}

const INLINE_RE = /(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))/g;

function renderInline(text: string, keyBase: string) {
    const parts = text.split(INLINE_RE).filter((p) => p !== "");
    return parts.map((part, i) => {
        if (part.startsWith("**") && part.endsWith("**")) {
            return (
                <strong key={`${keyBase}-${i}`} className="text-[#f2f2f2]">
                    {part.slice(2, -2)}
                </strong>
            );
        }
        if (part.startsWith("`") && part.endsWith("`")) {
            return (
                <code key={`${keyBase}-${i}`} className="bg-[#111111] border border-[#242424] px-1.5 py-0.5 rounded text-xs font-mono text-[#f2f2f2]">
                    {part.slice(1, -1)}
                </code>
            );
        }
        const link = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
        if (link) {
            return (
                <a
                    key={`${keyBase}-${i}`}
                    href={link[2]}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[#7aa2f7] underline underline-offset-2 hover:text-[#9bb8f8]"
                >
                    {link[1]}
                </a>
            );
        }
        return <span key={`${keyBase}-${i}`}>{part}</span>;
    });
}

/**
 * ContentBody — shared renderer for the `body` markdown field stored on
 * concepts, recipes, books, and articles in knowledge-base.json. Handles a
 * small, fixed subset of markdown: paragraphs, ##/### headings, **bold**,
 * `inline code`, [links](url), --- rules, ordered and unordered lists, and
 * ``` fenced code blocks. Anything richer should go through a real MDX
 * pipeline; this keeps the static-export bundle tiny and dependency-free.
 */
export default function ContentBody({ body, className = "" }: ContentBodyProps) {
    const paragraphs = body.split("\n\n");
    return (
        <div className={`prose prose-invert max-w-none text-[#8a8a8a] leading-relaxed text-sm md:text-md space-y-4 font-sans py-4 border-t border-[#242424] ${className}`}>
            {paragraphs.map((para: string, idx: number) => {
                if (para.trim() === "---") {
                    return <hr key={idx} className="border-[#242424] my-4" />;
                }
                if (para.startsWith("```")) {
                    const code = para.replace(/```python|```/g, "").trim();
                    return (
                        <pre key={idx} className="bg-[#111111] border border-[#242424] p-4 rounded text-xs font-mono text-[#f2f2f2] overflow-x-auto my-4">
                            <code>{code}</code>
                        </pre>
                    );
                }
                const heading = para.match(/^(#{2,3})\s+(.+)$/);
                if (heading) {
                    const Tag = heading[1].length === 2 ? "h2" : "h3";
                    return (
                        <Tag key={idx} className="text-lg font-bold text-[#f2f2f2] mt-6 mb-2 font-mono">
                            {renderInline(heading[2], `h-${idx}`)}
                        </Tag>
                    );
                }
                if (/^(\d+\.\s)/m.test(para)) {
                    return (
                        <ol key={idx} className="list-decimal pl-5 space-y-2">
                            {para.split("\n").map((li: string, lidx: number) => (
                                <li key={lidx}>{renderInline(li.replace(/^\d+\.\s*/, ""), `ol-${idx}-${lidx}`)}</li>
                            ))}
                        </ol>
                    );
                }
                if (/^- /.test(para)) {
                    return (
                        <ul key={idx} className="list-disc pl-5 space-y-2">
                            {para.split("\n").map((li: string, lidx: number) => (
                                <li key={lidx}>{renderInline(li.replace(/^- /, ""), `ul-${idx}-${lidx}`)}</li>
                            ))}
                        </ul>
                    );
                }
                return <p key={idx}>{renderInline(para, `p-${idx}`)}</p>;
            })}
        </div>
    );
}
