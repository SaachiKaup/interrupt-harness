from mcp.server.fastmcp import FastMCP

server = FastMCP("interrupt-harness")


@server.tool()
def ping() -> str:
    """Check that the local server is reachable."""
    return "pong"


if __name__ == "__main__":
    server.run(transport="stdio")
