# HPF Evaluation Harness v2 — Blind eval set generation + scoring
#
# Usage:
#   python evaluation/harness.py --list
#   python evaluation/harness.py --run hpf rag
#   python evaluation/harness.py --run hpf gemini
#   python evaluation/harness.py --run hpf gpt claude gemini rag

import csv, json, os, random, sys, time, yaml
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))

SCORING_RUBRIC = {
    "technical_correctness": {"weight": 30, "description": "Are the facts accurate?"},
    "completeness": {"weight": 20, "description": "Does it cover what matters?"},
    "reasoning_quality": {"weight": 20, "description": "Are claims supported by evidence?"},
    "actionability": {"weight": 15, "description": "Can the reader act on this?"},
    "clarity": {"weight": 10, "description": "Is it well-structured and clear?"},
    "hallucination_penalty": {"weight": 5, "description": "Penalty for fabrications"},
}

FAILURE_REASONS = [
    "KnowledgeGap", "Retrieval", "Reasoning", "Evidence",
    "Rendering", "Hallucination", "ModelKnowledge", "EvaluatorDisagreement",
]


def load_benchmark(path=None):
    if path is None:
        path = HERE / "benchmark_v1.yaml"
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_providers(names=None, domain_dir=None):
    from evaluation.providers import HPFProvider
    from evaluation.providers.rag_provider import RAGProvider
    from evaluation.providers.openai_compatible import OpenAICompatibleProvider

    # Gemini
    import os as _os
    google_key = _os.environ.get("GOOGLE_API_KEY", "")
    mistral_key = _os.environ.get("MISTRAL_API_KEY", "")

    all_providers = {
        "hpf": HPFProvider(domain_dir or str(HERE.parent)),
        "rag": RAGProvider(domain_dir or str(HERE.parent)),
    }

    if google_key:
        # Gemini OpenAI-compatible endpoint
        all_providers["gemini"] = OpenAICompatibleProvider(
            "Gemini", "GOOGLE_API_KEY", "gemini-2.0-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )

    if mistral_key:
        all_providers["mistral"] = OpenAICompatibleProvider(
            "Mistral", "MISTRAL_API_KEY", "mistral-small-latest",
            base_url="https://api.mistral.ai/v1"
        )

    if names:
        return {k: v for k, v in all_providers.items() if k in names}
    return all_providers


def generate_blind_eval(questions, providers, output_dir):
    blind_dir = Path(output_dir) / "blind"
    blind_dir.mkdir(parents=True, exist_ok=True)
    meta_dir = Path(output_dir) / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)

    labels = list(providers.keys())

    for q in questions:
        qid = q["id"]
        shuffled = labels[:]
        random.shuffle(shuffled)

        meta = {"qid": qid, "mode": q["mode"], "question": q["question"], "answers": {}}
        blind_parts = [f"# Question: {q['question']}\n", f"Mode: {q['mode']}\n"]

        for i, label in enumerate(shuffled):
            letter = chr(65 + i)
            answer, trace = providers[label].answer(q["question"])
            answer_text = answer if isinstance(answer, str) else str(answer)

            meta["answers"][letter] = {"provider": label, "trace": trace}
            blind_parts.append(f"\n=== Answer {letter} ===\n")
            blind_parts.append(answer_text)

        with open(blind_dir / f"{qid}.md", "w") as f:
            f.writelines(blind_parts)
        with open(meta_dir / f"{qid}.json", "w") as f:
            json.dump(meta, f, indent=2)

    return blind_dir, meta_dir


DEFAULT_DOMAIN = str(Path(__file__).parent.parent.parent / "domain-browser-automation")


def run_benchmark(provider_names=None, output_dir=None, domain_dir=None):
    benchmark = load_benchmark()
    questions = benchmark["questions"]

    if output_dir is None:
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir = HERE / "runs" / run_id
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if domain_dir is None:
        if Path(DEFAULT_DOMAIN).is_dir():
            domain_dir = DEFAULT_DOMAIN
        else:
            domain_dir = str(HERE.parent)
    providers = load_providers(names=provider_names, domain_dir=domain_dir)
    print(f"Running: {list(providers.keys())}")
    print(f"Questions: {len(questions)}")
    print(f"Output: {output_dir}\n")

    results = []
    for q in questions:
        print(f"  {q['id']}: {q['question'][:55]}...")

        for name, provider in providers.items():
            t0 = time.time()
            answer, trace = provider.answer(q["question"])
            elapsed = time.time() - t0
            answer_text = answer if isinstance(answer, str) else str(answer)

            results.append({
                "qid": q["id"],
                "mode": q["mode"],
                "provider": name,
                "answer_length": len(answer_text),
                "time_seconds": round(elapsed, 2),
                "failure_reason": None,
                "trace": trace,
            })

    with open(output_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    blind_dir, meta_dir = generate_blind_eval(questions, providers, output_dir)
    print(f"\nBlind eval sets: {blind_dir}")
    print(f"Metadata: {meta_dir}")
    print(f"Results: {output_dir / 'results.json'}")

    return results


def list_questions():
    benchmark = load_benchmark()
    print(f"{benchmark['benchmark']['name']} (frozen {benchmark['benchmark']['frozen']})")
    print(f"Failure reasons: {', '.join(benchmark['benchmark']['failure_reasons'])}\n")
    for q in benchmark["questions"]:
        print(f"  {q['id']:6s} [{q['mode']:13s}] {q['question']}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List questions")
    parser.add_argument("--run", nargs="+", help="Providers to run (hpf, rag, gemini, mistral)")
    parser.add_argument("--run-id", type=str, help="Run ID")
    args = parser.parse_args()

    if args.list:
        list_questions()
    else:
        run_benchmark(
            provider_names=args.run if args.run else ["hpf"],
            output_dir=HERE / "runs" / (f"run_{args.run_id}" if args.run_id else None)
        )
