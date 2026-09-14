"""Normalize H10-like market data into canonical MARKET candidates.

This module intentionally contains no H10 network/authentication code.
It is a provider boundary: upstream data in, normalized candidates out.
"""

from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = (
    "candidate_id",
    "marketplace",
    "asin",
    "title",
    "price",
    "monthly_sales",
    "monthly_revenue",
    "review_count",
    "rating",
    "source",
)


def _first(item: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in item and item[key] is not None:
            return item[key]
    return default


def normalize_candidate(item: dict[str, Any], index: int = 0) -> dict[str, Any]:
    """Normalize one provider record without adding business conclusions."""
    asin = _first(item, "asin", "ASIN", "product_id", default=f"UNKNOWN-{index}")

    candidate = {
        "candidate_id": str(_first(item, "candidate_id", "id", default=asin)),
        "marketplace": _first(item, "marketplace", "market", "country", default="unknown"),
        "asin": str(asin),
        "title": str(_first(item, "title", "product_title", default="")),
        "price": _first(item, "price", "current_price"),
        "monthly_sales": _first(item, "monthly_sales", "sales", "estimated_monthly_sales"),
        "monthly_revenue": _first(item, "monthly_revenue", "revenue", "estimated_monthly_revenue"),
        "review_count": _first(item, "review_count", "reviews", "number_of_reviews"),
        "rating": _first(item, "rating", "stars"),
        "source": _first(item, "source", "provider"),
    }

    optional_metrics = item.get("metrics")
    if isinstance(optional_metrics, dict):
        candidate["metrics"] = dict(optional_metrics)

    metadata = item.get("metadata")
    if isinstance(metadata, dict):
        candidate["metadata"] = dict(metadata)

    missing = [field for field in REQUIRED_FIELDS if candidate[field] is None]
    if missing:
        raise ValueError(f"Missing required candidate fields: {', '.join(missing)}")

    return candidate


def normalize(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize an H10-like payload into canonical candidate records.

    Accepted top-level shapes:
    - {"candidates": [...]}
    - {"products": [...]}
    - {"results": [...]}
    """
    if not isinstance(payload, dict):
        raise TypeError("Provider payload must be a dict")

    records = None
    for key in ("candidates", "products", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            records = value
            break

    if records is None:
        raise ValueError("Provider payload must contain candidates, products, or results list")

    normalized = []
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            raise TypeError(f"Provider record at index {index} must be a dict")
        normalized.append(normalize_candidate(item, index=index))

    return normalized


class H10Adapter:
    """Stateless adapter facade used by the pipeline integration layer."""

    provider = "h10"

    def normalize(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        return normalize(payload)
