from __future__ import annotations

from pipeline.contracts import AgentRequest, AgentResult
from pipeline.state import Decision, Stage


AGENT_ID = "pain.mock"
AGENT_VERSION = "0.1.0"


def run(request: AgentRequest) -> AgentResult:
    """Deterministic PAIN worker used to prove the agent-to-pipeline interface."""
    if request.stage != Stage.PAIN:
        return AgentResult(
            decision=Decision.FAIL,
            output={"error": "mock pain agent requires PAIN stage"},
            invalidation_conditions=["Agent must only execute when pipeline stage is PAIN."],
            task_id=request.task_id,
            agent_id=AGENT_ID,
            agent_version=AGENT_VERSION,
            status="ERROR",
        )

    evidence = request.evidence
    verified = len(evidence) >= int(request.constraints.get("minimum_evidence", 3))

    return AgentResult(
        decision=Decision.PASS if verified else Decision.FAIL,
        output={"pain_verified": verified, "evidence_count": len(evidence)},
        evidence=evidence,
        invalidation_conditions=[
            "Pain is invalidated if fewer than the configured minimum independent evidence sources confirm the same recurring problem."
        ],
        task_id=request.task_id,
        agent_id=AGENT_ID,
        agent_version=AGENT_VERSION,
        confidence=1.0 if verified else 0.4,
    )
