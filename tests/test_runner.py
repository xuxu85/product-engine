import json

from pipeline.contracts import AgentResult
from pipeline.runner import PipelineRunner
from pipeline.state import Decision, Stage


def test_runner_persists_and_reloads_state(tmp_path):
    path = tmp_path / "state.json"
    runner = PipelineRunner(path)

    state = runner.apply(
        AgentResult(
            decision=Decision.PASS,
            output={"pain_verified": True},
            invalidation_conditions=["fewer than 3 independent evidence sources"],
        )
    )

    assert state.stage == Stage.MARKET
    saved = json.loads(path.read_text())
    assert saved["stage"] == "MARKET"
    assert saved["decision"] == "PASS"

    reloaded = PipelineRunner(path).load_state()
    assert reloaded.stage == Stage.MARKET
    assert reloaded.decision == Decision.PASS
    assert reloaded.history[-1]["decision"] == "PASS"
