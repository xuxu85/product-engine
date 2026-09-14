from __future__ import annotations

from typing import Any

from .contracts import AgentResult
from .state import Decision, Stage


REVIEW_MECHANISM = "product-review-analyze-skill"
REVIEW_REPOSITORY = "AronLEEdev/product-review-analyze-skill"


def review_report_to_result(report: dict[str, Any], *, task_id: str = "", agent_version: str = "") -> AgentResult:
    """Adapt a completed review-skill report into the Product Engine PAIN contract.

    The adapter only translates provider output. It does not collect reviews,
    classify products, invent filters, or manufacture evidence.
    """
    if not isinstance(report, dict):
        raise TypeError("report must be a dict")

    products = report.get("products", [])
    complaint_themes = report.get("complaintThemes", [])
    totals = report.get("totals", {})
    verdict = report.get("verdict")

    evidence = []
    for theme in complaint_themes:
        if not isinstance(theme, dict):
            continue
        for quote in theme.get("exampleQuotes", []) or []:
            if not isinstance(quote, dict) or not quote.get("quote"):
                continue
            evidence.append(
                {
                    "source": "amazon_reviews",
                    "provider": REVIEW_MECHANISM,
                    "repository": REVIEW_REPOSITORY,
                    "theme": theme.get("theme"),
                    "asin": quote.get("asin"),
                    "stars": quote.get("stars"),
                    "quote": quote["quote"],
                }
            )

    output = {
        "keyword": report.get("keyword"),
        "products": products,
        "totals": totals,
        "complaintThemes": complaint_themes,
        "praiseThemes": report.get("praiseThemes", []),
        "mustFix": report.get("mustFix", []),
        "mustKeep": report.get("mustKeep", []),
        "angle": report.get("angle"),
        "verdict": verdict,
        "market": report.get("market"),
        "keywords": report.get("keywords"),
        "provenance": {
            "mechanism": REVIEW_MECHANISM,
            "repository": REVIEW_REPOSITORY,
            "marketplace": "amazon.com",
        },
    }

    invalidation_conditions = [
        "PAIN evidence is insufficient when no complaint theme is supported by real review quotes.",
        "PAIN opportunity is invalidated when recurring complaints do not produce a material product gap.",
    ]

    decision = Decision.PASS if evidence and complaint_themes else Decision.FAIL

    return AgentResult(
        decision=decision,
        output=output,
        evidence=evidence,
        invalidation_conditions=invalidation_conditions,
        next_stage=Stage.OPPORTUNITY if decision is Decision.PASS else None,
        task_id=task_id,
        agent_id=REVIEW_MECHANISM,
        agent_version=agent_version,
        status="SUCCESS",
        confidence=None,
    )
