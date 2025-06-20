import json
import os

from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from remote_mcp_agent.prompt import NOTION_PROMPT

# ---- MCP Library ----
# https://github.com/modelcontextprotocol/servers
# https://smithery.ai/

# ---- Notion -----
# https://developers.notion.com/docs/mcp
# https://github.com/makenotion/notion-mcp-server
# https://github.com/makenotion/notion-mcp-server/blob/main/scripts/notion-openapi.json

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if NOTION_API_KEY is None:
    raise ValueError("NOTION_API_KEY is not set")

# Use a simpler headers format
NOTION_MCP_HEADERS = json.dumps({
    "Authorization": f"Bearer {NOTION_API_KEY}", 
    "Notion-Version": "2022-06-28"
})

root_agent = Agent(
  model="gemini-2.0-flash",
  name="Notion_MCP_Agent",
  instruction=NOTION_PROMPT,
  tools=[
    MCPToolset(
      connection_params=StdioServerParameters(
        command="docker",
        args=[
          "run",
          "--rm",
          "-i",
          "-e", "OPENAPI_MCP_HEADERS",
          "mcp/notion"
        ],
        env={"OPENAPI_MCP_HEADERS": NOTION_MCP_HEADERS},
      )
    ),
  ],
)