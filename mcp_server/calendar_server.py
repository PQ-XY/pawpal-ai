"""
PawPal+ Calendar MCP server (FastMCP).

Exposes the cat-care calendar as MCP tools. The agent connects to this server
as an MCP client and calls these tools to schedule approved care tasks.

Backed by a local JSON store (calendar_store.json) so the integration is fully
self-contained: a real MCP server + real tool calls over the protocol, with no
external OAuth or cloud setup. The storage layer is isolated in one place, so
swapping it for a live Google/Notion backend later means changing only the
_load/_save/_insert helpers — the MCP tool surface stays identical.

Tools:
  - create_care_event(cat_name, task_type, description, date, time, priority)
  - list_upcoming_events(cat_name=None, limit=20)
  - delete_event(event_id)        # soft-safety: only marks cancelled

Run the server (stdio transport, what the client below uses):
    python -m mcp_server.calendar_server

Inspect it manually:
    npx @modelcontextprotocol/inspector python -m mcp_server.calendar_server
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

STORE_PATH = Path(__file__).resolve().parent / "calendar_store.json"

mcp = FastMCP("pawpal-calendar")


# --- storage layer (the only part that would change for a live backend) ----

def _load() -> List[Dict[str, Any]]:
    if not STORE_PATH.exists():
        return []
    try:
        return json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _save(events: List[Dict[str, Any]]) -> None:
    STORE_PATH.write_text(json.dumps(events, indent=2), encoding="utf-8")


# --- MCP tools -------------------------------------------------------------

@mcp.tool()
def create_care_event(
    cat_name: str,
    task_type: str,
    description: str,
    date: str,
    time: str = "09:00",
    priority: int = 3,
) -> Dict[str, Any]:
    """Schedule an approved cat-care task as a calendar event.

    Args:
        cat_name: Name of the cat the task is for.
        task_type: Canonical task type (e.g. feeding, medication, monitoring).
        description: Human-readable task description.
        date: Event date as YYYY-MM-DD.
        time: Event time as HH:MM (24h). Defaults to 09:00.
        priority: 1-5 priority; defaults to 3.

    Returns:
        The created event record, including its generated event_id.
    """
    events = _load()
    event = {
        "event_id": uuid.uuid4().hex[:12],
        "cat_name": cat_name,
        "task_type": task_type,
        "description": description,
        "date": date,
        "time": time,
        "priority": int(priority),
        "status": "scheduled",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    events.append(event)
    _save(events)
    return event


@mcp.tool()
def list_upcoming_events(cat_name: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
    """List scheduled care events, optionally filtered to one cat.

    Args:
        cat_name: If given, only return events for this cat.
        limit: Max number of events to return.

    Returns:
        A list of scheduled (non-cancelled) event records, sorted by date/time.
    """
    events = [e for e in _load() if e.get("status") == "scheduled"]
    if cat_name:
        events = [e for e in events if e.get("cat_name", "").lower() == cat_name.lower()]
    events.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))
    return events[:limit]


@mcp.tool()
def delete_event(event_id: str) -> Dict[str, Any]:
    """Cancel a scheduled event by id (soft delete; marks status=cancelled).

    Args:
        event_id: The id returned by create_care_event.

    Returns:
        {"event_id": ..., "cancelled": true/false}
    """
    events = _load()
    found = False
    for e in events:
        if e.get("event_id") == event_id:
            e["status"] = "cancelled"
            found = True
            break
    if found:
        _save(events)
    return {"event_id": event_id, "cancelled": found}


if __name__ == "__main__":
    mcp.run(transport="stdio")
