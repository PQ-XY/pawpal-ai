"""
Embedding-based knowledge retriever for PawPal+ (the "optimize" arm).

The baseline KnowledgeRetriever does exact dictionary-key lookups:
    breed.lower().replace(" ", "_") must equal a JSON key exactly.
That fails on realistic user input ("kidney disease", "Maine Coon cat",
"sugar diabetes") because none of those strings match a canonical key.

This subclass adds a resolution layer in front of every lookup. It maps a
free-text breed / age-group / condition string to the closest canonical key
before delegating to the parent's exact-match logic. So the only thing that
changes between baseline and treatment is *key resolution* — retrieval,
planning, and scoring downstream are identical. That isolation is what makes
the baseline-vs-embedding comparison a controlled experiment.

Resolution strategy, in order of preference:
  1. Exact key match (same as baseline — zero cost, no regression).
  2. Sentence-transformer cosine similarity, if the package is installed.
  3. A dependency-free lexical similarity (token Jaccard + char trigram dice),
     so the experiment is reproducible offline and during a live demo.

A match is only accepted above a similarity threshold; below it the lookup
returns None exactly like the baseline (no hallucinated matches).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from knowledge_retriever import KnowledgeRetriever

logger = logging.getLogger(__name__)

# Common lay-term aliases. These are *not* required for correctness — the
# similarity matcher resolves most of them anyway — but they make the intent
# auditable and pin a few medical synonyms the lexical matcher would miss.
CONDITION_ALIASES = {
    "kidney disease": "chronic_kidney_disease",
    "ckd": "chronic_kidney_disease",
    "renal disease": "chronic_kidney_disease",
    "sugar diabetes": "diabetes",
    "diabetes mellitus": "diabetes",
    "overactive thyroid": "hyperthyroidism",
    "thyroid": "hyperthyroidism",
    "heart disease": "hypertrophic_cardiomyopathy",
    "hcm": "hypertrophic_cardiomyopathy",
    "urinary tract disease": "feline_lower_urinary_tract_disease",
    "flutd": "feline_lower_urinary_tract_disease",
    "joint pain": "arthritis",
    "osteoarthritis": "arthritis",
    "fiv": "feline_immunodeficiency_virus",
    "breathing issues": "asthma",
}


def _tokens(s: str) -> List[str]:
    out, cur = [], []
    for ch in s.lower():
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            out.append("".join(cur))
            cur = []
    if cur:
        out.append("".join(cur))
    return out


def _trigrams(s: str) -> set:
    s = "".join(c for c in s.lower() if c.isalnum())
    return {s[i : i + 3] for i in range(len(s) - 2)} if len(s) >= 3 else {s}


def _lexical_similarity(a: str, b: str) -> float:
    """Blend of token Jaccard and character-trigram Dice. Range 0..1."""
    ta, tb = set(_tokens(a)), set(_tokens(b))
    jacc = len(ta & tb) / len(ta | tb) if (ta | tb) else 0.0
    ga, gb = _trigrams(a), _trigrams(b)
    dice = 2 * len(ga & gb) / (len(ga) + len(gb)) if (len(ga) + len(gb)) else 0.0
    return 0.5 * jacc + 0.5 * dice


class EmbeddingKnowledgeRetriever(KnowledgeRetriever):
    """KnowledgeRetriever with fuzzy/semantic key resolution in front."""

    SIM_THRESHOLD = 0.34

    def __init__(self, knowledge_base_path: str = "knowledge_base", use_st: bool = True):
        super().__init__(knowledge_base_path=knowledge_base_path)
        self._st_model = None
        self._st_cache: Dict[str, Any] = {}
        if use_st:
            self._try_load_sentence_transformer()
        backend = "sentence-transformers" if self._st_model else "lexical-fallback"
        logger.info("EmbeddingKnowledgeRetriever ready (backend=%s)", backend)

    def _try_load_sentence_transformer(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore

            self._st_model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Loaded sentence-transformers model all-MiniLM-L6-v2")
        except Exception as exc:  # ImportError or model download failure
            self._st_model = None
            logger.info("sentence-transformers unavailable (%s); using lexical fallback", exc)

    # ---- core resolution -------------------------------------------------

    def _candidate_strings(self, key: str, info: Dict[str, Any]) -> str:
        """A searchable text blob for a candidate key (key + display name)."""
        name = info.get("name", "") if isinstance(info, dict) else ""
        return f"{key.replace('_', ' ')} {name}".strip()

    def _resolve(self, query: str, table: Dict[str, Any]) -> Optional[str]:
        """Resolve a free-text query to the best canonical key in `table`."""
        if not query:
            return None

        norm = query.lower().strip().replace(" ", "_")
        if norm in table:  # exact match — identical to baseline behavior
            return norm

        cleaned = query.lower().strip()
        if cleaned in CONDITION_ALIASES and CONDITION_ALIASES[cleaned] in table:
            return CONDITION_ALIASES[cleaned]
        # alias substring (e.g. "feline asthma / breathing issues")
        for alias, target in CONDITION_ALIASES.items():
            if alias in cleaned and target in table:
                return target

        scored: List[Tuple[float, str]] = []
        if self._st_model is not None:
            scored = self._st_score(query, table)
        else:
            for key, info in table.items():
                cand = self._candidate_strings(key, info)
                scored.append((_lexical_similarity(query, cand), key))

        if not scored:
            return None
        scored.sort(reverse=True)
        best_score, best_key = scored[0]
        if best_score >= self.SIM_THRESHOLD:
            logger.info("Resolved '%s' -> '%s' (sim=%.2f)", query, best_key, best_score)
            return best_key
        logger.info("No confident match for '%s' (best sim=%.2f)", query, best_score)
        return None

    def _st_score(self, query: str, table: Dict[str, Any]) -> List[Tuple[float, str]]:
        import numpy as np  # local import; only on the ST path

        def embed(text: str):
            if text not in self._st_cache:
                self._st_cache[text] = self._st_model.encode(text, normalize_embeddings=True)
            return self._st_cache[text]

        q = embed(query)
        out = []
        for key, info in table.items():
            cand = self._candidate_strings(key, info)
            sim = float(np.dot(q, embed(cand)))
            out.append((sim, key))
        return out

    # ---- overrides: resolve, then delegate to the parent exact lookups ---

    def get_breed_info(self, breed: str) -> Optional[Dict[str, Any]]:
        resolved = self._resolve(breed, self.breeds)
        if resolved is None:
            logger.warning("Breed not resolvable: %s", breed)
            return None
        return self.breeds.get(resolved)

    def get_health_condition_info(self, condition: str) -> Optional[Dict[str, Any]]:
        resolved = self._resolve(condition, self.health_conditions)
        if resolved is None:
            logger.warning("Condition not resolvable: %s", condition)
            return None
        return self.health_conditions.get(resolved)

    def get_age_group_info(self, age_group: str) -> Optional[Dict[str, Any]]:
        resolved = self._resolve(age_group, self.age_groups)
        if resolved is None:
            return None
        return self.age_groups.get(resolved)


if __name__ == "__main__":
    r = EmbeddingKnowledgeRetriever()
    for q in ["kidney disease", "Maine Coon cat", "sugar diabetes", "overactive thyroid"]:
        table = r.health_conditions if "disease" in q or "diabetes" in q or "thyroid" in q else r.breeds
        print(f"{q!r:30} -> {r._resolve(q, table)}")
