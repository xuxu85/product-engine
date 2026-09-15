"""Thin Project Manager / Orchestrator for PRODUCT ENGINE.

The manager plans and enforces execution. It does not replace research tools,
execute browser work, or authorize capital.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.mechanism_registry import mechanisms_for

from .state import Decision, PipelineState, Stage


@dataclass(frozen=True)
class ExecutionPlan:
    stage: Stage
    lane: str
    mechanism: str
    objective: str
    bottleneck: str
    capital_required: float = 0.0
    blocked: bool = False
    blocking_reason: str = ""
    next_action: str = ""
    constraints: dict[str, Any] = field(default_factory=dict)


class ProjectManager:
    """Select the smallest valid execution plan for the current gate."""

    _LANE = {
        Stage.IDEA: "FINDER",
        Stage.MARKET: "FINDER",
        Stage.PAIN: "FINDER",
        Stage.OPPORTUNITY: "FINDER",
        Stage.PRODUCT_THESIS: "FINDER",
        Stage.DEMAND_VALIDATION: "FINDER",
        Stage.PRODUCT_SPEC: "BUILDER",
        Stage.FORMULA: "BUILDER",
        Stage.ECONOMICS: "BUILDER",
        Stage.MANUFACTURING: "BUILDER",
        Stage.PILOT: "BUILDER",
        Stage.SALES: "SELLER",
        Stage.REPEAT: "SELLER",
        Stage.SCALE: "SELLER",
    }

    _MECHANISM = {
        Stage.MARKET: "product-opportunity-finder-skill",
        Stage.PAIN: "review_pain_analysis",
        Stage.OPPORTUNITY: "pain.workflow + opportunity handoff",
        Stage.PRODUCT_THESIS: "product-engine thesis worker",
        Stage.DEMAND_VALIDATION: "existing validation workflow",
        Stage.PRODUCT_SPEC: "product-engine product-spec worker",
        Stage.FORMULA: "supplier/formulation workflow",
        Stage.ECONOMICS: "unit-economics workflow",
        Stage.MANUFACTURING: "RFQ/supplier workflow",
        Stage.PILOT: "pilot execution workflow",
        Stage.SALES: "Amazon/listing/launch workflow",
        Stage.REPEAT: "sales-feedback workflow",
        Stage.SCALE: "scale decision workflow",
    }

    _OBJECTIVE = {
        Stage.MARKET: "establish verified market/demand evidence",
        Stage.PAIN: "establish recurring consumer pain from independent evidence",
        Stage.OPPORTUNITY: "convert verified pain into a bounded opportunity",
        Stage.PRODUCT_THESIS: "define the falsifiable product thesis",
        Stage.DEMAND_VALIDATION: "test willingness to pay / demand for the thesis",
        Stage.PRODUCT_SPEC: "turn the validated thesis into a buildable product spec",
        Stage.FORMULA: "define formula/prototype requirements",
        Stage.ECONOMICS: "prove target unit economics",
        Stage.MANUFACTURING: "secure feasible supplier/manufacturing path",
        Stage.PILOT: "run the smallest credible pilot",
        Stage.SALES: "reach first real sale",
        Stage.REPEAT: "prove repeat purchase",
        Stage.SCALE: "scale only after repeat economics are validated",
    }

    def plan(
        self,
        state: PipelineState,
        *,
        available_mechanisms: set[str] | None = None,
        paid_dependencies: dict[str, bool] | None = None,
    ) -> ExecutionPlan:
        stage = state.stage
        if stage == Stage.STOP:
            return ExecutionPlan(
                stage=stage,
                lane="NONE",
                mechanism="none",
                objective="project stopped",
                bottleneck="STOP",
                blocked=True,
                blocking_reason="Pipeline is in STOP state.",
                next_action="Resolve the failed/pivoted gate before resuming.",
            )

        lane = self._LANE.get(stage, "NONE")
        mechanism = self._MECHANISM.get(stage, "existing stage worker")
        available = available_mechanisms or set()
        paid = paid_dependencies or {}

        # The registry is the canonical capability → ready-mechanism boundary.
        # For capabilities with multiple implementations, prefer an explicitly
        # available mechanism; otherwise preserve registry order as the fallback.
        if stage in {Stage.MARKET, Stage.PAIN}:
            capability = (
                "amazon_product_discovery"
                if stage == Stage.MARKET
                else "review_pain_analysis"
            )
            registered = mechanisms_for(capability)
            if not registered:
                return ExecutionPlan(
                    stage=stage,
                    lane=lane,
                    mechanism=mechanism,
                    objective=self._OBJECTIVE[stage],
                    bottleneck=stage.value,
                    blocked=True,
                    blocking_reason="No ready mechanism is registered for this capability.",
                    next_action="Search and inspect an existing repository/skill/API/MCP before building custom functionality.",
                )
            available_registered = tuple(m for m in registered if m.name in available)
            mechanism = (
                available_registered[0].name
                if available_registered
                else registered[0].name
            )

        # The manager never assumes a paid provider is available.
        if stage == Stage.MARKET and mechanism not in available:
            return ExecutionPlan(
                stage=stage,
                lane=lane,
                mechanism=mechanism,
                objective=self._OBJECTIVE[stage],
                bottleneck="MARKET",
                blocked=True,
                blocking_reason="Finder workflow is not available to execute this gate.",
                next_action="Activate the existing Finder workflow or supply a verified equivalent.",
            )

        if stage == Stage.PAIN and mechanism not in available:
            return ExecutionPlan(
                stage=stage,
                lane=lane,
                mechanism=mechanism,
                objective=self._OBJECTIVE[stage],
                bottleneck="PAIN",
                blocked=True,
                blocking_reason=(
                    f"No registered review-pain mechanism is currently available "
                    f"to execute this gate (selected: {mechanism}; legacy capability: review-analysis)."
                ),
                next_action="Activate one registered review-pain mechanism; do not build a replacement.",
            )

        h10_required = stage in {Stage.MARKET, Stage.DEMAND_VALIDATION}
        h10_ready = paid.get("h10", False)
        if h10_required and not h10_ready:
            return ExecutionPlan(
                stage=stage,
                lane=lane,
                mechanism=mechanism,
                objective=self._OBJECTIVE[stage],
                bottleneck=stage.value,
                capital_required=0.0,
                blocked=True,
                blocking_reason="This gate has a quantitative H10 dependency that is not active.",
                next_action="Use verified Amazon-native evidence first; activate H10 only when the exact missing metric blocks the gate.",
                constraints={"quantitative_claims": "blocked_without_provider_verification"},
            )

        return ExecutionPlan(
            stage=stage,
            lane=lane,
            mechanism=mechanism,
            objective=self._OBJECTIVE.get(stage, "execute current gate"),
            bottleneck=stage.value,
            capital_required=0.0,
            next_action=f"Execute {mechanism} and return a validated AgentResult for {stage.value}.",
        )

    @staticmethod
    def can_route(result_decision: Decision) -> bool:
        """Only PASS may advance the business pipeline."""
        return result_decision == Decision.PASS
