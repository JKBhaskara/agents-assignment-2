"""
Option B: Tasks Manager Tools

Google Tasks operations for creating, listing, updating, completing, and deleting tasks.
"""

from typing import Any, Optional

from tools.auth import get_tasks_service


def list_tasks(tasklist: str = "@default", max_results: int = 10) -> dict[str, Any]:
    """List tasks from a Google Tasks task list.

    Args:
        tasklist: The task list ID or "@default".
        max_results: Maximum number of tasks to return.

    Returns:
        A dictionary containing the request status and the returned tasks.
    """
    try:
        service = get_tasks_service()
        result = (
            service.tasks().list(tasklist=tasklist, maxResults=max_results).execute()
        )
        return {
            "status": "success",
            "tasklist": tasklist,
            "tasks": result.get("items", []),
        }
    except Exception as exc:
        return {"status": "error", "message": f"Unable to list tasks: {exc}"}


def create_task(
    title: str,
    notes: Optional[str] = None,
    due: Optional[str] = None,
    tasklist: str = "@default",
) -> dict[str, Any]:
    """Create a new task in a Google Tasks list.

    Args:
        title: The task title.
        notes: Optional notes for the task.
        due: Optional due date in RFC3339 format.
        tasklist: The task list ID or "@default".

    Returns:
        A dictionary containing the request status and the created task.
    """
    try:
        service = get_tasks_service()
        body: dict[str, Any] = {"title": title}
        if notes:
            body["notes"] = notes
        if due:
            body["due"] = due
        result = service.tasks().insert(tasklist=tasklist, body=body).execute()
        return {"status": "success", "task": result}
    except Exception as exc:
        return {"status": "error", "message": f"Unable to create task: {exc}"}


def complete_task(task_id: str, tasklist: str = "@default") -> dict[str, Any]:
    """Mark an existing task as completed.

    Args:
        task_id: The Google Tasks task ID.
        tasklist: The task list ID or "@default".

    Returns:
        A dictionary containing the request status and the updated task.
    """
    try:
        service = get_tasks_service()
        result = (
            service.tasks()
            .update(tasklist=tasklist, task=task_id, body={"status": "completed"})
            .execute()
        )
        return {"status": "success", "task": result}
    except Exception as exc:
        return {"status": "error", "message": f"Unable to complete task: {exc}"}


def update_task(
    task_id: str,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    due: Optional[str] = None,
    tasklist: str = "@default",
) -> dict[str, Any]:
    """Update the details of an existing task.

    Args:
        task_id: The Google Tasks task ID.
        title: Optional new title.
        notes: Optional new notes.
        due: Optional new due date.
        tasklist: The task list ID or "@default".

    Returns:
        A dictionary containing the request status and the updated task.
    """
    try:
        service = get_tasks_service()
        body: dict[str, Any] = {}
        if title is not None:
            body["title"] = title
        if notes is not None:
            body["notes"] = notes
        if due is not None:
            body["due"] = due
        result = (
            service.tasks().update(tasklist=tasklist, task=task_id, body=body).execute()
        )
        return {"status": "success", "task": result}
    except Exception as exc:
        return {"status": "error", "message": f"Unable to update task: {exc}"}


def delete_task(task_id: str, tasklist: str = "@default") -> dict[str, Any]:
    """Delete a task from a Google Tasks list.

    Args:
        task_id: The Google Tasks task ID.
        tasklist: The task list ID or "@default".

    Returns:
        A dictionary containing the request status and the deleted task ID.
    """
    try:
        service = get_tasks_service()
        service.tasks().delete(tasklist=tasklist, task=task_id).execute()
        return {"status": "success", "deleted_task_id": task_id}
    except Exception as exc:
        return {"status": "error", "message": f"Unable to delete task: {exc}"}


tasks_tools = [list_tasks, create_task, complete_task, update_task, delete_task]
