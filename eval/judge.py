"""
LLM-as-judge for PawPal+ : groundedness scoring.
 
Scores ONE quality dimension per generated plan:
 
    groundedness = is every care claim in the plan supported by the
                   knowledge that was actually retrieved for that cat?
 
Label is binary per plan:
    1 = grounded     (plan advice traceable to retrieved KB context)
    0 = not grounded (plan contains advice the retrieval did not support)
 
Two judge backends:
  - deterministic (default): rule-based groundedness check. Reproducible,
    offline, no API key. Used to produce a stable label column.
  - llm (--backend llm)    : a Gemini judge returns {"grounded": 0/1, "reason": ...}.
    Matches the LLM-as-judge pattern; non-deterministic.
 
The judge label is "rater 2". The human label file (eval/human_labels.jsonl)
is "rater 1". Cohen's kappa between them is computed in eval/cohens_kappa.py.
 
Usage:
    python -m eval.judge --golden eval/golden.jsonl --out eval/judge_labels.jsonl
    python -m eval.judge --golden eval/golden.jsonl --backend llm --out eval/judge_labels_llm.jsonl
"""
 
from __future__ import annotations
 
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List
 
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
 
from ai_agent import CatProfile, CatTaskPlanningAgent  # noqa: E402
from knowledge_retriever import KnowledgeRetriever  # noqa: E402
from eval.context_recall import retrieved_context_text  # noqa: E402
 
 
def _tokens(s: str) -> set:
    return {t for t in "".join(c if c.isalnum() else " " for c in s.lower()).split() if t}
 
 
def judge_groundedness_deterministic(plan: Dict[str, Any], context: str) -> Dict[str, Any]:
    """Rule: a plan is grounded if a strong majority of its tasks are traceable
    to the retrieved context — i.e. the task's subject appears in what was
    retrieved. We test each task_type's content tokens against the context
    (ignoring generic boilerplate). Groundedness is about whether the plan's
    recommendations came from retrieval, not about rationale phrasing."""
    tasks = plan.get("suggested_tasks", [])
    if not tasks:
        return {"grounded": 0, "reason": "no tasks in plan"}
 
    ctx_tokens = _tokens(context)
    untraceable = []
    for task in tasks:
        # The task_type is the claim subject (e.g. "feeding_specialized",
        # "medication", "monitoring"). Split it into content tokens and check
        # whether its core appears in retrieved context.
        ttoks = _tokens(task.get("task_type", ""))
        if not ttoks:
            untraceable.append(task.get("task_type", "<empty>"))
            continue
        # grounded if ANY content token of the task subject is present in context
        if not (ttoks & ctx_tokens):
            untraceable.append(task.get("task_type", ""))
 
    frac_untraceable = len(untraceable) / len(tasks)
    grounded = 1 if frac_untraceable <= 0.34 else 0
    return {
        "grounded": grounded,
        "reason": f"{len(untraceable)}/{len(tasks)} tasks not traceable to retrieval "
                  f"(frac={frac_untraceable:.2f})"
                  + (f"; e.g. {untraceable[:3]}" if untraceable else ""),
    }
 
 
def _generate_with_backoff(client: Any, model: str, prompt: str, max_retries: int = 6):
    """Call Gemini, backing off on 429 / RESOURCE_EXHAUSTED until it succeeds.
    Free-tier is ~5 requests/min, so a rate-limited run self-throttles here
    instead of crashing."""
    import time
    from google.genai import types
 
    delay = 20.0  # free-tier RetryInfo typically asks ~20s
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0, responseMimeType="application/json"
                ),
            )
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            is_rate = "429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower()
            if not is_rate or attempt == max_retries - 1:
                raise
            print(f"  [rate-limited; sleeping {delay:.0f}s then retrying "
                  f"({attempt + 1}/{max_retries})]")
            time.sleep(delay)
    raise RuntimeError("exhausted retries")
 
 
