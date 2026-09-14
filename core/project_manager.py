"""Thin business Project Manager / Orchestrator layer.

This module plans and enforces execution; it does not replace research tools.
"""
from dataclasses import dataclass
from typing import Literal


Status = Literal["PASS", "FAIL", "PIVOT", "OPEN", "BLOCKED"]


@dataclass(frozen=True)
class ManagerDecision:
    stage: str
    gate: str
    lane: str
    status: Status
    bottleneck: str
    execution_mechanism: str
    capital_required: float
    next_action: str
    reason: str


class ProjectManager:
    """Determine the smallest next execution step for the current business gate."""

    STAGE_LANES = {
        "MARKET": "FINDER",
        "PAIN": "FINDER",
        "OPPORTUNITY": "FINDER",
        "PRODUCT_THESIS": "FINDER",
        "DEMAND_VALIDATION": "FINDER",
        "PRODUCT_SPEC": "BUILDER",
        "FORMULA": "BUILDER",
        "ECONOMICS": "BUILDER",
        "MANUFACTURING": "BUILDER",
        "PILOT": "BUILDER",
        "SALES": "SELLER",
        "REPEAT": "SELLER",
        "SCALE": "SELLER",
    }

    MECHANISMS = {
        "MARKET": "product-opportunity-finder-skill",
        "PAIN": "product-review-analyze-skill",
        "OPPORTUNITY": "product-opportunity-finder-skill + pain evidence",
        "PRODUCT_THESIS": "validated opportunity evidence",
        "DEMAND_VALIDATION": "Amazon / H10 / market validation workflow",
    }

    def plan(self, stage: str, *, evidence_ready: bool = False,
             required_provider_ready: bool = True,
             mechanism: str | None = None) -> ManagerDecision:
        stage = stage.upper()
        lane = self.STAGE_LANES.get(stage, "FINDER")
        mechanism = mechanism or self.MECHANISMS.get(stage, "stage-specific existing workflow")

        if not required_provider_ready:
            return ManagerDecision(
                stage=stage,
                gate=stage,
                lane=lane,
                status="BLOCKED",
                bottleneck="MISSING REQUIRED PROVIDER / DEPENDENCY",
                execution_mechanism=mechanism,
                capital_required=0.0,
                next_action="Define the exact missing function, verify whether an existing alternative can satisfy it, then authorize only the minimum required dependency.",
                reason="Only work that genuinely depends on the unavailable provider is blocked.",
            )

        if evidence_ready:
            return ManagerDecision(
                stage=stage,
                gate=stage,
                lane=lane,
                status="PASS",
                bottleneck="NEXT GATE",
                execution_mechanism=mechanism,
                capital_required=0.0,
                next_action="Route to the next gate and execute its minimum required evidence/workflow.",
                reason="Current gate has sufficient validated evidence for transition.",
            )

        return ManagerDecision(
            stage=stage,
            gate=stage,
            lane=lane,
            status="OPEN",
            bottleneck=f"CLOSE {stage} GATE",
            execution_mechanism=mechanism,
            capital_required=0.0,
            next_action=f"Execute {mechanism} only to obtain the evidence required to decide {stage}.",
            reason="Current gate is not yet supported by sufficient validated evidence.",
        )
