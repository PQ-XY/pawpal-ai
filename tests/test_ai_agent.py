"""
Unit tests for the PawPal+ AI planning layer (CatTaskPlanningAgent).

These complement the existing tests/test_pawpal.py, which cover the
deterministic scheduler (Owner / Pet / Scheduler / Task). This file targets
the AI components the rubric asks for: tool/path routing, retry behavior, and
error paths — all with the Gemini call MOCKED so the suite is deterministic and
needs no API key or network.

Mock seam: CatTaskPlanningAgent._request_gemini is the single method that talks
to the network. Patching it lets us simulate any model response (valid JSON,
malformed JSON, empty body, exceptions) without a real client.

Run:
    pytest tests/test_ai_agent.py -v
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from ai_agent import AgentPlan, CatProfile, CatTaskPlanningAgent
from knowledge_retriever import KnowledgeRetriever


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def retriever():
    """Real retriever over the repo's knowledge base (deterministic)."""
    return KnowledgeRetriever(knowledge_base_path="knowledge_base")


@pytest.fixture
def agent(retriever):
    """Agent with a real retriever. No API key needed; tests that exercise the
    Gemini path inject a fake client and patch _request_gemini."""
    return CatTaskPlanningAgent(knowledge_retriever=retriever)


@pytest.fixture
def healthy_profile():
    return CatProfile(name="Jasper", breed="Domestic Shorthair", age_years=5)


@pytest.fixture
def ckd_profile():
    return CatProfile(
        name="Smokey", breed="Siamese", age_years=11,
        health_conditions=["Chronic Kidney Disease"],
    )


def _valid_gemini_payload() -> dict:
    """A schema-valid AgentPlan payload, as Gemini would return after json.loads."""
    return {
        "summary": "Care plan for a test cat.",
        "suggested_tasks": [
            {
                "task_type": "feeding", "description": "Feed the cat",
                "priority": 4, "frequency": "2 times daily",
                "suggested_time": "8:00 AM", "rationale": "Daily nutrition is essential.",
                "confidence": 0.9,
            },
            {
                "task_type": "water", "description": "Refresh water",
                "priority": 4, "frequency": "daily",
                "suggested_time": "Morning", "rationale": "Fresh water supports hydration.",
                "confidence": 0.88,
            },
            {
                "task_type": "litter", "description": "Clean litter box",
                "priority": 5, "frequency": "daily",
                "suggested_time": "Evening", "rationale": "Clean litter prevents illness.",
                "confidence": 0.85,
            },
        ],
        "warnings": [],
        "next_steps": ["Review the plan."],
    }


# --------------------------------------------------------------------------
# 1-2. Routing: no key -> fallback; key + valid response -> gemini
# --------------------------------------------------------------------------

def test_routes_to_fallback_when_no_api_key(agent, healthy_profile, monkeypatch):
    """With no GOOGLE_API_KEY the agent must use the deterministic fallback."""
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    result = agent.create_plan(healthy_profile)
    assert result["source"] == "fallback"
    assert result["plan"]["suggested_tasks"]  # non-empty


def test_routes_to_gemini_when_key_present_and_response_valid(agent, healthy_profile, monkeypatch):
    """With a key and a valid mocked response, the agent uses the Gemini path."""
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-key-for-test")
    agent.client = object()  # non-None so _request_gemini's guard passes
    payload = json.dumps(_valid_gemini_payload())
    with patch.object(agent, "_request_gemini", return_value=payload) as mock_req:
        result = agent.create_plan(healthy_profile)
    assert result["source"] == "gemini"
    assert mock_req.call_count == 1  # valid first try, no retry
    assert len(result["plan"]["suggested_tasks"]) == 3


# --------------------------------------------------------------------------
# 3. Retry: malformed JSON on first call -> stricter reprompt -> success
# --------------------------------------------------------------------------

