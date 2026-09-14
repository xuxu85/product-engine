from __future__ import annotations

from collections import Counter
from typing import Any

from pipeline.contracts import AgentRequest, AgentResult
from pipeline.state import Decision, Stage


REQUIRED_SOURCES = {"Amazon", "Reddit", "Interview"}


def normalize_evidence(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize raw evidence into the canonical CUSTOMER EVIDENCE shape."""
    normalized: list[dict[str, Any]] = []
    for item in evidence:
        source = str(item.get("source", "Other")).strip() or "Other"
        pain_statement = str(
            item.get("pain_statement", item.get("pain", ""))
        ).strip()
        if not pain_statement:
            continue
        normalized.append(
            {
                "source": source,
                "source_url": str(item.get("source_url", "")).strip(),
                "consumer_context": str(item.get("consumer_context", "")).strip(),
                "pain_statement": pain_statement,
                "intensity": float(item.get("intensity", 0)),
                "frequency_signal": str(item.get("frequency_signal", "")).strip(),
                "verbatim": str(item.get("verbatim", "")).strip(),
            }
        )
    return normalized


def build_opportunity(evidence: list[dict[str, Any]], request: AgentRequest) -> dict[str, Any]:
    """Build a deterministic Opportunity Card from verified evidence."""
    sources = {item["source"] for item in evidence}
    pain_counts = Counter(item["pain_statement"].lower() for item in evidence)
    dominant_pain = pain_counts.most_common(1)[0][0]
    avg_intensity = sum(item["intensity"] for item in evidence) / len(evidence)

    return {
        "title": f"Recurring pain: {dominant_pain[:80]}",
        "consumer": str(request.input.get("consumer", "")),
        "pain": dominant_pain,
        "pain_frequency": len(evidence),
        "pain_severity": round(avg_intensity, 2),
        "evidence_count": len(evidence),
        "evidence_sources": sorted(sources),
        "target_price": request.input.get("target_price", 0),
        "validation_cost": request.input.get("validation_cost", 0),
        "capital_required": request.input.get("capital_required", 0),
        "invalidation_condition": (
            "Invalidate if fewer than the configured minimum independent sources "
            "confirm the same recurring consumer problem."
        ),
    }


def run(request: AgentRequest) -> AgentResult:
    """Convert raw PAIN evidence into a verified pain decision and Opportunity Card."""
    if request.stage != Stage.PAIN:
        return AgentResult(
            decision=Decision.FAIL,
            output={"error": "pain workflow requires PAIN stage"},
            invalidation_conditions=["Workflow must only execute when pipeline stage is PAIN."],
            task_id=request.task_id,
            agent_id="pain.workflow",
            agent_version="0.1.0",
            status="ERROR",
        )

    evidence = normalize_evidence(request.evidence)
    minimum = int(request.constraints.get("minimum_evidence", 3))
    independent_sources = {item["source"] for item in evidence}
    verified = len(evidence) >= minimum and len(independent_sources) >= minimum

    if not verified:
        return AgentResult(
            decision=Decision.FAIL,
            output={
                "pain_verified": False,
                "evidence_count": len(evidence),
                "independent_source_count": len(independent_sources),
            },
            evidence=evidence,
            invalidation_conditions=[
                "Pain remains unverified if the minimum number of independent sources is not met."
            ],
            task_id=request.task_id,
            agent_id="pain.workflow",
            agent_version="0.1.0",
            confidence=0.4,
        )

    opportunity = build_opportunity(evidence, request)
    return AgentResult(
        decision=Decision.PASS,
        output={"pain_verified": True, "opportunity": opportunity},
        evidence=evidence,
        invalidation_conditions=[
            "Invalidate if fewer than the configured minimum independent sources confirm the same recurring consumer problem.",
            "Invalidate if subsequent validation fails to demonstrate willingness to pay."
        ],
        task_id=request.task_id,
        agent_id="pain.workflow",
        agent_version="0.1.0",
        confidence=1.0,
    )
