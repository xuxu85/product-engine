from __future__ import annotations

from .state import Decision, Stage

# Explicit transition policy. The core owns routing; agents only return decisions.
TRANSITIONS: dict[Stage, dict[Decision, Stage]] = {
    Stage.IDEA: {
        Decision.PASS: Stage.MARKET,
        Decision.FAIL: Stage.STOP,
        Decision.PIVOT: Stage.IDEA,
    },
    Stage.MARKET: {
        Decision.PASS: Stage.PAIN,
        Decision.FAIL: Stage.STOP,
        Decision.PIVOT: Stage.MARKET,
    },
    Stage.PAIN: {
        Decision.PASS: Stage.OPPORTUNITY,
        Decision.FAIL: Stage.MARKET,
        Decision.PIVOT: Stage.MARKET,
    },
    Stage.OPPORTUNITY: {
        Decision.PASS: Stage.PRODUCT_THESIS,
        Decision.FAIL: Stage.PAIN,
        Decision.PIVOT: Stage.PAIN,
    },
    Stage.PRODUCT_THESIS: {
        Decision.PASS: Stage.DEMAND_VALIDATION,
        Decision.FAIL: Stage.OPPORTUNITY,
        Decision.PIVOT: Stage.OPPORTUNITY,
    },
    Stage.DEMAND_VALIDATION: {
        Decision.PASS: Stage.PRODUCT_SPEC,
        Decision.FAIL: Stage.PRODUCT_THESIS,
        Decision.PIVOT: Stage.PRODUCT_THESIS,
    },
    Stage.PRODUCT_SPEC: {
        Decision.PASS: Stage.FORMULA,
        Decision.FAIL: Stage.PRODUCT_THESIS,
        Decision.PIVOT: Stage.PRODUCT_THESIS,
    },
    Stage.FORMULA: {
        Decision.PASS: Stage.ECONOMICS,
        Decision.FAIL: Stage.PRODUCT_SPEC,
        Decision.PIVOT: Stage.PRODUCT_SPEC,
    },
    Stage.ECONOMICS: {
        Decision.PASS: Stage.MANUFACTURING,
        Decision.FAIL: Stage.PRODUCT_SPEC,
        Decision.PIVOT: Stage.PRODUCT_SPEC,
    },
    Stage.MANUFACTURING: {
        Decision.PASS: Stage.PILOT,
        Decision.FAIL: Stage.PRODUCT_SPEC,
        Decision.PIVOT: Stage.PRODUCT_SPEC,
    },
    Stage.PILOT: {
        Decision.PASS: Stage.SALES,
        Decision.FAIL: Stage.MANUFACTURING,
        Decision.PIVOT: Stage.PRODUCT_SPEC,
    },
    Stage.SALES: {
        Decision.PASS: Stage.REPEAT,
        Decision.FAIL: Stage.DEMAND_VALIDATION,
        Decision.PIVOT: Stage.PRODUCT_SPEC,
    },
    Stage.REPEAT: {
        Decision.PASS: Stage.SCALE,
        Decision.FAIL: Stage.SALES,
        Decision.PIVOT: Stage.PRODUCT_SPEC,
    },
}


def next_stage(stage: Stage, decision: Decision) -> Stage:
    try:
        return TRANSITIONS[stage][decision]
    except KeyError as exc:
        raise ValueError(f"No transition defined for {stage.value} / {decision.value}") from exc
