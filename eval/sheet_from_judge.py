"""
Build a human labeling sheet FROM THE JUDGE'S SAVED OUTPUT.

This guarantees the human (rater 1) labels the exact same plans the LLM judge
(rater 2) scored — a hard requirement for a valid Cohen's kappa. It reads the
judge output file (which now persists each judged plan's tasks + context) and
emits:

  - eval/labeling_sheet.md   : context + plan tasks per case, WITHOUT the
                               judge's verdict (so labeling stays independent)
  - eval/human_labels.jsonl  : one {"id":..., "grounded": null} row per case

Run AFTER the judge:
    python -m eval.judge --golden eval/golden.jsonl --backend llm --out eval/judge_labels_llm.jsonl
    python -m eval.sheet_from_judge --judge eval/judge_labels_llm.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", default=str(here / "judge_labels_llm.jsonl"))
    ap.add_argument("--sheet", default=str(here / "labeling_sheet.md"))
    ap.add_argument("--labels", default=str(here / "human_labels.jsonl"))
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.judge, encoding="utf-8") if l.strip()]

    if rows and "plan_tasks" not in rows[0]:
        raise SystemExit(
            "This judge file has no saved plans. Re-run the patched judge first "
            "so it persists plan_tasks/context, then rebuild the sheet."
        )

    lines = [
        "# Groundedness labeling sheet",
        "",
        "Decide for each plan: are ALL task rationales supported by the RETRIEVED",
        "CONTEXT? Mark **1 = grounded** or **0 = not grounded** in `human_labels.jsonl`.",
        "Label independently — the judge's verdict is intentionally hidden here.",
        "",
        "Rule to apply consistently: a task is ungrounded if its rationale asserts",
        "something not present in the retrieved context, even if it is generally",
        "true cat-care advice (e.g. dental care / vet visits not in the context).",
        "",
        "---",
        "",
    ]
    label_rows = []

    for r in rows:
        inp = r.get("input", {})
        conds = inp.get("health_conditions") or []
        lines.append(f"## {r['id']}  — {inp.get('name','?')} "
                     f"({inp.get('breed','?')}, {inp.get('age_years','?')}y)")
        lines.append(f"*Conditions:* {', '.join(conds) if conds else 'none'}  "
                     f"|  *plan source:* {r.get('source','?')}")
        lines.append("")
        lines.append("**Retrieved context:**")
        ctx = r.get("context", "")
        lines.append(f"> {ctx[:700]}{'...' if len(ctx) > 700 else ''}")
        lines.append("")
        lines.append("**Plan tasks:**")
        for t in r.get("plan_tasks", []):
            lines.append(f"- `{t.get('task_type')}` — {t.get('rationale','')}")
        lines.append("")
        lines.append(f"**Your label for {r['id']}:** ___ (1 grounded / 0 not)")
        lines.append("")
        lines.append("---")
        lines.append("")
        label_rows.append({"id": r["id"], "grounded": None})

    Path(args.sheet).write_text("\n".join(lines), encoding="utf-8")
    with open(args.labels, "w", encoding="utf-8") as fh:
        for row in label_rows:
            fh.write(json.dumps(row) + "\n")

    print(f"Wrote labeling sheet ({len(label_rows)} cases) -> {args.sheet}")
    print(f"Wrote blank human labels -> {args.labels}")
    print("These plans are the EXACT ones the judge scored. Label, then run cohens_kappa.")


if __name__ == "__main__":
    main()
