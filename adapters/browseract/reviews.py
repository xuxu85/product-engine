"""BrowserAct provider adapter for Amazon Product Reviews.

Provider boundary only: resolve and validate the real workflow contract before
starting a task, then validate returned structured output before downstream
handoff. It does not make business decisions.
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from typing import Any

from core.mechanism_contract import FieldSpec, MechanismContract, require_valid, validate_inputs, validate_output

API_BASE = "https://api.browseract.com/v2/workflow"
DEFAULT_TEMPLATE_ID = "113863425622286759"
DEFAULT_WORKFLOW_NAME = "Amazon Product Reviews Scraper Bot"
DEFAULT_MARKETPLACE_URL = "https://www.amazon.es"
DEFAULT_REVIEW_COUNT = 10

REVIEW_CONTRACT = MechanismContract(
    mechanism="browseract-amazon-reviews-api",
    input_fields=(
        FieldSpec("Marketplace URL"),
        FieldSpec("ASIN"),
        FieldSpec("Review Count"),
    ),
    output_required_keys=("results",),
    output_item_required_keys=("asin", "review_text", "star_rating"),
)


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


def _find_workflow_id(api_key: str, workflow_name: str) -> str:
    payload = _request(
        f"{API_BASE}/list-workflows?{urllib.parse.urlencode({'page': 1, 'limit': 500})}",
        api_key,
    )
    matches = [
        item for item in payload.get("items", [])
        if str(item.get("name", "")).strip() == workflow_name
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"BrowserAct workflow preflight failed: expected exactly one workflow named {workflow_name!r}, found {len(matches)}"
        )
    return str(matches[0]["id"])


def _preflight_workflow(api_key: str, workflow_id: str) -> None:
    workflow = _request(
        f"{API_BASE}/get-workflow?{urllib.parse.urlencode({'workflow_id': workflow_id})}",
        api_key,
    )
    actual = {str(item.get("name")): item for item in workflow.get("input_parameters", [])}
    expected = {field.name for field in REVIEW_CONTRACT.input_fields if field.required}
    missing = sorted(expected - set(actual))
    if missing:
        raise RuntimeError(
            "BrowserAct workflow preflight failed: missing required provider inputs: "
            + ", ".join(missing)
        )


def run_reviews(
    asin: str,
    api_key: str | None = None,
    template_id: str | None = None,
    marketplace_url: str | None = None,
    review_count: int | None = None,
    poll_interval: float = 5.0,
    max_wait_seconds: int = 1800,
) -> dict[str, Any]:
    """Preflight the provider contract, then run one BrowserAct review task."""
    api_key = api_key or os.getenv("BROWSERACT_API_KEY")
    if not api_key:
        raise RuntimeError("BROWSERACT_API_KEY is required")

    template_id = template_id or os.getenv(
        "BROWSERACT_REVIEW_WORKFLOW_TEMPLATE_ID", DEFAULT_TEMPLATE_ID
    )
    workflow_name = os.getenv("BROWSERACT_REVIEW_WORKFLOW_NAME", DEFAULT_WORKFLOW_NAME)
    marketplace_url = marketplace_url or os.getenv(
        "AMAZON_MARKETPLACE_URL", DEFAULT_MARKETPLACE_URL
    )
    review_count = review_count or int(
        os.getenv("BROWSERACT_REVIEW_COUNT", str(DEFAULT_REVIEW_COUNT))
    )

    values = {
        "Marketplace URL": marketplace_url,
        "ASIN": asin,
        "Review Count": str(review_count),
    }
    require_valid(validate_inputs(REVIEW_CONTRACT, values))

    workflow_id = _find_workflow_id(api_key, workflow_name)
    _preflight_workflow(api_key, workflow_id)

    payload = {
        "workflow_id": workflow_id,
        "input_parameters": [
            {"name": "Marketplace URL", "value": marketplace_url},
            {"name": "ASIN", "value": asin},
            {"name": "Review Count", "value": str(review_count)},
        ],
    }
    started = _request(f"{API_BASE}/run-task", api_key, "POST", payload)
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
            output = extract_output(status)
            require_valid(validate_output(REVIEW_CONTRACT, output))
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
        rating = item.get("star_rating", item.get("Rating", item.get("rating", item.get("stars"))))
        try:
            if float(rating) <= 2:
                result.append(item)
        except (TypeError, ValueError):
            continue
    return result
