from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .contracts import AgentRequest, AgentResult
from .router import apply_result
from .state import PipelineState, Stage


class PipelineRunner:
    """Minimal deterministic runner. Agents remain external to this package."""

    def __init__(self, state_path: str | Path = "runs/current/state.json") -> None:
        self.state_path = Path(state_path)

    def load_state(self) -> PipelineState:
        if not self.state_path.exists():
            return PipelineState(stage=Stage.IDEA)
        data = json.loads(self.state_path.read_text(encoding="utf-8"))
        return PipelineState(
            stage=Stage(data["stage"]),
            decision=data.get("decision"),
            payload=data.get("payload", {}),
            history=data.get("history", []),
        )

    def save_state(self, state: PipelineState) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(state)
        data["stage"] = state.stage.value
        if state.decision is not None:
            data["decision"] = state.decision.value
        self.state_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def apply(self, result: AgentResult) -> PipelineState:
        state = self.load_state()
        state = apply_result(state, result)
        self.save_state(state)
        return state
