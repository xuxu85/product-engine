from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .contracts import AgentRequest, AgentResult
from .manager import ExecutionPlan, ProjectManager
from .router import Router
from .state import Decision, PipelineState, Stage


class PipelineRunner:
    """Minimal deterministic runner. External mechanisms remain outside the package."""

    def __init__(self, state_path: str | Path = "runs/current/state.json") -> None:
        self.state_path = Path(state_path)
        self.manager = ProjectManager()
        self.router = Router()

    def load_state(self) -> PipelineState:
        if not self.state_path.exists():
            return PipelineState(stage=Stage.IDEA)
        data = json.loads(self.state_path.read_text(encoding="utf-8"))
        decision = data.get("decision")
        return PipelineState(
            stage=Stage(data["stage"]),
            decision=Decision(decision) if decision else None,
            payload=data.get("payload", {}),
            history=data.get("history", []),
        )

    def save_state(self, state: PipelineState) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(state)
        data["stage"] = state.stage.value
        data["decision"] = state.decision.value if state.decision else None
        self.state_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def plan(self, *, available_mechanisms=None, paid_dependencies=None) -> ExecutionPlan:
        """Return the PM plan without executing or spending capital."""
        return self.manager.plan(
            self.load_state(),
            available_mechanisms=available_mechanisms,
            paid_dependencies=paid_dependencies,
        )

    def request(self, *, available_mechanisms=None, paid_dependencies=None, input=None) -> AgentRequest:
        """Build the canonical request for the selected external mechanism."""
        state = self.load_state()
        plan = self.plan(
            available_mechanisms=available_mechanisms,
            paid_dependencies=paid_dependencies,
        )
        if plan.blocked:
            raise RuntimeError(plan.blocking_reason)
        return AgentRequest(
            stage=state.stage,
            input=input or {},
            constraints={
                "mechanism": plan.mechanism,
                "objective": plan.objective,
                "bottleneck": plan.bottleneck,
                "capital_required": plan.capital_required,
            },
            agent_id=plan.mechanism,
        )

    def apply(self, result: AgentResult) -> PipelineState:
        state = self.load_state()
        state = self.router.apply(state, result)
        self.save_state(state)
        return state
