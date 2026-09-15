"""BrowserAct provider adapter for Amazon Reviews API.

Provider boundary only: starts BrowserAct's official Amazon Reviews workflow
and returns raw structured review records. It does not make business decisions.
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from typing import Any

API_BASE = "https://api.browseract.com/v2/workflow"
DEFAULT_TEMPLATE_ID = "77817507798321724"


def _request(url: str, api_key: str, method: str = "GET", body: Any = None) -> dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def run_reviews(
    asin: str,
    api_key: str | None = None,
    template_id: str | None = None,
    poll_interval: float = 5.0,
    max_wait_seconds: int = 1800,
) -> dict[str, Any]:
    """Run BrowserAct's no-login Amazon Reviews template for one ASIN."""
    api_key = api_key or os.getenv("BROWSERACT_API_KEY")
    if not api_key:
        raise RuntimeError("BROWSERACT_API_KEY is required")

    template_id = template_id or os.getenv(
        "BROWSERACT_REVIEW_WORKFLOW_TEMPLATE_ID", DEFAULT_TEMPLATE_ID
    )
    payload = {
        "workflow_template_id": template_id,
        "input_parameters": [{"name": "ASIN", "value": asin}],
    }
    started = _request(f"{API_BASE}/run-task-by-template", api_key, "POST", payload)
    task_id = started.get("id")
    if not task_id:
        raise RuntimeError(f"BrowserAct did not return task id: {started}")

    deadline = time.monotonic() + max_wait_seconds
    while time.monotonic() < deadline:
        status = _request(
            f"{API_BASE}/get-task?{urllib.parse.urlencode({'task_id': task_id})}",
            api_key,
        )
        state = str(status.get("status", "")).lower()
        if state in {"finished", "completed", "success"}:
            return status
        if state in {"failed", "error", "canceled", "cancelled"}:
            raise RuntimeError(f"BrowserAct task {task_id} failed: {status}")
        time.sleep(poll_interval)

    raise TimeoutError(f"BrowserAct task {task_id} did not finish within {max_wait_seconds}s")


def extract_output(task: dict[str, Any]) -> Any:
    """Decode BrowserAct task output when it is JSON; otherwise return text."""
    output = task.get("output", {})
    value = output.get("string") if isinstance(output, dict) else output
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def critical_reviews(reviews: Any) -> list[dict[str, Any]]:
    """Keep 1-2 star records without inferring pain or gate decisions."""
    if isinstance(reviews, dict):
        for key in ("reviews", "results", "data", "items"):
            if isinstance(reviews.get(key), list):
                reviews = reviews[key]
                break
    if not isinstance(reviews, list):
        return []
    result = []
    for item in reviews:
        if not isinstance(item, dict):
            continue
        rating = item.get("Rating", item.get("rating", item.get("stars")))
        try:
            if float(rating) <= 2:
                result.append(item)
        except (TypeError, ValueError):
            continue
    return result