def judge_groundedness_llm(plan: Dict[str, Any], context: str, client: Any, model: str) -> Dict[str, Any]:  # pragma: no cover
    plan_text = json.dumps(
        {"summary": plan.get("summary"), "tasks": [
            {"task_type": t.get("task_type"), "rationale": t.get("rationale")}
            for t in plan.get("suggested_tasks", [])
        ]},
        indent=2,
    )
    prompt = (
        "You are evaluating whether a cat-care plan is GROUNDED in retrieved knowledge.\n"
        "A plan is grounded (1) only if its task rationales are supported by the CONTEXT. "
        "If the plan asserts care advice the context does not support, it is not grounded (0).\n\n"
        f"RETRIEVED CONTEXT:\n{context}\n\nPLAN:\n{plan_text}\n\n"
        "Return exactly one JSON object: {\"grounded\": 0 or 1, \"reason\": \"...\"}"
    )
    resp = _generate_with_backoff(client, model, prompt)
    try:
        out = json.loads(resp.text or "{}")
        return {"grounded": int(out.get("grounded", 0)), "reason": str(out.get("reason", ""))}
    except (json.JSONDecodeError, ValueError):
        return {"grounded": 0, "reason": "judge returned unparseable output"}
 
 
def build_agent(retriever_mode: str) -> CatTaskPlanningAgent:
    kb_path = str(REPO_ROOT / "knowledge_base")
    if retriever_mode == "embedding":
        from embedding_retriever import EmbeddingKnowledgeRetriever
        retriever = EmbeddingKnowledgeRetriever(knowledge_base_path=kb_path)
    else:
        retriever = KnowledgeRetriever(knowledge_base_path=kb_path)
    return CatTaskPlanningAgent(knowledge_retriever=retriever)
 
 
def run(golden_path: Path, backend: str, retriever_mode: str, out_path: str | None,
        sleep_between: float = 0.0) -> List[Dict[str, Any]]:
    import time
    cases = [json.loads(l) for l in open(golden_path, encoding="utf-8") if l.strip()]
    agent = build_agent(retriever_mode)
    model_name = getattr(agent, "model", "gemini-2.5-flash")
 
    rows: List[Dict[str, Any]] = []
    for idx, case in enumerate(cases):
        if sleep_between and idx > 0:
            time.sleep(sleep_between)
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
        except Exception as exc:
            rows.append({"id": case["id"], "grounded": 0, "reason": f"plan error: {exc}"})
            continue
 
        if backend == "llm":
            verdict = judge_groundedness_llm(plan, context, agent.client, model_name)
        else:
            verdict = judge_groundedness_deterministic(plan, context)
        rows.append({
            "id": case["id"],
            "grounded": verdict["grounded"],
            "reason": verdict["reason"],
            # Persist the exact plan + context that was judged, so an
            # independent human labeler reviews the SAME artifact (required for
            # a valid Cohen's kappa).
            "source": result.get("source"),
            "input": inp,
            "context": context,
            "plan_tasks": [
                {"task_type": t.get("task_type"), "rationale": t.get("rationale")}
                for t in plan.get("suggested_tasks", [])
            ],
            "summary": plan.get("summary", ""),
        })
 
        # Write incrementally so a mid-run rate-limit failure keeps progress.
        if out_path:
            Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as fh:
                for r in rows:
                    fh.write(json.dumps(r) + "\n")
        print(f"  [{idx + 1}/{len(cases)}] {case['id']}: grounded={verdict['grounded']}")
 
    return rows
 
 
def main() -> None:
    ap = argparse.ArgumentParser(description="LLM-as-judge: groundedness labels for PawPal+ plans.")
    ap.add_argument("--golden", default=str(REPO_ROOT / "eval" / "golden.jsonl"))
    ap.add_argument("--backend", choices=["deterministic", "llm"], default="deterministic")
    ap.add_argument("--retriever", choices=["exact", "embedding"], default="exact")
    ap.add_argument("--out", default=str(REPO_ROOT / "eval" / "judge_labels.jsonl"))
    ap.add_argument("--sleep", type=float, default=0.0,
                    help="Seconds to wait between cases (free-tier: try 30 to stay under 5/min).")
    args = ap.parse_args()
 
    rows = run(Path(args.golden), args.backend, args.retriever, args.out, args.sleep)
    n_grounded = sum(r["grounded"] for r in rows)
    print(f"Judge ({args.backend}) labeled {len(rows)} plans: "
          f"{n_grounded} grounded, {len(rows) - n_grounded} not grounded.")
    print(f"Labels written to {args.out}")
 
 
if __name__ == "__main__":
    main()
