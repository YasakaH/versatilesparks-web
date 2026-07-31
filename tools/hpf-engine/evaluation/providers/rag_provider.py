# RAG answer provider — naive baseline using keyword search over knowledge objects
# Uses the knowledge base but WITHOUT structured reasoning

import os
from . import AnswerProvider


class RAGProvider(AnswerProvider):
    def __init__(self, domain_dir: str):
        self.domain_dir = domain_dir
        self._objects = None

    def _load_objects(self):
        if self._objects is None:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
            from hpf.retriever import load_domain
            self._objects = load_domain(self.domain_dir)
        return self._objects

    def answer(self, question: str) -> str:
        objects = self._load_objects()
        q = question.lower()
        relevant = []
        for obj in objects:
            semantic = obj.get("semantic", "").lower()
            if any(word in semantic for word in q.split()):
                relevant.append(obj)

        if not relevant:
            return "No relevant knowledge found.", {"provider": "rag", "objects_consulted": 0}

        result_parts = []
        for obj in relevant[:3]:
            result_parts.append(f"--- {obj['title']} ---")
            result_parts.append(obj.get("semantic", ""))
            result_parts.append("")

        return "\n".join(result_parts), {"provider": "rag", "objects_consulted": len(relevant)}