def test_retry_on_malformed_json_then_succeeds(agent, healthy_profile, monkeypatch):
    """First response is non-JSON; agent retries with a stricter prompt and
    succeeds on the second call (two _request_gemini calls, gemini source)."""
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-key-for-test")
    agent.client = object()
    good = json.dumps(_valid_gemini_payload())
    with patch.object(
        agent, "_request_gemini",
        side_effect=["this is not json {oops", good],
    ) as mock_req:
        result = agent.create_plan(healthy_profile)
    assert mock_req.call_count == 2          # retry happened
    assert result["source"] == "gemini"      # retry recovered the call


def test_retry_exhausted_falls_back(agent, healthy_profile, monkeypatch):
    """If both the first call and the retry return junk, the agent gives up and
    falls back rather than raising."""
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-key-for-test")
    agent.client = object()
    with patch.object(
        agent, "_request_gemini",
        side_effect=["not json", "still not json"],
    ) as mock_req:
        result = agent.create_plan(healthy_profile)
    assert mock_req.call_count == 2
    assert result["source"] == "fallback"
    assert any("validation failed" in w.lower() for w in result["warnings"])


# --------------------------------------------------------------------------
# 4-6. Error paths -> graceful fallback (never raises out of create_plan)
# --------------------------------------------------------------------------

def test_empty_response_falls_back(agent, healthy_profile, monkeypatch):
    """An empty model body raises ValueError internally and routes to fallback."""
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-key-for-test")
    agent.client = object()
    with patch.object(agent, "_request_gemini", return_value="   "):
        result = agent.create_plan(healthy_profile)
    assert result["source"] == "fallback"


def test_schema_invalid_response_falls_back(agent, healthy_profile, monkeypatch):
    """Valid JSON that violates the AgentPlan schema (priority out of range,
    missing fields) must route to fallback, not crash."""
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-key-for-test")
    agent.client = object()
    bad_schema = json.dumps({
        "summary": "Bad plan",
        "suggested_tasks": [{"task_type": "feeding", "priority": 99}],  # missing fields, bad priority
    })
    with patch.object(agent, "_request_gemini", return_value=bad_schema):
        result = agent.create_plan(healthy_profile)
    assert result["source"] == "fallback"


def test_api_exception_falls_back_with_warning(agent, healthy_profile, monkeypatch):
    """A raised exception from the network call is caught and converted to a
    fallback plan carrying an explanatory warning."""
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-key-for-test")
    agent.client = object()
    with patch.object(agent, "_request_gemini", side_effect=RuntimeError("503 unavailable")):
        result = agent.create_plan(healthy_profile)
    assert result["source"] == "fallback"
    assert any("api failure" in w.lower() for w in result["warnings"])


# --------------------------------------------------------------------------
# 7-8. Parsing / schema validation contract
# --------------------------------------------------------------------------

def test_parse_plan_accepts_valid_payload(agent):
    """_parse_plan returns an AgentPlan for a schema-valid dict."""
    plan = agent._parse_plan(_valid_gemini_payload())
    assert isinstance(plan, AgentPlan)
    assert len(plan.suggested_tasks) == 3


def test_parse_plan_rejects_out_of_range_priority(agent):
    """_parse_plan raises for a priority outside 1..5 (schema guard works)."""
    from pydantic import ValidationError
    bad = _valid_gemini_payload()
    bad["suggested_tasks"][0]["priority"] = 9  # ge=1, le=5 violated
    with pytest.raises(ValidationError):
        agent._parse_plan(bad)


# --------------------------------------------------------------------------
# 9. Health grounding routes into the fallback plan (bonus integration check)
# --------------------------------------------------------------------------

def test_fallback_plan_grounds_health_condition(agent, ckd_profile, monkeypatch):
    """A CKD cat's fallback plan should surface medication/monitoring tasks
    retrieved from the knowledge base."""
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    result = agent.create_plan(ckd_profile)
    task_types = " ".join(t["task_type"] for t in result["plan"]["suggested_tasks"]).lower()
    assert "medication" in task_types or "monitoring" in task_types
