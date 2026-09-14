"""Provider-independent interface between market data and FINDER."""

from __future__ import annotations

from typing import Any

from pipeline.contracts import AgentRequest
from pipeline.state import Stage


def build_request(
    candidates: list[dict[str, Any]],
    *,
    task_id: str = "market-discovery",
    agent_id: str = "finder",
    agent_version: str = "0.1.0",
    constraints: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
) -> AgentRequest:
    """Build the canonical MARKET request consumed by FINDER.

    Provider-specific payloads must already be normalized before reaching
    this boundary. This function performs no market scoring or validation.
    """
    if not isinstance(candidates, list):
        raise TypeError("candidates must be a list")

    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            raise TypeError(f"candidate at index {index} must be a dict")

    return AgentRequest(
        task_id=task_id,
        agent_id=agent_id,
        agent_version=agent_version,
        stage=Stage.MARKET,
        input={"candidates": candidates},
        constraints=constraints or {},
        evidence=evidence or [],
    )


class FinderInput:
    """Small facade keeping the FINDER input contract explicit."""

    def build(
        self,
        candidates: list[dict[str, Any]],
        *,
        task_id: str = "market-discovery",
        constraints: dict[str, Any] | None = None,
        evidence: list[dict[str, Any]] | None = None,
    ) -> AgentRequest:
        return build_request(
            candidates,
            task_id=task_id,
            constraints=constraints,
            evidence=evidence,
        )
