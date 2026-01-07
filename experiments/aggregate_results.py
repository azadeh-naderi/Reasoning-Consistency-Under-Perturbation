"""
Aggregate multiple summary_*.json files into a single report.
"""

import json
from pathlib import Path


def main():
    repo = Path(__file__).resolve().parents[1]
    results_dir = repo / "results"

    summaries = []
    for p in results_dir.glob("summary_*.json"):
        data = json.load(open(p, "r", encoding="utf-8"))
        for row in data:
            row["_file"] = p.name
            summaries.append(row)

    out_path = results_dir / "aggregated_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

    print(f"Saved: {out_path} ({len(summaries)} rows)")


if __name__ == "__main__":
    main()
