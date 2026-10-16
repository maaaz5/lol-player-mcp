from mcp.server.fastmcp import FastMCP

from lol_mcp.config import load_settings
from lol_mcp.riot_client import RiotClient
from lol_mcp.tools.accounts import register_account_tools
from lol_mcp.tools.ranked import register_ranked_tools
from lol_mcp.tools.matches import register_match_tools


mcp = FastMCP("lol-mcp")


def main():
    settings = load_settings()
    riot = RiotClient(settings)

    register_account_tools(mcp, riot)
    register_ranked_tools(mcp, riot)
    register_match_tools(mcp, riot)

    # Start the MCP server using stdio transport.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
