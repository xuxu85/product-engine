"""Registry for reusable research mechanisms.

The Product Engine does not implement provider-specific research when a ready
mechanism already exists. This registry records the capability boundary so the
Project Manager can select/reuse a mechanism before requesting custom work.
"""
from dataclasses import dataclass
from typing import Literal


MechanismStatus = Literal["AVAILABLE", "DEPENDENCY_REQUIRED", "NOT_VERIFIED"]


@dataclass(frozen=True)
class Mechanism:
    name: str
    function: str
    lane: str
    input_type: str
    output_type: str
    status: MechanismStatus
    dependency: str | None = None
    repository: str | None = None


READY_MECHANISMS = (
    Mechanism(
        name="product-opportunity-finder-skill",
        function="amazon_product_discovery",
        lane="FINDER",
        input_type="market/category/search scope",
        output_type="candidate products + demand/rankability signals",
        status="DEPENDENCY_REQUIRED",
        dependency="Amazon browser session; H10 optional/required for H10-dependent metrics",
        repository="AronLEEdev/product-opportunity-finder-skill",
    ),
    Mechanism(
        name="helium10-mcp-review-insights",
        function="review_pain_analysis",
        lane="FINDER",
        input_type="Amazon ASIN or category/niche + marketplace",
        output_type="review insights: rating distribution + sentiment + keywords + complaint themes + improvement priorities",
        status="DEPENDENCY_REQUIRED",
        dependency="Helium 10 Diamond+ MCP access/OAuth",
        repository="helium10/Helium10-MCP",
    ),
    Mechanism(
        name="product-review-analyze-skill",
        function="review_pain_analysis",
        lane="FINDER",
        input_type="product/review corpus",
        output_type="review themes + pain clusters + evidence",
        status="AVAILABLE",
        repository="AronLEEdev/product-review-analyze-skill",
    ),
    Mechanism(
        name="product-research-skills",
        function="amazon_product_research",
        lane="FINDER",
        input_type="research brief",
        output_type="structured Amazon research",
        status="NOT_VERIFIED",
        repository="AronLEEdev/product-research-skills",
    ),
    Mechanism(
        name="helium10-mcp",
        function="helium10_data_access",
        lane="FINDER",
        input_type="H10 research request",
        output_type="verified H10 metrics",
        status="DEPENDENCY_REQUIRED",
        dependency="H10 MCP access/credentials and applicable plan",
        repository="helium10/Helium10-MCP",
    ),
)


def mechanisms_for(function: str) -> tuple[Mechanism, ...]:
    """Return registered mechanisms for one exact capability."""
    return tuple(m for m in READY_MECHANISMS if m.function == function)


def require_ready_mechanism(function: str) -> Mechanism:
    """Select the first registered mechanism; fail loudly if none exists."""
    matches = mechanisms_for(function)
    if not matches:
        raise LookupError(
            f"No ready mechanism registered for capability={function!r}. "
            "Search repositories/tools before implementing custom functionality."
        )
    return matches[0]
