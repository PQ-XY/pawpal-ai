"""
Eval runner for PawPal+ cat care planning agent.

Loads the golden set, runs each case through CatTaskPlanningAgent, and scores
three dimensions per case:

  1. task_coverage  - did the plan include the expected task categories?
  2. grounding      - did expected knowledge-base facts surface in the plan text?
  3. forbidden      - did the plan avoid breed-default / unsafe statements that
                      the health condition contraindicates?

The runner is deterministic: with GOOGLE_API_KEY unset the agent uses its
fallback planner, so scores are reproducible offline. Pass --gemini to score
the live Gemini path instead.

Usage:
    python -m eval.run_eval                  # fallback planner (default)
    python -m eval.run_eval --retriever embedding
    python -m eval.run_eval --out eval/results_baseline.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Make the repo root importable whether run as a module or a script.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_agent import CatProfile, CatTaskPlanningAgent  # noqa: E402
from ai_validator import PlanValidator  # noqa: E402
from knowledge_retriever import KnowledgeRetriever  # noqa: E402

GOLDEN_PATH = Path(__file__).resolve().parent / "golden.jsonl"

# Reuse the validator's normalization so "coverage" means the same thing the
# system itself means by it. One shared PlanValidator instance is enough.
_NORMALIZER = PlanValidator()


def normalize_task_type(raw: str) -> str:
    """Map a raw task_type string to its canonical category via the validator."""
    norm = _NORMALIZER._normalize_task_type(raw)  # canonical category or raw
    return norm or ""


# Qualifiers that negate/limit a forbidden phrase, turning "intense exercise"
# (bad) into "limited intense exercise" / "avoid intense exercise" (safe advice).
_NEGATORS = ("limited", "limit", "avoid", "avoids", "avoiding", "no ", "not ",
             "never", "restrict", "restricted", "minimize", "minimise",
             "reduce", "reduced", "less", "without", "prevent", "discourage")


def _forbidden_present(phrase: str, text: str) -> bool:
    """True only if `phrase` appears in `text` WITHOUT a negating qualifier
    immediately preceding it. Looks at the ~25 chars before each match for a
    negator so safe, limiting advice is not counted as a violation."""
    start = 0
    while True:
        i = text.find(phrase, start)
        if i == -1:
            return False
        window = text[max(0, i - 25):i]
        if not any(neg in window for neg in _NEGATORS):
            return True  # an unqualified (true) violation
        start = i + len(phrase)


def load_golden(path: Path = GOLDEN_PATH) -> List[Dict[str, Any]]:
    cases = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def plan_text_blob(plan: Dict[str, Any]) -> str:
    """Flatten all human-readable plan text into one lowercase string for
    grounding / forbidden substring checks."""
    parts: List[str] = [str(plan.get("summary", ""))]
    for task in plan.get("suggested_tasks", []):
        parts.append(str(task.get("description", "")))
        parts.append(str(task.get("rationale", "")))
        parts.append(str(task.get("frequency", "")))
    parts.extend(str(w) for w in plan.get("warnings", []))
    parts.extend(str(s) for s in plan.get("next_steps", []))
    return " ".join(parts).lower()


def score_case(case: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    """Score a single golden case against an agent result."""
    plan = result.get("plan", {})
    tasks = plan.get("suggested_tasks", [])

    # --- task coverage ---
    present_categories = {normalize_task_type(t.get("task_type", "")) for t in tasks}
    present_categories.discard("")
    expected_cov = case["expected_facts"]["task_coverage"]
    covered = [c for c in expected_cov if c in present_categories]
    coverage_score = len(covered) / len(expected_cov) if expected_cov else 1.0

    # --- grounding (expected facts surface in plan text) ---
    blob = plan_text_blob(plan)
    # Also fold in the retrieved knowledge guidelines, since grounding is about
    # whether the right knowledge was retrieved and reflected, not just phrasing.
    knowledge = result.get("knowledge", {})
    guideline_blob = " ".join(str(g) for g in knowledge.get("key_guidelines", [])).lower()
    care_reqs = []
    for hc in knowledge.get("health_conditions", []):
        care_reqs.extend(hc.get("care_requirements", []))
    care_blob = " ".join(str(c) for c in care_reqs).lower()
    full_blob = " ".join([blob, guideline_blob, care_blob])

    expected_ground = case["expected_facts"]["grounding"]
    grounded = [g for g in expected_ground if g.lower() in full_blob]
    grounding_score = len(grounded) / len(expected_ground) if expected_ground else 1.0

    # --- forbidden (should NOT appear) ---
    # Negation-aware: a forbidden phrase preceded by a negating qualifier
    # (e.g. "limited intense exercise", "avoid intense exercise") is SAFE advice,
    # not a violation. A naive substring match would false-positive on these.
    forbidden = case.get("forbidden_facts", [])
    violations = [f for f in forbidden if _forbidden_present(f.lower(), full_blob)]
    forbidden_clean = len(violations) == 0

    # --- combined per-case pass: coverage + grounding thresholds, no violations ---
    passed = coverage_score >= 0.75 and grounding_score >= 0.5 and forbidden_clean

    return {
        "id": case["id"],
        "tags": case["tags"],
        "source": result.get("source"),
        "coverage_score": round(coverage_score, 3),
        "covered": covered,
        "missing_coverage": [c for c in expected_cov if c not in present_categories],
        "grounding_score": round(grounding_score, 3),
        "grounded": grounded,
        "missing_grounding": [g for g in expected_ground if g.lower() not in full_blob],
        "forbidden_violations": violations,
        "passed": passed,
    }


def build_agent(retriever_mode: str) -> CatTaskPlanningAgent:
    kb_path = str(REPO_ROOT / "knowledge_base")
    if retriever_mode == "embedding":
        try:
            from embedding_retriever import EmbeddingKnowledgeRetriever
        except ImportError as exc:  # pragma: no cover
            raise SystemExit(
                "embedding retriever requested but embedding_retriever.py not found "
                f"or its deps are missing: {exc}"
            )
        retriever = EmbeddingKnowledgeRetriever(knowledge_base_path=kb_path)
    else:
        retriever = KnowledgeRetriever(knowledge_base_path=kb_path)
    return CatTaskPlanningAgent(knowledge_retriever=retriever)


def run(retriever_mode: str, out_path: str | None, golden_path: Path = GOLDEN_PATH) -> Dict[str, Any]:
    cases = load_golden(golden_path)
    agent = build_agent(retriever_mode)

    per_case: List[Dict[str, Any]] = []
    for case in cases:
        inp = case["input"]
        profile = CatProfile(
            name=inp["name"],
            breed=inp["breed"],
            age_years=inp["age_years"],
            health_conditions=inp.get("health_conditions") or None,
            preferences=inp.get("preferences") or None,
        )
        try:
            result = agent.create_plan(profile)
            per_case.append(score_case(case, result))
        except Exception as exc:  # a crashing plan is the worst outcome: score 0
            per_case.append(
                {
                    "id": case["id"],
                    "tags": case["tags"],
                    "source": "error",
                    "coverage_score": 0.0,
                    "covered": [],
                    "missing_coverage": case["expected_facts"]["task_coverage"],
                    "grounding_score": 0.0,
                    "grounded": [],
                    "missing_grounding": case["expected_facts"]["grounding"],
                    "forbidden_violations": [],
                    "passed": False,
                    "errored": True,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    n = len(per_case)
    summary = {
        "retriever": retriever_mode,
        "n_cases": n,
        "pass_rate": round(sum(c["passed"] for c in per_case) / n, 3),
        "mean_coverage": round(sum(c["coverage_score"] for c in per_case) / n, 3),
        "mean_grounding": round(sum(c["grounding_score"] for c in per_case) / n, 3),
        "forbidden_violation_cases": [c["id"] for c in per_case if c["forbidden_violations"]],
        "errored_cases": [c["id"] for c in per_case if c.get("errored")],
    }

    report = {"summary": summary, "cases": per_case}

    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PawPal+ golden-set eval.")
    parser.add_argument(
        "--retriever",
        choices=["exact", "embedding"],
        default="exact",
        help="Which retriever to use (exact = baseline, embedding = optimized).",
    )
    parser.add_argument("--out", default=None, help="Optional path to write JSON report.")
    parser.add_argument(
        "--golden",
        default=str(GOLDEN_PATH),
        help="Path to the golden set jsonl (default: eval/golden.jsonl).",
    )
    args = parser.parse_args()

    report = run(args.retriever, args.out, Path(args.golden))
    s = report["summary"]
    print("=" * 60)
    print(f"PawPal+ eval | retriever={s['retriever']} | n={s['n_cases']}")
    print("=" * 60)
    print(f"  pass_rate      : {s['pass_rate']:.3f}")
    print(f"  mean_coverage  : {s['mean_coverage']:.3f}")
    print(f"  mean_grounding : {s['mean_grounding']:.3f}")
    if s["forbidden_violation_cases"]:
        print(f"  forbidden viol.: {', '.join(s['forbidden_violation_cases'])}")
    else:
        print("  forbidden viol.: none")
    print("-" * 60)
    print(f"{'case':<10}{'cov':>6}{'grnd':>7}  {'pass':>5}  missing")
    for c in report["cases"]:
        miss = ",".join(c["missing_coverage"]) or "-"
        flag = "PASS" if c["passed"] else "FAIL"
        print(f"{c['id']:<10}{c['coverage_score']:>6.2f}{c['grounding_score']:>7.2f}  {flag:>5}  {miss}")


if __name__ == "__main__":
    main()
