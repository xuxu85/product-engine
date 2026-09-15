from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .state import PipelineState, Stage


# Commercial progress is gate-based. It is intentionally not task-count based.
PROGRESS_BY_STAGE: dict[Stage, int] = {
    Stage.IDEA: 0,
    Stage.MARKET: 5,
    Stage.PAIN: 15,
    Stage.OPPORTUNITY: 20,
    Stage.PRODUCT_THESIS: 25,
    Stage.DEMAND_VALIDATION: 35,
    Stage.PRODUCT_SPEC: 45,
    Stage.FORMULA: 55,
    Stage.ECONOMICS: 65,
    Stage.MANUFACTURING: 75,
    Stage.PILOT: 85,
    Stage.SALES: 95,
    Stage.REPEAT: 98,
    Stage.SCALE: 100,
    Stage.STOP: 0,
}


@dataclass(frozen=True)
class BusinessState:
    """Read-only business projection derived from the canonical pipeline state."""

    stage: str
    last_decision: str | None
    progress_percent: int
    current_gate: str
    bottleneck: str
    capital_required: float
    next_action: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "last_decision": self.last_decision,
            "progress_percent": self.progress_percent,
            "current_gate": self.current_gate,
            "bottleneck": self.bottleneck,
            "capital_required": self.capital_required,
            "next_action": self.next_action,
            "status": self.status,
        }


def project_business_state(
    state: PipelineState,
    *,
    bottleneck: str = "",
    capital_required: float = 0.0,
    next_action: str = "",
) -> BusinessState:
    """Project pipeline truth into the small business-level view used by Notion.

    This function does not make a gate decision and does not invent evidence.
    """
    stage = state.stage
    decision = state.decision
    status = "STOPPED" if stage == Stage.STOP else (decision.value if decision else "OPEN")
    return BusinessState(
        stage=stage.value,
        last_decision=decision.value if decision else None,
        progress_percent=PROGRESS_BY_STAGE[stage],
        current_gate=stage.value,
        bottleneck=bottleneck,
        capital_required=capital_required,
        next_action=next_action,
        status=status,
    )
