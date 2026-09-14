from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Stage(StrEnum):
    IDEA = "IDEA"
    MARKET = "MARKET"
    PAIN = "PAIN"
    OPPORTUNITY = "OPPORTUNITY"
    PRODUCT_THESIS = "PRODUCT_THESIS"
    DEMAND_VALIDATION = "DEMAND_VALIDATION"
    PRODUCT_SPEC = "PRODUCT_SPEC"
    FORMULA = "FORMULA"
    ECONOMICS = "ECONOMICS"
    MANUFACTURING = "MANUFACTURING"
    PILOT = "PILOT"
    SALES = "SALES"
    REPEAT = "REPEAT"
    SCALE = "SCALE"
    STOP = "STOP"


class Decision(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    PIVOT = "PIVOT"


@dataclass
class PipelineState:
    stage: Stage = Stage.IDEA
    decision: Decision | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def record(self, decision: Decision, output: dict[str, Any] | None = None) -> None:
        self.decision = decision
        self.history.append(
            {
                "stage": self.stage.value,
                "decision": decision.value,
                "output": output or {},
            }
        )
        if output:
            self.payload.update(output)
