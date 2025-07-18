#!/usr/bin/env python3
"""Google Docs MCP Server - Clean modular entry point."""

from mcp.server.fastmcp import FastMCP
from src.tools import register_tools

# Initialize FastMCP server
mcp = FastMCP("Google Docs API")

# Register all tools
register_tools(mcp)

def run():
    # Run the server using stdio transport
    mcp.run()


if __name__ == "__main__":
    run()