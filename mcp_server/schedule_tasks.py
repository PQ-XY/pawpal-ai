"""
Schedule HITL-approved cat-care tasks to the calendar via the MCP client.

This is the seam between PawPal+'s human-in-the-loop approval step and the
calendar MCP server. The frontend collects the user's approved tasks; this
module turns each into a calendar event by calling the MCP `create_care_event`
tool. Only approved tasks are scheduled — the human stays in the loop.

Usage (after the user approves tasks in the UI):
    from mcp_server.schedule_tasks import schedule_approved_tasks
    events = schedule_approved_tasks(
        cat_name="Smokey",
        approved_tasks=[...],     # list of task dicts from the approved plan
        start_date="2026-06-10",
    )
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List

from mcp_server.calendar_client import CalendarMCPClient

# Map free-form suggested_time labels to a concrete HH:MM for the event.
_TIME_HINTS = {
    "morning": "08:00", "afternoon": "13:00", "evening": "18:00",
    "night": "21:00", "with meals": "08:00",
}


def _resolve_time(suggested_time: str) -> str:
    """Map a free-form suggested_time label to a concrete HH:MM (24h)."""
    s = (suggested_time or "").strip().lower()
    if not s:
        return "09:00"

    # Try to parse an explicit clock time, e.g. "8:00 am", "17:30", "5 pm".
    import re
    m = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", s)
    if m and m.group(1):
        hour = int(m.group(1))
        minute = int(m.group(2) or 0)
        ampm = m.group(3)
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        if 0 <= hour <= 23 and 0 <= minute <= 59 and (":" in s or ampm):
            return f"{hour:02d}:{minute:02d}"

    for hint, hhmm in _TIME_HINTS.items():
        if hint in s:
            return hhmm
    return "09:00"


def schedule_approved_tasks(
    cat_name: str,
    approved_tasks: List[Dict[str, Any]],
    start_date: str | None = None,
    client: CalendarMCPClient | None = None,
) -> List[Dict[str, Any]]:
    """Schedule each approved task as a calendar event via MCP.

    Args:
        cat_name: The cat the tasks are for.
        approved_tasks: Tasks the user approved (each a dict with at least
            task_type, description; optionally suggested_time, priority).
        start_date: ISO date (YYYY-MM-DD) for the events; defaults to today.
        client: Optional injected MCP client (for testing).

    Returns:
        The list of created event records returned by the MCP server.
    """
    client = client or CalendarMCPClient()
    date = start_date or datetime.utcnow().strftime("%Y-%m-%d")

    created: List[Dict[str, Any]] = []
    for task in approved_tasks:
        event = client.create_care_event(
            cat_name=cat_name,
            task_type=str(task.get("task_type", "task")),
            description=str(task.get("description", "")),
            date=date,
            time=_resolve_time(str(task.get("suggested_time", ""))),
            priority=int(task.get("priority", 3) or 3),
        )
        created.append(event)
    return created


if __name__ == "__main__":
    demo_tasks = [
        {"task_type": "medication", "description": "Insulin injection",
         "suggested_time": "Morning", "priority": 5},
        {"task_type": "feeding", "description": "Measured meal",
         "suggested_time": "8:00 AM", "priority": 4},
    ]
    out = schedule_approved_tasks("Smokey", demo_tasks, start_date="2026-06-10")
    print(f"Scheduled {len(out)} events via MCP:")
    for e in out:
        print(" ", e)
