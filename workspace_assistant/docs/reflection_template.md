# Assignment 2 Reflection

**Name:** Student
**Option:** B - Tasks
**Date:** 2026-07-05

---

## Tool Design Decisions

### Tools Implemented
1. **list_tasks**: Retrieves tasks from a Google Tasks list and returns them in a structured format.
2. **create_task**: Creates a new task with an optional title, notes, and due date.
3. **complete_task**: Marks an existing task as completed.
4. **update_task**: Updates task details such as title, notes, or due date.
5. **delete_task**: Removes a task from the selected task list.

### Why These Tools?
These tools were implemented to support a practical task-management workflow for the assistant. The main goal was to let the agent help a user list, create, modify, and complete tasks in Google Tasks without requiring manual interaction with the Google interface. This makes the agent more useful for everyday productivity scenarios.

### Description Strategy
The tool descriptions were written in direct, action-oriented language so the LLM could clearly understand each tool’s purpose. I used verbs like “list,” “create,” “update,” and “complete,” and I included key details such as task list, title, notes, due date, and task ID. This helped the agent map user requests to the right tool more reliably.

---

## Challenges Encountered

### Challenge 1: Missing ADK Session
- **Problem:** The agent threw a session-related error when trying to run a query because the runner was attempting to use a session that had not been initialized.
- **Solution:** I added a helper that creates or reuses a session before each request, which made the runtime behavior consistent and prevented the session lookup failure.

### Challenge 2: Model and API Configuration Errors
- **Problem:** The app initially failed because the model name and API key were not being handled correctly. Some errors were caused by an invalid or unsupported model string, while others were caused by missing Gemini credentials in the runtime environment.
- **Solution:** I updated the configuration flow so the project reads the API key and model name from the environment file and normalizes the model name to a supported format before the agent is created.

### Challenge 3: Quota and Rate-Limit Errors
- **Problem:** The model requests were sometimes blocked by Google’s free-tier quota, which produced 429 errors.
- **Solution:** I identified the issue as an external quota limit rather than a code defect, and I adjusted the configuration to use a supported model name while recognizing that quota limits may still affect runtime behavior.

---

## Error Handling Approach

I designed the tool functions to catch exceptions and return structured error messages instead of failing silently. Each tool returns a dictionary with a status field and either the requested result or an explanatory message. This makes debugging easier and gives the agent a clear way to report issues back to the user. I also focused on surfacing configuration problems, such as bad model names or missing API credentials, in a way that is easier to understand than a raw stack trace.

---

## Ideas for Improvement

If I had more time, I would add the following improvements:

1. Better fallback behavior when the primary model reaches quota limits, such as switching to a secondary model or retrying with a backoff strategy.
2. A more polished authentication flow for Google services, including clearer prompts for OAuth setup and token refresh.
3. Additional task-management capabilities such as filtering by due date, task list selection, and richer task summaries.

---

## Key Learnings

This assignment showed me that building AI agents is not only about writing tools, but also about making sure the surrounding runtime is configured correctly. The biggest lesson was that agent failures often come from environment setup, session management, or model compatibility issues rather than from the tool logic itself. I also learned that tool descriptions and function signatures need to be precise because the LLM depends on them to choose the correct action.

Overall, this project taught me how important it is to debug the system end-to-end. A working tool still needs proper session initialization, valid credentials, and a compatible model configuration to behave correctly in practice. That experience made the integration between the LLM, the tools, and the external services much clearer to me.
