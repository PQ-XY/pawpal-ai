"""
Build the human labeling sheet for groundedness judging.

For each case it writes:
  - eval/labeling_sheet.md     : human-readable. For each plan: the retrieved
                                 context and the plan's tasks+rationales, so you
                                 can decide grounded (1) or not (0) by reading.
  - eval/human_labels.jsonl    : one row per case with "grounded": null for you
                                 to fill in. Edit each null to 0 or 1.

This keeps your human labels INDEPENDENT of the judge: the sheet shows you the
evidence, not the judge's verdict, so the Cohen's kappa you compute later is a
real agreement measurement, not a copy.

Run against whatever plans you intend to judge (default: Gemini path needs a
key; falls back to deterministic plans if no key, which is fine for dry-running
the workflow).

Usage:
    python -m eval.build_labeling_sheet --golden eval/golden.jsonl --n 20
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_agent import CatProfile, CatTaskPlanningAgent  # noqa: E402
from knowledge_retriever import KnowledgeRetriever  # noqa: E402
from eval.context_recall import retrieved_context_text  # noqa: E402


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", default=str(here / "golden.jsonl"))
    ap.add_argument("--n", type=int, default=20, help="How many cases to include.")
    ap.add_argument("--retriever", choices=["exact", "embedding"], default="exact")
    ap.add_argument("--sheet", default=str(here / "labeling_sheet.md"))
    ap.add_argument("--labels", default=str(here / "human_labels.jsonl"))
    args = ap.parse_args()

    cases = [json.loads(l) for l in open(args.golden, encoding="utf-8") if l.strip()][: args.n]

    kb = str(REPO_ROOT / "knowledge_base")
    retriever = (
        __import__("embedding_retriever").EmbeddingKnowledgeRetriever(knowledge_base_path=kb)
        if args.retriever == "embedding"
        else KnowledgeRetriever(knowledge_base_path=kb)
    )
    agent = CatTaskPlanningAgent(knowledge_retriever=retriever)

    sheet_lines = [
        "# Groundedness labeling sheet",
        "",
        "For each plan, decide: are the plan's tasks/advice supported by the",
        "RETRIEVED CONTEXT? Mark **1 = grounded** or **0 = not grounded** in",
        "`human_labels.jsonl`. Judge independently — do not run the LLM judge first.",
        "",
        "---",
        "",
    ]
    label_rows = []

    for case in cases:
        inp = case["input"]
        profile = CatProfile(
            name=inp["name"], breed=inp["breed"], age_years=inp["age_years"],
            health_conditions=inp.get("health_conditions") or None,
            preferences=inp.get("preferences") or None,
        )
        try:
            result = agent.create_plan(profile)
            plan = result.get("plan", {})
            context = retrieved_context_text(result.get("knowledge", {}))
            source = result.get("source")
        except Exception as exc:
            plan, context, source = {}, f"(plan errored: {exc})", "error"

        sheet_lines.append(f"## {case['id']}  — {inp['name']} ({inp['breed']}, {inp['age_years']}y)")
        conds = inp.get("health_conditions") or []
        sheet_lines.append(f"*Conditions:* {', '.join(conds) if conds else 'none'}  |  *plan source:* {source}")
        sheet_lines.append("")
        sheet_lines.append("**Retrieved context:**")
        sheet_lines.append(f"> {context[:600]}{'...' if len(context) > 600 else ''}")
        sheet_lines.append("")
        sheet_lines.append("**Plan tasks:**")
        for t in plan.get("suggested_tasks", []):
            sheet_lines.append(f"- `{t.get('task_type')}` — {t.get('rationale','')}")
        sheet_lines.append("")
        sheet_lines.append(f"**Your label for {case['id']}:** ___ (1 grounded / 0 not)")
        sheet_lines.append("")
        sheet_lines.append("---")
        sheet_lines.append("")

        label_rows.append({"id": case["id"], "grounded": None})

    Path(args.sheet).write_text("\n".join(sheet_lines), encoding="utf-8")
    with open(args.labels, "w", encoding="utf-8") as fh:
        for row in label_rows:
            fh.write(json.dumps(row) + "\n")

    print(f"Wrote labeling sheet -> {args.sheet}")
    print(f"Wrote blank human labels ({len(label_rows)} rows, grounded=null) -> {args.labels}")
    print("Next: read the sheet, set each 'grounded' to 0 or 1 in the labels file.")


if __name__ == "__main__":
    main()
