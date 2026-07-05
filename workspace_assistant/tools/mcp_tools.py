"""
Part 2: GitHub MCP Integration

Configure McpToolset to connect to the GitHub MCP server.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

# Path to MCP server configuration (for Option B)
MCP_CONFIG_PATH = Path(__file__).parent.parent / "config" / "mcp_servers.json"


def load_mcp_config() -> dict:
    """Load MCP server configuration from JSON file."""
    if not MCP_CONFIG_PATH.exists():
        raise FileNotFoundError(f"MCP config not found: {MCP_CONFIG_PATH}")

    with open(MCP_CONFIG_PATH) as f:
        config = json.load(f)

    github_config = config.get("mcpServers", {}).get("github", {})
    env = github_config.get("env", {})
    for key, value in list(env.items()):
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            env[key] = os.getenv(env_var, "")

    return config


def get_github_mcp_toolset() -> McpToolset:
    """Create a GitHub MCP toolset using the direct server configuration."""
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "").strip() or "ghp_placeholder"

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token},
    )

    return McpToolset(
        connection_params=StdioConnectionParams(server_params=server_params)
    )


def get_github_mcp_toolset_from_config() -> McpToolset:
    """Create a GitHub MCP toolset using the JSON configuration file."""
    config = load_mcp_config()
    github = config["mcpServers"]["github"]

    token = (
        github["env"].get("GITHUB_PERSONAL_ACCESS_TOKEN", "").strip()
        or "ghp_placeholder"
    )
    github["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"] = token

    server_params = StdioServerParameters(
        command=github["command"],
        args=github["args"],
        env=github["env"],
    )

    return McpToolset(
        connection_params=StdioConnectionParams(server_params=server_params)
    )


def search_github_tools(query: str) -> dict:
    """Search for likely GitHub MCP tools by keyword.

    Args:
        query: Search term such as "issues", "repo", or "pull request".

    Returns:
        A dictionary with matching tool names and a short explanation.
    """
    try:
        keywords = [word.lower() for word in query.split() if word]
        suggestions = [
            "search_repositories",
            "list_issues",
            "get_file_contents",
            "create_issue",
            "list_pull_requests",
        ]
        if not keywords:
            matches = suggestions
        else:
            matches = [
                name
                for name in suggestions
                if any(keyword in name.lower() for keyword in keywords)
            ]
        return {"status": "success", "query": query, "available_tools": matches}
    except Exception as exc:
        return {"status": "error", "message": f"Unable to search GitHub tools: {exc}"}


def get_github_mcp_toolset_deferred() -> McpToolset:
    """Create a GitHub MCP toolset with deferred loading to reduce context size."""
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "").strip() or "ghp_placeholder"

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token},
    )

    return McpToolset(
        connection_params=StdioConnectionParams(server_params=server_params),
        defer_loading=True,
    )


mcp_tools = [get_github_mcp_toolset()]
