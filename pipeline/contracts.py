from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .state import Decision, Stage


def _coerce_stage(value: Stage | str | None, *, field_name: str) -> Stage | None:
    if value is None:
        return None
    if isinstance(value, Stage):
        return value
    try:
        return Stage(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid Stage") from exc


def _coerce_decision(value: Decision | str) -> Decision:
    if isinstance(value, Decision):
        return value
    try:
        return Decision(value)
    except ValueError as exc:
        raise ValueError("decision must be a valid Decision") from exc


@dataclass(frozen=True)
class AgentRequest:
    stage: Stage
    input: dict[str, Any]
    constraints: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    task_id: str = ""
    agent_id: str = ""
    agent_version: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage", _coerce_stage(self.stage, field_name="stage"))
        if not isinstance(self.input, dict):
            raise TypeError("input must be a dict")


@dataclass(frozen=True)
class AgentResult:
    decision: Decision
    output: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    invalidation_conditions: list[str] = field(default_factory=list)
    next_stage: Stage | None = None
    task_id: str = ""
    agent_id: str = ""
    agent_version: str = ""
    status: str = "SUCCESS"
    confidence: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision", _coerce_decision(self.decision))
        object.__setattr__(
            self,
            "next_stage",
            _coerce_stage(self.next_stage, field_name="next_stage"),
        )
        if not isinstance(self.output, dict):
            raise TypeError("output must be a dict")
        if not isinstance(self.invalidation_conditions, list):
            raise TypeError("invalidation_conditions must be a list")

    def validate(self) -> None:
        if self.status not in {"SUCCESS", "ERROR"}:
            raise ValueError("status must be SUCCESS or ERROR")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.invalidation_conditions:
            raise ValueError("Every gate result must define at least one invalidation condition")


@dataclass(frozen=True)
class ProductSpec:
    product: str
    consumer: str
    problem: str
    use_case: str
    required_modification: str
    bundle: tuple[str, ...]
    target_price: float
    max_landed_cost: float
    initial_quantity: int
    market: str
    validation_method: str
    invalidation_condition: str

    def validate(self) -> None:
        if self.target_price <= 0:
            raise ValueError("target_price must be > 0")
        if self.max_landed_cost <= 0:
            raise ValueError("max_landed_cost must be > 0")
        if self.max_landed_cost >= self.target_price:
            raise ValueError("max_landed_cost must be below target_price")
        if self.initial_quantity <= 0:
            raise ValueError("initial_quantity must be > 0")
        if not self.invalidation_condition.strip():
            raise ValueError("ProductSpec requires an invalidation condition")
