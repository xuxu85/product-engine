from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .state import Decision, Stage


@dataclass(frozen=True)
class AgentRequest:
    stage: Stage
    input: dict[str, Any]
    constraints: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class AgentResult:
    decision: Decision
    output: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    invalidation_conditions: list[str] = field(default_factory=list)
    next_stage: Stage | None = None

    def validate(self) -> None:
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
