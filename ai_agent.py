"""
AI Task Planning Agent for PawPal+ Cat Care System

This module implements the agentic workflow that uses retrieved cat care
knowledge to generate structured task recommendations with Google Gemma.
It includes a deterministic fallback so the project remains reproducible
when the API key is unavailable.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError

from ai_validator import PlanValidator
from knowledge_retriever import KnowledgeRetriever

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class SuggestedTask(BaseModel):
    """Structured task recommendation returned by the agent."""

    task_type: str = Field(..., description="Canonical task type or label")
    description: str = Field(..., description="User-facing task description")
    priority: int = Field(..., ge=1, le=5, description="Priority from 1 to 5")
    frequency: str = Field(..., description="Recommended cadence or recurrence")
    suggested_time: str = Field(..., description="Suggested time label or schedule")
    rationale: str = Field(..., description="Why the task is recommended")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class AgentPlan(BaseModel):
    """Validated agent response schema."""

    summary: str = Field(..., description="Short summary of the care plan")
    suggested_tasks: List[SuggestedTask] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)


@dataclass
class CatProfile:
    """Input profile for the planning agent."""

    name: str
    breed: str
    age_years: int
    health_conditions: Optional[List[str]] = None
    preferences: Optional[List[str]] = None


class CatTaskPlanningAgent:
    """Plans cat care tasks using retrieved knowledge and Google Gemma."""

    def __init__(
        self,
        knowledge_retriever: Optional[KnowledgeRetriever] = None,
        model: str = DEFAULT_MODEL,
    ):
        self.retriever = knowledge_retriever or KnowledgeRetriever()
        self.validator = PlanValidator()
        self.model = model
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
        logger.info("CatTaskPlanningAgent initialized with model %s", self.model)

    def create_plan(self, profile: CatProfile) -> Dict[str, Any]:
        """Generate a structured care plan for a cat profile."""
        logger.info(
            "Creating plan for cat=%s breed=%s age=%s conditions=%s",
            profile.name,
            profile.breed,
            profile.age_years,
            profile.health_conditions,
        )

        knowledge = self.retriever.retrieve_for_cat(
            breed=profile.breed,
            age_years=profile.age_years,
            health_conditions=profile.health_conditions,
        )
        frequencies = self.retriever.get_task_frequency_recommendations(
            breed=profile.breed,
            age_years=profile.age_years,
            health_conditions=profile.health_conditions,
        )

        if not self._has_api_key():
            logger.warning("GOOGLE_API_KEY missing; using deterministic fallback plan")
            return self._build_fallback_plan(profile, knowledge, frequencies)

        try:
            raw_response = self._call_gemini(profile, knowledge, frequencies)
            plan = self._parse_plan(raw_response)
            logger.info("Gemini generated a valid plan with %d tasks", len(plan.suggested_tasks))
            plan_payload = plan.model_dump()
            validation = self.validator.validate_plan(
                profile=profile.__dict__,
                plan=plan_payload,
                knowledge=knowledge,
            )

            return {
                "source": "gemini",
                "profile": profile.__dict__,
                "knowledge": knowledge,
                "frequency_recommendations": frequencies,
                "plan": plan_payload,
                "validation": {
                    "passed": validation.passed,
                    "score": validation.score,
                    "errors": validation.errors,
                    "warnings": validation.warnings,
                },
            }
        except (ValidationError, json.JSONDecodeError, KeyError, ValueError) as exc:
            logger.exception("Gemini response could not be validated; using fallback plan")
            fallback = self._build_fallback_plan(profile, knowledge, frequencies)
            fallback["warnings"].append(f"Gemini output validation failed: {exc}")
            return fallback
        except Exception as exc:
            logger.exception("Gemini API call failed; using fallback plan")
            fallback = self._build_fallback_plan(profile, knowledge, frequencies)
            fallback["warnings"].append(f"Gemini API failure: {exc}")
            return fallback

    def _has_api_key(self) -> bool:
        return bool(os.getenv("GOOGLE_API_KEY"))

    def _call_gemini(
        self,
        profile: CatProfile,
        knowledge: Dict[str, Any],
        frequencies: Dict[str, str],
    ) -> Dict[str, Any]:
        """Ask Gemini to produce structured JSON for the care plan."""
        prompt = self._build_prompt(profile, knowledge, frequencies)
        logger.info("Sending planning prompt to Gemini (%s)", self.model)

        text = self._request_gemini(prompt)
        if not text or not text.strip():
            raise ValueError("Gemini returned an empty response body.")

        try:
            logger.debug("Gemini raw response: %s", text)
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Initial Gemini parse failed; retrying with stricter JSON-only prompt")
            retry_prompt = (
                prompt
                + "\n\nIMPORTANT: Return only valid JSON. Do not add markdown fences, notes, or extra text."
            )
            retry_text = self._request_gemini(retry_prompt)
            if not retry_text or not retry_text.strip():
                raise ValueError("Gemini retry returned an empty response body.")
            logger.debug("Gemini retry raw response: %s", retry_text)
            return json.loads(retry_text)

    def _request_gemini(self, prompt: str) -> str:
        """Send a single request to Gemini and return response text."""
        if self.client is None:
            raise ValueError("GOOGLE_API_KEY is not configured.")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                maxOutputTokens=4096,
                responseMimeType="application/json",
                responseSchema=AgentPlan.model_json_schema(),
            ),
        )
        text = response.text or ""
        if not text.strip():
            raise ValueError("Gemini returned an empty response body.")

        return text

    def _build_prompt(
        self,
        profile: CatProfile,
        knowledge: Dict[str, Any],
        frequencies: Dict[str, str],
    ) -> str:
        """Build a strict prompt that asks for JSON only."""
        condensed_context = {
            "recommended_tasks": knowledge.get("recommended_tasks", []),
            "key_guidelines": knowledge.get("key_guidelines", [])[:15],
            "health_priorities": knowledge.get("health_priorities", []),
        }

        return (
            "You are a cat care planning assistant for the PawPal+ app. "
            "Use the retrieved knowledge to generate a safe, practical care plan. "
            "Return a valid JSON object that matches the provided schema. "
            "Keep the plan concise and return 6 to 7 suggested tasks. "
            "Include baseline care coverage for feeding, water, and litter in the suggested tasks when appropriate. "
            "\n\nCat profile:\n"
            f"- Name: {profile.name}\n"
            f"- Breed: {profile.breed}\n"
            f"- Age: {profile.age_years}\n"
            f"- Health conditions: {profile.health_conditions or []}\n"
            f"- Preferences: {profile.preferences or []}\n\n"
            f"Retrieved context: {json.dumps(condensed_context, indent=2, default=str)}\n\n"
            f"Frequency recommendations: {json.dumps(frequencies, indent=2, default=str)}\n\n"
            "Rules:\n"
            "- Focus only on cat care tasks that are relevant to the retrieved knowledge.\n"
            "- Prefer indoor cat tasks like feeding, water, litter box cleaning, playtime, grooming, medication, monitoring, and vet visits.\n"
            "- Ensure the final plan includes feeding, water, and litter coverage if the cat profile allows it.\n"
            "- Include warnings if health conditions require extra attention.\n"
            "- Keep the recommendations realistic for a single owner to complete.\n"
            "- Use confidence scores between 0 and 1.\n"
            "- Do not include markdown fences or commentary."
        )

    def _parse_plan(self, raw_response: Dict[str, Any]) -> AgentPlan:
        """Validate Gemini output against the expected schema."""
        return AgentPlan.model_validate(raw_response)

    def _build_fallback_plan(
        self,
        profile: CatProfile,
        knowledge: Dict[str, Any],
        frequencies: Dict[str, str],
    ) -> Dict[str, Any]:
        """Create a deterministic plan when Claude is unavailable."""
        suggested_tasks: List[SuggestedTask] = []
        recommended_tasks = knowledge.get("recommended_tasks", [])
        age_group = knowledge.get("age_info", {}).get("name", "Cat") if knowledge.get("age_info") else "Cat"
        base_time_map = self._default_schedule(profile.age_years)

        for task_name in sorted(set(recommended_tasks)):
            task_type = task_name.replace("_", " ").title()
            suggested_tasks.append(
                SuggestedTask(
                    task_type=task_name,
                    description=f"{task_type} for {profile.name}",
                    priority=self._priority_for_task(task_name),
                    frequency=frequencies.get(task_name, f"Recommended for {age_group.lower()}") ,
                    suggested_time=base_time_map.get(task_name, "Flexible"),
                    rationale=self._rationale_for_task(task_name, knowledge),
                    confidence=0.78,
                )
            )

        warnings = [
            "Fallback plan used because GOOGLE_API_KEY was unavailable or the Gemini response failed validation.",
        ]
        warnings.extend(self._build_health_warnings(knowledge))

        plan = AgentPlan(
            summary=self._build_summary(profile, knowledge),
            suggested_tasks=suggested_tasks,
            warnings=warnings,
            next_steps=[
                "Review the suggested schedule before saving tasks.",
                "Adjust times if multiple high-priority tasks overlap.",
                "Confirm health-related tasks with a veterinarian when needed.",
            ],
        )

        plan_payload = plan.model_dump()
        validation = self.validator.validate_plan(
            profile=profile.__dict__,
            plan=plan_payload,
            knowledge=knowledge,
        )

        return {
            "source": "fallback",
            "profile": profile.__dict__,
            "knowledge": knowledge,
            "frequency_recommendations": frequencies,
            "plan": plan_payload,
            "warnings": warnings,
            "validation": {
                "passed": validation.passed,
                "score": validation.score,
                "errors": validation.errors,
                "warnings": validation.warnings,
            },
        }

    def _build_summary(self, profile: CatProfile, knowledge: Dict[str, Any]) -> str:
        breed = knowledge.get("breed_info", {}).get("name", profile.breed)
        age_name = knowledge.get("age_info", {}).get("name", "Cat") if knowledge.get("age_info") else "Cat"
        return f"Generated a {age_name.lower()} care plan for {profile.name} ({breed})."

    def _build_health_warnings(self, knowledge: Dict[str, Any]) -> List[str]:
        warnings: List[str] = []
        for condition in knowledge.get("health_priorities", []):
            severity = condition.get("severity", "unknown")
            condition_name = condition.get("condition", "condition")
            if severity == "high":
                warnings.append(f"{condition_name} requires close monitoring and vet guidance.")
            elif severity == "medium":
                warnings.append(f"{condition_name} should be tracked in the care plan.")
        return warnings

    def _default_schedule(self, age_years: int) -> Dict[str, str]:
        age_group = self.retriever.infer_age_group(age_years)
        if age_group == "kitten":
            return {
                "feeding_frequent": "Morning, midday, evening, and bedtime",
                "water_refresh": "Morning and evening",
                "playtime_multiple": "Several short sessions throughout the day",
                "socialization": "Daily",
                "training": "Short sessions after meals",
            }
        if age_group == "senior":
            return {
                "feeding_senior_formula": "Morning and evening",
                "gentle_play": "Mid-morning or early evening",
                "grooming": "Daily or as needed",
                "water_access": "All day",
                "comfort_monitoring": "Morning and evening",
                "vet_visits_frequent": "Schedule in advance",
            }
        return {
            "feeding_twice_daily": "Morning and evening",
            "playtime": "Late morning or evening",
            "grooming": "Weekly",
            "water_refresh": "Morning and evening",
            "litter_maintenance": "Morning and evening",
        }

    def _priority_for_task(self, task_name: str) -> int:
        if any(keyword in task_name for keyword in ["medication", "monitoring", "litter", "water"]):
            return 5 if "medication" in task_name else 4
        if any(keyword in task_name for keyword in ["feeding", "vet"]):
            return 4
        if any(keyword in task_name for keyword in ["grooming", "play", "training"]):
            return 3
        return 2

    def _rationale_for_task(self, task_name: str, knowledge: Dict[str, Any]) -> str:
        lower = task_name.lower()
        if "medication" in lower:
            return "Health conditions in the retrieved knowledge indicate medication support may be needed."
        if "water" in lower:
            return "Fresh water supports hydration and helps with common feline health risks."
        if "litter" in lower:
            return "Clean litter helps with comfort and lets you monitor elimination habits."
        if "groom" in lower:
            return "Grooming supports coat health and helps catch skin or matting issues early."
        if "play" in lower or "exercise" in lower:
            return "Play helps meet activity needs and reduces stress or boredom."
        if "monitor" in lower:
            return "Monitoring helps catch behavior or appetite changes early."
        if "vet" in lower:
            return "Regular veterinary care is recommended in the retrieved knowledge."
        return "This task is recommended by the retrieved cat care knowledge."


if __name__ == "__main__":
    agent = CatTaskPlanningAgent()
    demo_profile = CatProfile(
        name="Mochi",
        breed="Abyssinian",
        age_years=3,
        health_conditions=["Asthma"],
        preferences=["Lots of play", "Interactive toys"],
    )
    result = agent.create_plan(demo_profile)
    print(json.dumps(result, indent=2, default=str))
