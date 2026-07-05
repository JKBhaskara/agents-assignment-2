"""
Google Workspace Assistant - Main Agent Definition

Part 1: Implement tasks tools and system instructions.
Part 2: Add a GitHub MCP toolset for repository and issue workflows.
"""

import os

from google.adk.agents import LlmAgent

from config.settings import Settings
from tools.mcp_tools import (
    get_github_mcp_toolset_deferred,
    mcp_tools,
    search_github_tools,
)
from tools.tasks_tools import tasks_tools


def create_agent() -> LlmAgent:
    """Create the Workspace Assistant agent with Tasks and GitHub capabilities."""
    settings = Settings()

    instruction = """You are a helpful Google Workspace assistant for task management and GitHub workflows.
You can list, create, update, complete, and delete tasks in Google Tasks.
You can also help with GitHub by listing repositories, inspecting issues, and creating issues when a user asks.
Always explain what you are doing clearly, and when a user asks to create or modify data, confirm the action before making changes.
"""

    if settings.google_api_key:
        os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)

    return LlmAgent(
        name="workspace_assistant",
        model=settings.model_name,
        instruction=instruction,
        tools=[*tasks_tools, *mcp_tools],
    )


def create_agent_with_tool_search() -> LlmAgent:
    """Create an agent that uses deferred GitHub tool loading to reduce context size."""
    settings = Settings()

    instruction = """You are a helpful Google Workspace assistant for task management and GitHub workflows.
Use the GitHub tool search helper first when a user asks about repositories, issues, or pull requests.
You can list, create, update, complete, and delete tasks in Google Tasks.
"""

    if settings.google_api_key:
        os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)

    return LlmAgent(
        name="workspace_assistant_search",
        model=settings.model_name,
        instruction=instruction,
        tools=[*tasks_tools, search_github_tools, get_github_mcp_toolset_deferred()],
    )
