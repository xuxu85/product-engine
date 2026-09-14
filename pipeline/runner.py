from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .contracts import AgentResult
from .router import Router
from .state import Decision, PipelineState, Stage


class PipelineRunner:
    """Minimal deterministic runner. Agents remain external to this package."""

    def __init__(self, state_path: str | Path = "runs/current/state.json") -> None:
        self.state_path = Path(state_path)
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

    def apply(self, result: AgentResult) -> PipelineState:
        state = self.load_state()
        state = self.router.apply(state, result)
        self.save_state(state)
        return state
