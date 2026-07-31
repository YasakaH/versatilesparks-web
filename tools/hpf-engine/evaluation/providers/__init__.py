# Answer providers for HPF evaluation harness

import abc
import os
import sys


class AnswerProvider(abc.ABC):
    @abc.abstractmethod
    def answer(self, question: str) -> str:
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__.replace("Provider", "")


class HPFProvider(AnswerProvider):
    def __init__(self, domain_dir: str):
        self.domain_dir = domain_dir
        self._objects = None

    def _ensure_path(self):
        p = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        if p not in sys.path:
            sys.path.insert(0, p)

    def _load_objects(self):
        if self._objects is None:
            self._ensure_path()
            from hpf.retriever import load_domain
            self._objects = load_domain(self.domain_dir)
        return self._objects

    def answer(self, question: str) -> str:
        self._ensure_path()
        from hpf.question_analyzer import analyze
        from hpf.retriever import retrieve
        from hpf.evidence_builder import build
        from hpf.renderer import render

        analysis = analyze(question)
        objects = self._load_objects()
        candidates = retrieve(analysis["entities"], objects)
        argument, actual_mode = build(analysis["mode"], candidates, question)
        output = render(actual_mode, argument)

        trace = {
            "question": question,
            "mode": analysis["mode"],
            "entities": analysis["entities"],
            "retrieved": [o["id"] for o in candidates[:5]],
            "argument_keys": list(argument.keys()),
        }

        return output, trace
