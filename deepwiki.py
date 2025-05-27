# deepwiki.py

from agents import Agent, Runner
from agents.mcp import MCPServerSse

deepwiki_agent = None
mcp_server = None

async def setup_deepwiki():
    global deepwiki_agent, mcp_server
    mcp_server = await MCPServerSse(
        name="DeepWiki",
        params={"url": "https://mcp.deepwiki.com/sse"}
    ).__aenter__()

    deepwiki_agent = Agent(
        name="DeepWikiAgent",
        instructions="You are a helpful assistant with access to DeepWiki tools.",
        mcp_servers=[mcp_server],
    )

async def cleanup_deepwiki():
    global mcp_server
    if mcp_server:
        await mcp_server.__aexit__(None, None, None)

async def handle_deepwiki_query(message: str) -> str:
    if deepwiki_agent is None:
        raise RuntimeError("DeepWiki agent not initialized")

    result = await Runner.run(starting_agent=deepwiki_agent, input=message)
    return result.final_output
