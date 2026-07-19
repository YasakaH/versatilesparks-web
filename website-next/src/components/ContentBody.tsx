import React from "react";

interface ContentBodyProps {
    body: string;
    className?: string;
}

/**
 * ContentBody — shared renderer for the `body` markdown field stored on
 * concepts, recipes, and books in knowledge-base.json. Handles a small,
 * fixed subset of markdown: paragraphs, ### headings, ordered lists, and
 * ``` fenced code blocks. Anything richer should go through a real MDX
 * pipeline; this keeps the static-export bundle tiny and dependency-free.
 */
export default function ContentBody({ body, className = "" }: ContentBodyProps) {
    const paragraphs = body.split("\n\n");
    return (
        <div className={`prose prose-invert max-w-none text-[#8a8a8a] leading-relaxed text-sm md:text-md space-y-4 font-sans py-4 border-t border-[#242424] ${className}`}>
            {paragraphs.map((para: string, idx: number) => {
                if (para.startsWith("```")) {
                    const code = para.replace(/```python|```/g, "").trim();
                    return (
                        <pre key={idx} className="bg-[#111111] border border-[#242424] p-4 rounded text-xs font-mono text-[#f2f2f2] overflow-x-auto my-4">
                            <code>{code}</code>
                        </pre>
                    );
                }
                if (para.startsWith("###")) {
                    return (
                        <h3 key={idx} className="text-lg font-bold text-[#f2f2f2] mt-6 mb-2 font-mono">
                            {para.replace(/^###\s*/, "").trim()}
                        </h3>
                    );
                }
                if (/^\d+\.\s/.test(para)) {
                    return (
                        <ol key={idx} className="list-decimal pl-5 space-y-2">
                            {para.split("\n").map((li: string, lidx: number) => (
                                <li key={lidx}>{li.replace(/^\d+\.\s*/, "")}</li>
                            ))}
                        </ol>
                    );
                }
                return <p key={idx}>{para}</p>;
            })}
        </div>
    );
}