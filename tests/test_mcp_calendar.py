"""
Unit tests for the MCP calendar integration.

These mirror the project's existing mock-based testing approach: the external
boundary (the MCP client, which would launch the server subprocess) is replaced
with a fake, so the tests are deterministic and need neither the running MCP
server nor the mcp SDK installed.

What's covered:
  - approved tasks are scheduled as events (one tool call per task)
  - free-form suggested_time labels resolve to concrete HH:MM
  - only the approved tasks are scheduled (human-in-the-loop respected)
  - missing/sloppy fields fall back to safe defaults

Run:
    pytest tests/test_mcp_calendar.py -v
"""

from __future__ import annotations

from mcp_server.schedule_tasks import _resolve_time, schedule_approved_tasks


class FakeCalendarClient:
    """Stand-in for CalendarMCPClient that records calls instead of launching
    the real MCP server."""

    def __init__(self):
        self.calls = []
        self._counter = 0

    def create_care_event(self, cat_name, task_type, description, date, time="09:00", priority=3):
        self._counter += 1
        record = {
            "event_id": f"evt{self._counter}",
            "cat_name": cat_name, "task_type": task_type,
            "description": description, "date": date,
            "time": time, "priority": priority, "status": "scheduled",
        }
        self.calls.append(record)
        return record


def test_schedules_one_event_per_approved_task():
    fake = FakeCalendarClient()
    tasks = [
        {"task_type": "medication", "description": "Insulin", "suggested_time": "Morning", "priority": 5},
        {"task_type": "feeding", "description": "Meal", "suggested_time": "8:00 AM", "priority": 4},
    ]
    events = schedule_approved_tasks("Smokey", tasks, start_date="2026-06-10", client=fake)
    assert len(events) == 2
    assert len(fake.calls) == 2  # exactly one tool call per approved task
    assert events[0]["cat_name"] == "Smokey"


def test_only_approved_tasks_are_scheduled():
    """The function schedules exactly what it is given — the HITL approval
    upstream decides the list, nothing extra is invented here."""
    fake = FakeCalendarClient()
    approved = [{"task_type": "water", "description": "Refresh water"}]
    events = schedule_approved_tasks("Luna", approved, client=fake)
    assert len(events) == 1
    assert fake.calls[0]["task_type"] == "water"


def test_time_label_resolves_to_clock_time():
    fake = FakeCalendarClient()
    tasks = [{"task_type": "feeding", "description": "Meal", "suggested_time": "5:00 PM"}]
    schedule_approved_tasks("Felix", tasks, start_date="2026-06-10", client=fake)
    assert fake.calls[0]["time"] == "17:00"


def test_missing_fields_use_safe_defaults():
    fake = FakeCalendarClient()
    tasks = [{"task_type": "monitoring"}]  # no description, time, or priority
    events = schedule_approved_tasks("Coco", tasks, client=fake)
    assert events[0]["priority"] == 3        # default priority
    assert events[0]["time"] == "09:00"      # default time
    assert events[0]["description"] == ""    # empty, not crash


def test_resolve_time_units():
    assert _resolve_time("Morning") == "08:00"
    assert _resolve_time("8:00 AM") == "08:00"
    assert _resolve_time("12:00 PM") == "12:00"
    assert _resolve_time("") == "09:00"
    assert _resolve_time("with meals") == "08:00"
