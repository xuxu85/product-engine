"""BrowserAct Amazon product-search provider boundary."""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from typing import Any

API_BASE = "https://api.browseract.com/v2/workflow"
DEFAULT_TEMPLATE_ID = "77809217106347580"


def _request(url: str, api_key: str, method: str = "GET", body: Any = None) -> dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def run_search(keywords: str, brand: str = "", limit: int = 20, language: str = "en", api_key: str | None = None, template_id: str | None = None, max_wait_seconds: int = 600, poll_interval: int = 10) -> Any:
    """Run one BrowserAct Amazon Product Search task and return provider output."""
    api_key = api_key or os.getenv("BROWSERACT_API_KEY")
    if not api_key:
        raise RuntimeError("BROWSERACT_API_KEY is required")
    if not keywords.strip():
        raise ValueError("keywords must not be empty")
    template_id = template_id or os.getenv("BROWSERACT_PRODUCT_SEARCH_TEMPLATE_ID", DEFAULT_TEMPLATE_ID)
    payload = {"workflow_template_id": template_id, "input_parameters": [
        {"name": "KeyWords", "value": keywords},
        {"name": "Brand", "value": brand},
        {"name": "Maximum_date", "value": str(limit)},
        {"name": "language", "value": language},
    ]}
    started = _request(f"{API_BASE}/run-task-by-template", api_key, "POST", payload)
    task_id = started.get("id")
    if not task_id:
        raise RuntimeError(f"BrowserAct did not return task id: {started}")
    deadline = time.monotonic() + max_wait_seconds
    while time.monotonic() < deadline:
        status = _request(f"{API_BASE}/get-task-status?{urllib.parse.urlencode({'task_id': task_id})}", api_key)
        state = str(status.get("status", "")).lower()
        if state == "finished":
            task = _request(f"{API_BASE}/get-task?{urllib.parse.urlencode({'task_id': task_id})}", api_key)
            output = task.get("output", {})
            value = output.get("string") if isinstance(output, dict) else output
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return value
        if state in {"failed", "error", "canceled", "cancelled"}:
            raise RuntimeError(f"BrowserAct task {task_id} failed: {status}")
        time.sleep(poll_interval)
    raise TimeoutError(f"BrowserAct task {task_id} did not finish within {max_wait_seconds}s")
