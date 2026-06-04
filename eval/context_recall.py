"""
Context Recall metric for PawPal+ retrieval evaluation.

Implements the RAGAS context-recall definition:

    context_recall = (reference claims supported by retrieved context)
                     / (total reference claims)

Reference: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/

Mapping onto PawPal+:
  - "reference claims"     -> a golden case's expected_facts.grounding list
                              (the facts a correct plan must be grounded in)
  - "retrieved context"    -> the retriever output for that case:
                              key_guidelines + health care_requirements +
                              recommended_tasks (the text the planner sees)

Claim attribution (is a claim supported by the context?) has two backends:
  1. deterministic (default) -- substring + token-overlap match. Reproducible,
     offline, no API key. This is what the experiment table is computed with.
  2. llm  (optional)         -- a Gemini judge marks each claim attributed/not,
     matching RAGAS's LLM-based approach. Non-deterministic; use for a labeled
     spot-check, not the controlled experiment.

Run directly to compute context recall for both retrievers on a golden set:
    python -m eval.context_recall --golden eval/golden_paraphrase.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_agent import CatProfile, CatTaskPlanningAgent  # noqa: E402
from knowledge_retriever import KnowledgeRetriever  # noqa: E402


# ---- context assembly ----------------------------------------------------

def retrieved_context_text(knowledge: Dict[str, Any]) -> str:
    """Flatten the retriever output into the 'retrieved context' string that
    the planner is grounded on."""
    parts: List[str] = []
    parts.extend(str(g) for g in knowledge.get("key_guidelines", []))
    parts.extend(str(t) for t in knowledge.get("recommended_tasks", []))
    for hc in knowledge.get("health_conditions", []):
        parts.append(str(hc.get("name", "")))
        parts.extend(str(c) for c in hc.get("care_requirements", []))
        parts.extend(str(r) for r in hc.get("recommended_tasks", []))
    for hp in knowledge.get("health_priorities", []):
        parts.extend(str(c) for c in hp.get("care_requirements", []))
    return " ".join(parts).lower()


# ---- claim attribution backends ------------------------------------------

def _tokens(s: str) -> set:
    return {t for t in "".join(c if c.isalnum() else " " for c in s.lower()).split() if t}


def claim_supported_deterministic(claim: str, context: str) -> bool:
    """A claim is supported if it appears as a substring, or if a strong
    majority of its content tokens appear in the context."""
    c = claim.lower().strip()
    if c in context:
        return True
    claim_tokens = _tokens(claim)
    if not claim_tokens:
        return False
    ctx_tokens = _tokens(context)
    overlap = len(claim_tokens & ctx_tokens) / len(claim_tokens)
    return overlap >= 0.6


def claim_supported_llm(claim: str, context: str, model: Any) -> bool:  # pragma: no cover
    """Optional Gemini judge: mark a single claim attributed or not."""
    from google.genai import types

    prompt = (
        "You are grading whether a claim is supported by retrieved context.\n"
        f"CONTEXT:\n{context}\n\nCLAIM:\n{claim}\n\n"
        "Answer with exactly one JSON object: {\"attributed\": true} or "
        "{\"attributed\": false}. A claim is attributed only if the context "
        "contains information that supports it."
    )
    resp = model.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0, responseMimeType="application/json"
        ),
    )
    try:
        return bool(json.loads(resp.text or "{}").get("attributed", False))
    except json.JSONDecodeError:
        return False


# ---- metric --------------------------------------------------------------

def context_recall_for_case(
    grounding_claims: List[str], context: str, backend: str = "deterministic", model: Any = None
) -> Tuple[float, List[str]]:
    """Return (recall, list_of_unsupported_claims) for one case."""
    if not grounding_claims:
        return 1.0, []
    unsupported: List[str] = []
    for claim in grounding_claims:
        if backend == "llm":
            ok = claim_supported_llm(claim, context, model)
        else:
            ok = claim_supported_deterministic(claim, context)
        if not ok:
            unsupported.append(claim)
    supported = len(grounding_claims) - len(unsupported)
    return supported / len(grounding_claims), unsupported


def build_agent(retriever_mode: str) -> CatTaskPlanningAgent:
    kb_path = str(REPO_ROOT / "knowledge_base")
    if retriever_mode == "embedding":
        from embedding_retriever import EmbeddingKnowledgeRetriever
        retriever = EmbeddingKnowledgeRetriever(knowledge_base_path=kb_path)
    else:
        retriever = KnowledgeRetriever(knowledge_base_path=kb_path)
    return CatTaskPlanningAgent(knowledge_retriever=retriever)


def evaluate(golden_path: Path, retriever_mode: str, backend: str = "deterministic") -> Dict[str, Any]:
    cases = [json.loads(l) for l in open(golden_path, encoding="utf-8") if l.strip()]
    agent = build_agent(retriever_mode)
    model = agent.client if backend == "llm" else None

    per_case = []
    for case in cases:
        inp = case["input"]
        profile = CatProfile(
            name=inp["name"], breed=inp["breed"], age_years=inp["age_years"],
            health_conditions=inp.get("health_conditions") or None,
            preferences=inp.get("preferences") or None,
        )
        try:
            result = agent.create_plan(profile)
            context = retrieved_context_text(result.get("knowledge", {}))
        except Exception:
            context = ""  # crashing retrieval = empty context = 0 recall
        claims = case["expected_facts"]["grounding"]
        recall, unsupported = context_recall_for_case(claims, context, backend, model)
        per_case.append({"id": case["id"], "context_recall": round(recall, 3), "unsupported": unsupported})

    mean = round(sum(c["context_recall"] for c in per_case) / len(per_case), 3)
    return {
        "retriever": retriever_mode,
        "backend": backend,
        "n_cases": len(per_case),
        "mean_context_recall": mean,
        "cases": per_case,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="RAGAS-style context recall for PawPal+.")
    ap.add_argument("--golden", default=str(REPO_ROOT / "eval" / "golden_paraphrase.jsonl"))
    ap.add_argument("--backend", choices=["deterministic", "llm"], default="deterministic")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    base = evaluate(Path(args.golden), "exact", args.backend)
    emb = evaluate(Path(args.golden), "embedding", args.backend)

    print("=" * 56)
    print(f"Context Recall (RAGAS def.) | backend={args.backend}")
    print(f"golden={Path(args.golden).name} | n={base['n_cases']}")
    print("=" * 56)
    print(f"  baseline (exact)   : {base['mean_context_recall']:.3f}")
    print(f"  embedding          : {emb['mean_context_recall']:.3f}")
    print(f"  delta              : {emb['mean_context_recall'] - base['mean_context_recall']:+.3f}")
    print("-" * 56)
    print(f"{'case':<10}{'exact':>8}{'embed':>8}")
    emb_by_id = {c["id"]: c for c in emb["cases"]}
    for c in base["cases"]:
        e = emb_by_id[c["id"]]
        print(f"{c['id']:<10}{c['context_recall']:>8.2f}{e['context_recall']:>8.2f}")

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        json.dump({"baseline": base, "embedding": emb}, open(args.out, "w"), indent=2)


if __name__ == "__main__":
    main()
