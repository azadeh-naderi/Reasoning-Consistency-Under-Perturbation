"""
Run perturbation-based consistency experiments.

Pipeline:
1) Load task_set.json
2) Generate perturbed variants per item
3) Query LLM for each variant
4) Parse JSON responses
5) Compute stability metrics
6) Save raw logs + summary results
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, List

from openai import OpenAI

from perturbations import all_perturbations
from evaluation import extract_json, stability_score, exact_match, numeric_close

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a careful reasoning assistant.
Return your response in JSON with keys:
- final_answer
- rationale (brief; do not include private chain-of-thought)
- verification (brief self-check)
Follow the JSON format exactly.
""".strip()


def llm_call(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.2, max_tokens: int = 600) -> str:
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return resp.choices[0].message.content or ""


def generate_variants(base_prompt: str, perturbation_fns: Dict[str, Any]) -> List[Dict[str, str]]:
    variants = [{"name": "original", "text": base_prompt}]
    for group_name, fn in perturbation_fns.items():
        for i, v in enumerate(fn(base_prompt), start=1):
            variants.append({"name": f"{group_name}_{i}", "text": v})
    return variants


def evaluate_item(item: Dict[str, Any], model: str) -> Dict[str, Any]:
    perts = all_perturbations()
    variants = generate_variants(item["prompt"], perts)

    raw_rows = []
    final_answers = []

    for v in variants:
        raw = llm_call(v["text"], model=model)
        parsed = extract_json(raw)
        fa = parsed.get("final_answer")
        final_answers.append(fa)

        raw_rows.append({
            "item_id": item["id"],
            "domain": item.get("domain"),
            "variant": v["name"],
            "prompt": v["text"],
            "raw_text": raw,
            "parsed": parsed
        })

    answer_key = item.get("answer_key")

    # correctness check against answer_key (best-effort)
    correct_flags = []
    for fa in final_answers:
        if isinstance(answer_key, (int, float)):
            close = numeric_close(fa, answer_key, tol=1e-2)
            correct_flags.append(bool(close) if close is not None else False)
        else:
            correct_flags.append(exact_match(fa, answer_key))

    summary = {
        "item_id": item["id"],
        "domain": item.get("domain"),
        "answer_key": answer_key,
        "n_variants": len(variants),
        "stability_majority": stability_score(final_answers, reference=None),
        "stability_vs_key": stability_score(final_answers, reference=answer_key),
        "accuracy_over_variants": sum(1 for c in correct_flags if c) / len(correct_flags)
    }

    return {"summary": summary, "rows": raw_rows}


def main():
    repo = Path(__file__).resolve().parents[1]
    tasks_path = repo / "prompts" / "task_set.json"

    with open(tasks_path, "r", encoding="utf-8") as f:
        taskset = json.load(f)

    model = os.getenv("MODEL_NAME", "gpt-4o-mini")
    out_dir = repo / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_rows = []
    all_summaries = []

    ts = int(time.time())
    for item in taskset["items"]:
        out = evaluate_item(item, model=model)
        all_summaries.append(out["summary"])
        all_rows.extend(out["rows"])

    raw_path = out_dir / f"raw_runs_{model}_{ts}.jsonl"
    with open(raw_path, "w", encoding="utf-8") as f:
        for r in all_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary_path = out_dir / f"summary_{model}_{ts}.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_summaries, f, indent=2, ensure_ascii=False)

    print(f"Saved raw: {raw_path}")
    print(f"Saved summary: {summary_path}")


if __name__ == "__main__":
    main()
