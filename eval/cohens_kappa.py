"""
Cohen's kappa for PawPal+ judge validation.

Computes inter-rater agreement between two binary label sets on the SAME items:
  - rater 1 : human labels      (eval/human_labels.jsonl)
  - rater 2 : LLM judge labels   (eval/judge_labels_llm.jsonl)

Both files are jsonl with objects {"id": ..., "grounded": 0|1}. Items are
matched by id; only ids present in both files are scored.

Formula (Cohen 1960):
    kappa = (Po - Pe) / (1 - Pe)
where Po is observed agreement and Pe is expected (chance) agreement computed
from each rater's marginal label frequencies. Implemented from scratch (no
sklearn) so the repo has no extra dependency and the math is auditable.

Usage:
    python -m eval.cohens_kappa \
        --human eval/human_labels.jsonl \
        --judge eval/judge_labels_llm.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def load_labels(path: Path) -> Dict[str, int]:
    labels: Dict[str, int] = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("grounded") is None:
                continue  # unlabeled row — skip
            labels[obj["id"]] = int(obj["grounded"])
    return labels


def cohens_kappa(rater1: List[int], rater2: List[int]) -> Tuple[float, Dict]:
    """Return (kappa, details) for two equal-length binary label lists."""
    if len(rater1) != len(rater2):
        raise ValueError("rater label lists must be the same length")
    n = len(rater1)
    if n == 0:
        raise ValueError("no overlapping labeled items to compare")

    # observed agreement
    agree = sum(1 for a, b in zip(rater1, rater2) if a == b)
    po = agree / n

    # chance agreement from marginals (binary: classes 0 and 1)
    pe = 0.0
    for cls in (0, 1):
        p1 = sum(1 for x in rater1 if x == cls) / n
        p2 = sum(1 for x in rater2 if x == cls) / n
        pe += p1 * p2

    if abs(1.0 - pe) < 1e-12:
        # Degenerate: both raters used a single class for everything.
        # kappa is undefined; report po and flag it.
        kappa = float("nan")
    else:
        kappa = (po - pe) / (1.0 - pe)

    # 2x2 confusion (rater1 row, rater2 col)
    confusion = {(i, j): 0 for i in (0, 1) for j in (0, 1)}
    for a, b in zip(rater1, rater2):
        confusion[(a, b)] += 1

    details = {
        "n": n,
        "observed_agreement": round(po, 4),
        "expected_agreement": round(pe, 4),
        "confusion": {f"h{ i }_j{ j }": confusion[(i, j)] for (i, j) in confusion},
        "interpretation": interpret_kappa(kappa),
    }
    return kappa, details


def interpret_kappa(kappa: float) -> str:
    """Landis & Koch (1977) bands."""
    if kappa != kappa:  # NaN
        return "undefined (no label variance)"
    if kappa < 0:
        return "less than chance agreement"
    if kappa <= 0.20:
        return "slight"
    if kappa <= 0.40:
        return "fair"
    if kappa <= 0.60:
        return "moderate"
    if kappa <= 0.80:
        return "substantial"
    return "almost perfect"


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Cohen's kappa between human and judge labels.")
    ap.add_argument("--human", default=str(here / "human_labels.jsonl"))
    ap.add_argument("--judge", default=str(here / "judge_labels_llm.jsonl"))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    human = load_labels(Path(args.human))
    judge = load_labels(Path(args.judge))

    shared_ids = sorted(set(human) & set(judge))
    if not shared_ids:
        raise SystemExit("No overlapping labeled ids between the two files.")

    r1 = [human[i] for i in shared_ids]
    r2 = [judge[i] for i in shared_ids]
    kappa, details = cohens_kappa(r1, r2)

    print("=" * 52)
    print("Cohen's kappa : human (rater 1) vs LLM judge (rater 2)")
    print("=" * 52)
    print(f"  items compared      : {details['n']}")
    print(f"  observed agreement  : {details['observed_agreement']:.3f}")
    print(f"  expected (chance)   : {details['expected_agreement']:.3f}")
    kappa_str = "undefined" if kappa != kappa else f"{kappa:.3f}"
    print(f"  Cohen's kappa       : {kappa_str}")
    print(f"  interpretation      : {details['interpretation']}")
    print(f"  target              : kappa >= 0.60 "
          + ("(MET)" if (kappa == kappa and kappa >= 0.60) else "(not met)"))
    print("-" * 52)
    c = details["confusion"]
    print("  confusion (rows=human, cols=judge):")
    print(f"            judge=0   judge=1")
    print(f"  human=0   {c['h0_j0']:>7}   {c['h0_j1']:>7}")
    print(f"  human=1   {c['h1_j0']:>7}   {c['h1_j1']:>7}")
    print("-" * 52)
    disagreements = [i for i in shared_ids if human[i] != judge[i]]
    if disagreements:
        print(f"  disagreements on: {', '.join(disagreements)}")
    else:
        print("  no disagreements")

    if args.out:
        report = {"kappa": None if kappa != kappa else round(kappa, 4),
                  "details": details, "disagreements": disagreements}
        json.dump(report, open(args.out, "w"), indent=2)


if __name__ == "__main__":
    main()
