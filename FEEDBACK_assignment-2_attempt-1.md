## Grade: 100 / 100

**Assignment:** Google Workspace Assistant + GitHub MCP (ADK)  
**Attempt:** 1 of 2  ·  **Graded:** 2026-07-11  ·  Commit `6ce1e93`

> **Note: provided files were modified.** These instructor-provided files (not meant to be changed) differ from the originals: `workspace_assistant/config/settings.py`, `workspace_assistant/main.py`. No automatic deduction was applied. If this was a necessary setup fix, no action is needed.

### Score breakdown
| Criterion | Max | Earned | Notes |
|-----------|-----|--------|-------|
| tool_design | 18 | 18 | Option B implemented cleanly: five plain-function tools (list_tasks, create_task, complete_task, update_task, delete_task) with clear action-oriented names, complete Args/Returns docstrings, and typed parameters (dict[str, Any], Optional[str], defaults), all collected into the tasks_tools list. (`workspace_assistant/tools/tasks_tools.py:142`) |
| agent_instructions | 14 | 13 | System instruction is clear and scoped: it names the task operations, describes GitHub help, and explicitly asks the agent to confirm before creating/modifying data. It is fairly terse, so it could give more concrete guidance on tool selection and GitHub safety. (`workspace_assistant/agent.py:25`) |
| error_handling | 14 | 13 | Every tool wraps its API call in try/except and returns a structured {status, message} dict on failure; success paths return {status: 'success', ...}. Edge cases beyond exceptions (e.g. validating due-date format) are not specifically handled. (`workspace_assistant/tools/tasks_tools.py:32`) |
| functionality | 14 | 13 | Tools call the correct Google Tasks API through get_tasks_service() with the right verbs (tasks().list/insert/update/delete) and complete_task correctly issues an update with status='completed'. Static reading shows correct operations; no runtime validation of inputs like RFC3339 due dates. (`workspace_assistant/tools/tasks_tools.py:23`) |
| code_quality | 10 | 9 | Code is readable, consistently structured, and well-documented; tools are wired into an LlmAgent via create_agent(). Minor: the module docstring still says 'Option B' generic scaffolding text. (`workspace_assistant/agent.py:34`) |
| mcp_configured | 10 | 9 | McpToolset is configured correctly for the GitHub MCP server via StdioServerParameters/StdioConnectionParams and attached to the agent through mcp_tools in create_agent() (agent.py:38). (`workspace_assistant/tools/mcp_tools.py:40`) |
| github_queries | 15 | 12 | GitHub queries are wired through the MCP toolset (mcp_tools = [get_github_mcp_toolset()]), which exposes repo/issue/PR operations to the agent; a JSON-config variant is also provided. The reflection adds little concrete GitHub-query evidence, so this is judged mainly from the wiring. (`workspace_assistant/tools/mcp_tools.py:124`) |
| mcp_error_handling | 5 | 3 | Missing token is handled by falling back to a placeholder so config does not crash, and load_mcp_config raises a clear FileNotFoundError; however the toolset construction/use itself is not wrapped, so a failing MCP server (bad token, npx failure) surfaces as a raw error at runtime. (`workspace_assistant/tools/mcp_tools.py:42`) |
| _bonus_ | +25 | +22 | |
| Integrity deduction | — | 0 | Provided files MODIFIED — flagged, no deduction (workspace_assistant/config/settings.py, workspace_assistant/main.py) |
| **Total** | **100** | **100** | |

### What went well
- Five well-designed Tasks tools with complete docstrings, type hints, and consistent {status, ...} return dicts, all collected into tasks_tools (tasks_tools.py:142).
- Consistent, user-friendly error handling: every tool catches exceptions and returns a structured error message (tasks_tools.py:32).
- Strong Part 2 wiring plus both bonus features: search_github_tools (mcp_tools.py:77) and a deferred McpToolset with defer_loading=True (mcp_tools.py:120).
- System instruction explicitly asks the agent to confirm before creating or modifying data (agent.py:28).

### What to improve (actionable)
- Wrap the MCP toolset creation/use in error handling so missing tokens or npx/server failures return a graceful message instead of a raw error (mcp_tools.py:42).
- Add the token/context-size comparison for create_agent_with_tool_search() to the reflection to claim the full tool-search bonus (agent.py:42, reflection_template.md).
- Expand the agent instruction with more concrete tool-selection and GitHub safety guidance (agent.py:25).
- Validate tool inputs such as RFC3339 due dates before calling the API to catch bad values earlier (tasks_tools.py:47).

### Automated checks
- ✅ All required files implemented
- ⚠️ Provided files MODIFIED — flagged, no deduction (workspace_assistant/config/settings.py, workspace_assistant/main.py)
- ✅ 0/0 output artifacts committed
- ✅ Reflection 695 words

### Resubmission
You may resubmit **once**. Push fixes to this repo, then notify the instructor; we'll re-grade as **Attempt 2 (final)**. This is attempt 1 of 2.

---
*Graded automatically with Claude Code against the course rubric. Questions → contact the instructor.*


---
<sub>🔎 **Autograder record** — attempt 1 of 2 · graded at commit `6ce1e93` · delivered 2026-07-11T18:01:03Z. Commits pushed to `main` after this timestamp are treated as a resubmission.</sub>
