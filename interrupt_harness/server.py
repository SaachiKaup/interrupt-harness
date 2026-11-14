from mcp.server.fastmcp import FastMCP

from openmath_chat import (
    DEFAULT_PROJECT,
    DEFAULT_TEAM,
    continue_chat,
    find_chats,
    list_models,
    read_summary,
    start_chat,
    stop_chat,
)

server = FastMCP(
    "interrupt-harness",
    instructions=(
        "Send mathematical investigations to OpenMathOS with start. For status requests, "
        "use summary and summarize only its published records. Do not solve, compile, "
        "or reproduce the investigation locally. Use continue to send a new turn to an "
        "existing session, including after a stop request. Start new work, continue a "
        "session, or stop a session only when the user asks."
    ),
)


@server.tool()
def ping() -> str:
    """Check that the local server is reachable."""
    return "pong"


@server.tool()
def models() -> list[dict]:
    """List selectable model IDs and their reasoning effort choices."""
    return list_models()


@server.tool()
def find_sessions(query: str, limit: int = 10, team: str = DEFAULT_TEAM,
                  project: str = DEFAULT_PROJECT) -> list[dict]:
    """Find recent project chats by title or their first page of history."""
    return find_chats(query, team=team, project=project, limit=limit)


@server.tool()
def start(prompt: str, team: str = DEFAULT_TEAM, project: str = DEFAULT_PROJECT,
          title: str = "", model: str = "", effort: str = "") -> dict:
    """Start in Caltech Mathathon SPA by default; use models for model IDs and effort choices."""
    return start_chat(prompt, team=team, project=project, title=title, model=model, effort=effort)


@server.tool(name="continue")
def continue_turn(prompt: str, session: str, team: str = DEFAULT_TEAM,
                  project: str = DEFAULT_PROJECT, model: str = "", effort: str = "") -> dict:
    """Send a new turn to an existing session, even if it was previously stopped."""
    return continue_chat(
        prompt, session=session, team=team, project=project, model=model, effort=effort
    )


@server.tool()
def summary(session: str, team: str = DEFAULT_TEAM, project: str = DEFAULT_PROJECT) -> dict:
    """Fetch the full published history for this session so you can summarize it for the user."""
    return read_summary(team, project, session)


@server.tool()
def stop(session: str, team: str = DEFAULT_TEAM, project: str = DEFAULT_PROJECT) -> dict:
    """Send one stop request to the exact OpenMathOS session."""
    return stop_chat(team, project, session)


if __name__ == "__main__":
    server.run(transport="stdio")
