from __future__ import annotations

from .state import Stage

# Maximum amount that may be spent before willingness-to-pay evidence is established.
# This is intentionally a policy input, not a hard-coded business budget.
DEFAULT_VALIDATION_BUDGET = 250.0


def capital_allowed(stage: Stage, amount: float, validation_budget: float = DEFAULT_VALIDATION_BUDGET) -> bool:
    if amount < 0:
        raise ValueError("capital amount cannot be negative")
    if stage in {
        Stage.IDEA,
        Stage.MARKET,
        Stage.PAIN,
        Stage.OPPORTUNITY,
        Stage.PRODUCT_THESIS,
    }:
        return amount <= validation_budget
    if stage == Stage.DEMAND_VALIDATION:
        return amount <= validation_budget
    # Meaningful capital becomes eligible only after demand validation passes.
    return True
