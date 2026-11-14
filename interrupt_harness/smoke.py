import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check() -> None:
    process = StdioServerParameters(command=sys.executable, args=["-m", "interrupt_harness.server"])
    async with stdio_client(process) as (read, write):
        async with ClientSession(read, write) as client:
            await client.initialize()
            reply = await client.call_tool("ping", {})
            assert reply.content[0].text == "pong"
    print("MCP ping: pong")


if __name__ == "__main__":
    asyncio.run(check())
