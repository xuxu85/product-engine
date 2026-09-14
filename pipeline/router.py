from __future__ import annotations

from dataclasses import dataclass

from .contracts import AgentRequest, AgentResult
from .gates import next_stage
from .state import PipelineState, Stage


@dataclass
class Router:
    """Pure routing layer. It never executes an agent and never spends capital."""

    def apply(self, state: PipelineState, result: AgentResult) -> PipelineState:
        if state.stage == Stage.SCALE:
            raise ValueError("SCALE is terminal in the current v0.1 state machine")

        result.validate()
        expected = next_stage(state.stage, result.decision)

        if result.next_stage is not None and result.next_stage != expected:
            raise ValueError(
                f"Agent requested {result.next_stage.value}, "
                f"but gate policy requires {expected.value}"
            )

        state.record(result.decision, result.output)
        state.stage = expected
        return state


def route(request: AgentRequest, result: AgentResult) -> AgentRequest:
    """Convert an agent result into the canonical request for the next stage."""

    result.validate()

    expected = next_stage(request.stage, result.decision)

    if result.next_stage is not None and result.next_stage != expected:
        raise ValueError(
            f"Agent requested {result.next_stage.value}, "
            f"but gate policy requires {expected.value}"
        )

    if result.decision.value != "PASS":
        raise ValueError("route requires a PASS result")

    return AgentRequest(
        task_id=result.task_id or f"{request.task_id}:{expected.value.lower()}",
        agent_id=f"{expected.value.lower()}.input",
        agent_version=result.agent_version or request.agent_version,
        stage=expected,
        input=result.output,
        constraints=request.constraints,
        evidence=result.evidence,
    )
