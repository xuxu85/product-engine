"""Deterministic synthetic MARKET/FINDER worker.

Architecture-only fixture: it must never be treated as market validation.
"""

from __future__ import annotations

from typing import Any

from pipeline.contracts import AgentRequest, AgentResult


def run(request: AgentRequest) -> AgentResult:
    if request.stage.value != "MARKET":
        return AgentResult(
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_version=request.agent_version,
            status="ERROR",
            decision="FAIL",
            output={},
            evidence=[],
            confidence=0.0,
            invalidation_conditions=["FAIL if the worker receives a stage other than MARKET."],
            next_stage=None,
        )

    candidates: list[dict[str, Any]] = request.input.get("candidates", [])
    if not candidates:
        return AgentResult(
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_version=request.agent_version,
            status="ERROR",
            decision="FAIL",
            output={},
            evidence=[],
            confidence=0.0,
            invalidation_conditions=["FAIL if no candidate fixture is supplied."],
            next_stage=None,
        )

    evidence = [
        {
            "source": "Synthetic",
            "source_url": "fixture://market",
            "candidate_id": candidate.get("candidate_id"),
            "signal": candidate.get("signal", "synthetic market signal"),
        }
        for candidate in candidates
    ]
    return AgentResult(
        task_id=request.task_id,
        agent_id=request.agent_id,
        agent_version=request.agent_version,
        status="SUCCESS",
        decision="PASS",
        output={"candidates": candidates},
        evidence=evidence,
        confidence=1.0,
        invalidation_conditions=["Architecture test only: replace synthetic evidence with real market evidence before a business PASS."],
        next_stage="PAIN",
    )
