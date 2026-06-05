"""
MCP client for the PawPal+ calendar server.

The agent uses this to schedule approved care tasks by calling tools on the
calendar MCP server. It launches the server as a stdio subprocess, performs the
MCP handshake, lists available tools, and calls them — i.e. a real MCP client
talking to a real MCP server over the protocol.

The MCP Python SDK is async; this wrapper exposes small synchronous helpers so
the rest of the (synchronous) PawPal+ codebase can call them without dealing
with the event loop.

Example:
    from mcp_server.calendar_client import CalendarMCPClient
    client = CalendarMCPClient()
    ev = client.create_care_event("Smokey", "medication", "Give insulin",
                                  "2026-06-10", "08:00", 5)
    print(client.list_upcoming_events("Smokey"))
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

REPO_ROOT = Path(__file__).resolve().parent.parent


def _server_params() -> StdioServerParameters:
    # Launch the server module with the same interpreter, from the repo root,
    # so its imports resolve.
    return StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.calendar_server"],
        cwd=str(REPO_ROOT),
    )


async def _call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    async with stdio_client(_server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments)
            # FastMCP returns structured content; prefer structured, fall back
            # to the text block.
            if getattr(result, "structuredContent", None) is not None:
                sc = result.structuredContent
                # FastMCP wraps list/scalar returns under "result"
                return sc.get("result", sc) if isinstance(sc, dict) else sc
            if result.content:
                block = result.content[0]
                text = getattr(block, "text", None)
                if text is not None:
                    import json
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return text
            return None


async def _list_tools() -> List[str]:
    async with stdio_client(_server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            return [t.name for t in tools.tools]


def _run(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        # Already inside an event loop (e.g. some notebook/UI contexts):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


class CalendarMCPClient:
    """Synchronous facade over the calendar MCP server."""

    def list_tools(self) -> List[str]:
        return _run(_list_tools())

    def create_care_event(
        self, cat_name: str, task_type: str, description: str,
        date: str, time: str = "09:00", priority: int = 3,
    ) -> Dict[str, Any]:
        return _run(_call_tool("create_care_event", {
            "cat_name": cat_name, "task_type": task_type,
            "description": description, "date": date,
            "time": time, "priority": priority,
        }))

    def list_upcoming_events(self, cat_name: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        return _run(_call_tool("list_upcoming_events", {"cat_name": cat_name, "limit": limit}))

    def delete_event(self, event_id: str) -> Dict[str, Any]:
        return _run(_call_tool("delete_event", {"event_id": event_id}))


if __name__ == "__main__":
    c = CalendarMCPClient()
    print("Available MCP tools:", c.list_tools())
    ev = c.create_care_event("Smokey", "medication", "Give insulin injection",
                             "2026-06-10", "08:00", 5)
    print("Created:", ev)
    print("Upcoming for Smokey:", c.list_upcoming_events("Smokey"))
