"""
Validator layer for AI-generated cat care plans.

This module provides guardrails and reliability checks for AI output.
It validates plan content against core safety and quality rules and
writes structured logs for traceability.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def _configure_validator_logger() -> logging.Logger:
    """Configure a file-backed logger for validator events."""
    logger = logging.getLogger("pawpal.ai_validator")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_dir / "ai_validator.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = _configure_validator_logger()


@dataclass
class ValidationResult:
    """Result of plan validation checks."""

    passed: bool
    errors: List[str]
    warnings: List[str]
    score: float


class PlanValidator:
    """Applies guardrail checks to an AI-generated care plan."""

    REQUIRED_BASELINE_TASKS = {"feeding", "water", "litter"}
    MAX_CONFIDENCE_WARN_THRESHOLD = 0.55

    def validate_plan(
        self,
        profile: Dict[str, Any],
        plan: Dict[str, Any],
        knowledge: Optional[Dict[str, Any]] = None,
    ) -> ValidationResult:
        """
        Validate plan content and return pass/fail with diagnostics.

        Checks include:
        - Presence and shape of plan fields
        - Priority range and confidence range
        - Baseline cat-care task coverage
        - Health condition task coverage
        - Duplicate task-time combinations
        """
        errors: List[str] = []
        warnings: List[str] = []

        summary = plan.get("summary")
        suggested_tasks = plan.get("suggested_tasks", [])

        if not summary or not isinstance(summary, str):
            errors.append("Plan summary is missing or invalid.")

        if not isinstance(suggested_tasks, list) or not suggested_tasks:
            errors.append("Plan must include at least one suggested task.")
            self._log_result(profile, False, 0.0, errors, warnings)
            return ValidationResult(False, errors, warnings, 0.0)

        normalized_types: List[str] = []

        for idx, task in enumerate(suggested_tasks, start=1):
            task_errors, task_warnings, normalized = self._validate_task(task, idx)
            errors.extend(task_errors)
            warnings.extend(task_warnings)
            if normalized:
                normalized_types.append(normalized)

        self._check_baseline_coverage(normalized_types, warnings)
        self._check_health_coverage(normalized_types, profile, knowledge, warnings)
        self._check_duplicate_time_blocks(suggested_tasks, warnings)

        score = self._compute_score(errors, warnings, len(suggested_tasks))
        passed = len(errors) == 0

        self._log_result(profile, passed, score, errors, warnings)
        return ValidationResult(passed, errors, warnings, score)

    def _validate_task(
        self, task: Dict[str, Any], index: int
    ) -> tuple[List[str], List[str], Optional[str]]:
        errors: List[str] = []
        warnings: List[str] = []

        required_fields = [
            "task_type",
            "description",
            "priority",
            "frequency",
            "suggested_time",
            "rationale",
            "confidence",
        ]

        for field in required_fields:
            if field not in task:
                errors.append(f"Task #{index} missing required field: {field}.")

        task_type = str(task.get("task_type", "")).strip()
        description = str(task.get("description", "")).strip()
        rationale = str(task.get("rationale", "")).strip()

        if not task_type:
            errors.append(f"Task #{index} has empty task_type.")
        if not description:
            errors.append(f"Task #{index} has empty description.")
        if len(rationale) < 12:
            warnings.append(
                f"Task #{index} rationale is too short and may be low quality."
            )

        priority = task.get("priority")
        if not isinstance(priority, int) or priority < 1 or priority > 5:
            errors.append(f"Task #{index} priority must be an integer between 1 and 5.")

        confidence = task.get("confidence")
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            errors.append(f"Task #{index} confidence must be between 0 and 1.")
        elif confidence < self.MAX_CONFIDENCE_WARN_THRESHOLD:
            warnings.append(
                f"Task #{index} has low confidence ({confidence:.2f}). Consider human review."
            )

        normalized = self._normalize_task_type(task_type)
        return errors, warnings, normalized

    def _check_baseline_coverage(
        self, normalized_types: List[str], warnings: List[str]
    ) -> None:
        pool = " ".join(normalized_types)
        missing = [
            required for required in self.REQUIRED_BASELINE_TASKS if required not in pool
        ]
        if missing:
            warnings.append(
                "Plan is missing baseline daily care categories: "
                + ", ".join(sorted(missing))
                + "."
            )

    def _check_health_coverage(
        self,
        normalized_types: List[str],
        profile: Dict[str, Any],
        knowledge: Optional[Dict[str, Any]],
        warnings: List[str],
    ) -> None:
        conditions = profile.get("health_conditions") or []
        if not conditions:
            return

        pool = " ".join(normalized_types)
        if "medication" not in pool and any(
            token in " ".join([c.lower() for c in conditions])
            for token in ["diabetes", "thyroid", "cardio", "asthma", "arthritis"]
        ):
            warnings.append(
                "Health conditions suggest medication-related tasks, but none were generated."
            )

        if knowledge:
            expected = knowledge.get("recommended_tasks", [])
            missing_expected = []
            for expected_task in expected:
                normalized_expected = self._normalize_task_type(str(expected_task))
                if normalized_expected and normalized_expected not in pool:
                    missing_expected.append(str(expected_task))
            if missing_expected:
                warnings.append(
                    "Some retrieved recommended tasks were not included: "
                    + ", ".join(sorted(set(missing_expected)))
                    + "."
                )

    def _check_duplicate_time_blocks(
        self, suggested_tasks: List[Dict[str, Any]], warnings: List[str]
    ) -> None:
        seen = set()
        duplicates = []

        for task in suggested_tasks:
            task_type = str(task.get("task_type", "")).strip().lower()
            suggested_time = str(task.get("suggested_time", "")).strip().lower()
            key = (task_type, suggested_time)
            if key in seen:
                duplicates.append(f"{task_type} @ {suggested_time}")
            seen.add(key)

        if duplicates:
            warnings.append(
                "Duplicate task-time suggestions detected: "
                + ", ".join(sorted(set(duplicates)))
                + "."
            )

    def _compute_score(
        self, errors: List[str], warnings: List[str], task_count: int
    ) -> float:
        base = 1.0
        base -= min(0.7, len(errors) * 0.25)
        base -= min(0.3, len(warnings) * 0.03)

        if task_count < 3:
            base -= 0.1

        return max(0.0, round(base, 2))

    def _normalize_task_type(self, task_type: str) -> Optional[str]:
        value = task_type.strip().lower().replace("_", " ")
        if not value:
            return None

        aliases = {
            "feeding": "feeding",
            "feeding frequent": "feeding",
            "feeding twice daily": "feeding",
            "feeding senior formula": "feeding",
            "water": "water",
            "water refresh": "water",
            "water bowl refresh": "water",
            "water access": "water",
            "litter": "litter",
            "litter box cleaning": "litter",
            "litter maintenance": "litter",
            "medication": "medication",
            "medication injection": "medication",
            "monitoring": "monitoring",
            "health monitoring": "monitoring",
            "playtime": "playtime",
            "gentle play": "playtime",
            "playtime multiple": "playtime",
            "grooming": "grooming",
            "vet visit": "vet",
            "vet visits": "vet",
            "veterinary checkup": "vet",
        }

        return aliases.get(value, value)

    def _log_result(
        self,
        profile: Dict[str, Any],
        passed: bool,
        score: float,
        errors: List[str],
        warnings: List[str],
    ) -> None:
        cat_name = profile.get("name", "unknown")
        breed = profile.get("breed", "unknown")

        logger.info(
            "validation_result | cat=%s | breed=%s | passed=%s | score=%.2f | errors=%d | warnings=%d",
            cat_name,
            breed,
            passed,
            score,
            len(errors),
            len(warnings),
        )

        if errors:
            for item in errors:
                logger.error("validation_error | cat=%s | %s", cat_name, item)

        if warnings:
            for item in warnings:
                logger.warning("validation_warning | cat=%s | %s", cat_name, item)

        logger.info("validation_timestamp | %s", datetime.utcnow().isoformat() + "Z")
