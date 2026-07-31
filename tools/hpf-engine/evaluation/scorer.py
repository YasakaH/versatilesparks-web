# Dual-judge auto-scorer
# Runs two independent LLM judges (Mistral Small + NVIDIA Llama) on blind eval sets.
# Each judge outputs numeric scores + winner + rationale. Results are averaged.
# Disagreements flagged for manual review.

import json, os, sys, time, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

# Load .env from hermes dir
_env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
if os.path.isfile(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

SCORING_PROMPT = """Evaluate two answers to a browser automation question. Return ONLY valid JSON.

Score each answer 0-10 per criterion (hallucination_penalty is 0-5, where 5 = no hallucination):
- technical_correctness: Are the facts accurate? (weight 30)
- completeness: Does it cover what matters? (weight 20)
- reasoning_quality: Are claims supported? (weight 20)
- actionability: Can the reader act? (weight 15)
- clarity: Is it well-structured? (weight 10)
- hallucination_penalty: 5 = no hallucination, 0 = completely fabricated (weight 5)

Also pick a winner ("A", "B", or "Tie") and a one-sentence rationale.

JSON format:
{{"scores":{{"A":{{"technical_correctness":N,"completeness":N,"reasoning_quality":N,"actionability":N,"clarity":N,"hallucination_penalty":N}},"B":{{"technical_correctness":N,"completeness":N,"reasoning_quality":N,"actionability":N,"clarity":N,"hallucination_penalty":N}}}},"winner":"A|B|Tie","rationale":"one sentence explaining why"}}

Question: {question}
Mode: {mode}

=== Answer A ===
{answer_a}

=== Answer B ===
{answer_b}
"""


# Model configs
JUDGES = [
    {
        "name": "mistral",
        "api_key": os.environ.get("MISTRAL_API_KEY", ""),
        "url": "https://api.mistral.ai/v1/chat/completions",
        "model": "mistral-small-latest",
    },
    {
        "name": "llama",
        "api_key": os.environ.get("NVIDIA_API_KEY", ""),
        "url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "meta/llama-3.1-8b-instruct",
    },
]


def call_model(prompt, config):
    payload = json.dumps({
        "model": config["model"],
        "messages": [
            {"role": "system", "content": "You output only JSON."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 600,
    }).encode("utf-8")
    headers = {"Authorization": "Bearer " + config["api_key"], "Content-Type": "application/json"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(config["url"], data=payload, headers=headers)
            resp = urllib.request.urlopen(req, timeout=60)
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue
            return None
        except Exception:
            return None
    return None


def parse_verdict(text):
    """Parse JSON from model output. Expects {'scores': {...}, 'winner': str, 'rationale': str}."""
    if not text:
        return None
    text = re.sub(r"<thought>.*?(</thought>|$)", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]*>", "", text)
    for candidate in _extract_json(text):
        try:
            d = json.loads(candidate)
            if "scores" in d and "winner" in d:
                return d
        except json.JSONDecodeError:
            continue
    return None


def _extract_json(text):
    candidates = []
    depth = 0
    start = -1
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start >= 0:
                candidates.append(text[start:i+1])
                start = -1
    return list(reversed(candidates))


def compute_total(scores):
    weights = {"technical_correctness": 30, "completeness": 20, "reasoning_quality": 20,
               "actionability": 15, "clarity": 10, "hallucination_penalty": 5}
    total = 0
    for k, w in weights.items():
        v = scores.get(k, 0)
        total += (v / 10.0) * w if k != "hallucination_penalty" else v
    return round(total, 1)


def average_scores(score_list):
    """Average numeric scores from multiple judges."""
    if not score_list:
        return None
    keys = ["technical_correctness", "completeness", "reasoning_quality",
            "actionability", "clarity", "hallucination_penalty"]
    result = {}
    for k in keys:
        vals = [s.get(k, 0) for s in score_list]
        result[k] = round(sum(vals) / len(vals), 1)
    return result


def score_run(run_dir):
    blind_dir = os.path.join(run_dir, "blind")
    meta_dir = os.path.join(run_dir, "meta")
    files = sorted(f for f in os.listdir(blind_dir) if f.endswith(".md"))

    # Filter judges with API keys
    active_judges = [j for j in JUDGES if j["api_key"]]
    if not active_judges:
        print("ERROR: No judges configured. Set MISTRAL_API_KEY and/or NVIDIA_API_KEY.")
        return

    print(f"Judges: {', '.join(j['name'] for j in active_judges)}")
    print(f"Eval sets: {len(files)}\n")

    results = []
    disagreements = []

    for fname in files:
        qid = fname.replace(".md", "")
        blind = open(os.path.join(blind_dir, fname)).read()
        meta = json.load(open(os.path.join(meta_dir, f"{qid}.json")))

        parts = blind.split("=== Answer ")
        if len(parts) < 3:
            print(f"  {qid}: SKIP (bad format)")
            continue

        header = parts[0].strip()
        q_lines = [l for l in header.split("\n") if l.startswith("# Question:")]
        question = q_lines[0].replace("# Question:", "").strip() if q_lines else qid
        mode_lines = [l for l in header.split("\n") if l.startswith("Mode:")]
        mode = mode_lines[0].replace("Mode:", "").strip() if mode_lines else "?"

        answer_texts = {}
        for i in [1, 2]:
            block = parts[i]
            answer_texts[block[0]] = block[2:].strip()

        if len(answer_texts) < 2:
            print(f"  {qid}: SKIP (<2 answers)")
            continue

        provider_map = {l: info["provider"] for l, info in meta["answers"].items()}
        prompt = SCORING_PROMPT.format(
            question=question, mode=mode,
            answer_a=answer_texts["A"][:1000],
            answer_b=answer_texts["B"][:1000],
        )

        # Collect verdicts from all judges
        verdicts = []
        for judge in active_judges:
            raw = call_model(prompt, judge)
            v = parse_verdict(raw)
            verdicts.append({"judge": judge["name"], "raw": raw, "parsed": v})
            if not v:
                print(f"  {qid}: {judge['name']} PARSE FAIL")

        # Extract per-letter scores from each judge
        a_scores = [v["parsed"]["scores"]["A"] for v in verdicts if v["parsed"]]
        b_scores = [v["parsed"]["scores"]["B"] for v in verdicts if v["parsed"]]
        winners = [v["parsed"]["winner"] for v in verdicts if v["parsed"]]
        rationales = [v["parsed"]["rationale"] for v in verdicts if v["parsed"]]

        # Average across judges
        avg_a = average_scores(a_scores) if a_scores else None
        avg_b = average_scores(b_scores) if b_scores else None

        # Consensus winner
        hpf_letter = next((l for l, p in provider_map.items() if p == "hpf"), None)
        rag_letter = next((l for l, p in provider_map.items() if p == "rag"), None)

        hpf_total = compute_total(avg_a) if avg_a and provider_map.get("A") == "hpf" else \
                    compute_total(avg_b) if avg_b and provider_map.get("B") == "hpf" else 0
        rag_total = compute_total(avg_a) if avg_a and provider_map.get("A") == "rag" else \
                    compute_total(avg_b) if avg_b and provider_map.get("B") == "rag" else 0

        unique_winners = list(set(winners)) if winners else []
        consensus = unique_winners[0] if len(unique_winners) == 1 else "DISAGREEMENT"

        if consensus == "DISAGREEMENT":
            disagreements.append(qid)

        row = {
            "qid": qid, "mode": mode, "question": question,
            "hpf_total": hpf_total, "rag_total": rag_total,
            "consensus_winner": consensus,
            "judges": [
                {
                    "judge": v["judge"],
                    "parsed": v["parsed"],
                } for v in verdicts
            ],
        }

        status = f"HPF={hpf_total:.0f} RAG={rag_total:.0f}"
        if consensus == "DISAGREEMENT":
            status += " DISAGREE"
            print(f"  {qid}: {status}")
        else:
            status += f" ({consensus})"
            print(f"  {qid}: {status}")

        results.append(row)

    return results, disagreements


if __name__ == "__main__":
    run_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "runs/run_002")
    results, disagreements = score_run(run_dir)

    out_path = os.path.join(run_dir, "scores.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    hpf_total = sum(r["hpf_total"] for r in results)
    rag_total = sum(r["rag_total"] for r in results)
    hpf_wins = 0
    rag_wins = 0
    ties = 0
    dis = 0
    for r in results:
        if r["consensus_winner"] == "DISAGREEMENT":
            dis += 1
        elif r["hpf_total"] > r["rag_total"]:
            hpf_wins += 1
        elif r["rag_total"] > r["hpf_total"]:
            rag_wins += 1
        else:
            ties += 1

    print(f"\n=== Summary ===")
    print(f"  HPF: {hpf_total:.0f} total ({hpf_total/len(results):.1f}/q), {hpf_wins} wins")
    print(f"  RAG: {rag_total:.0f} total ({rag_total/len(results):.1f}/q), {rag_wins} wins")
    print(f"  Ties: {ties}  Disagreements: {dis}")
    if disagreements:
        print(f"  Flagged for review: {', '.join(disagreements)}")
    print(f"\nScores saved to: {out_path}")
