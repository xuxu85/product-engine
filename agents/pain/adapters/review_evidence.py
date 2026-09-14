from __future__ import annotations

from typing import Any


def reviews_to_evidence(reviews_by_item: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize review-analysis output into CUSTOMER EVIDENCE records.

    The adapter accepts an upstream review workflow's structured output and
    converts negative/critical reviews into evidence records. It does not
    infer demand, sales, or willingness to pay.
    """
    evidence: list[dict[str, Any]] = []
    for item_id, polarity in reviews_by_item.items():
        for review in polarity.get("critical", []):
            body = str(review.get("body", "")).strip()
            title = str(review.get("title", "")).strip()
            if not body and not title:
                continue
            evidence.append({
                "source": str(review.get("source", "Review")),
                "source_url": str(review.get("source_url", "")),
                "consumer_context": str(review.get("consumer_context", "")),
                "pain_statement": f"{title}: {body}".strip(": "),
                "intensity": float(review.get("intensity", 0)),
                "frequency_signal": str(review.get("frequency_signal", "critical_review")),
                "verbatim": body or title,
                "item_id": item_id,
            })
    return evidence
