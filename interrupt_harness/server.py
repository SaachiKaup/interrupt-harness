from mcp.server.fastmcp import FastMCP

from openmath_chat import DEFAULT_PROJECT, DEFAULT_TEAM, list_models, start_chat

server = FastMCP("interrupt-harness")


@server.tool()
def ping() -> str:
    """Check that the local server is reachable."""
    return "pong"


@server.tool()
def models() -> list[dict]:
    """List selectable model IDs and their reasoning effort choices."""
    return list_models()


@server.tool()
def start(prompt: str, team: str = DEFAULT_TEAM, project: str = DEFAULT_PROJECT,
          title: str = "", model: str = "", effort: str = "") -> dict:
    """Start in Caltech Mathathon SPA by default; use models for model IDs and effort choices."""
    return start_chat(prompt, team=team, project=project, title=title, model=model, effort=effort)


if __name__ == "__main__":
    server.run(transport="stdio")
