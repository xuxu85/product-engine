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


def test_runner_projects_business_state(tmp_path):
    runner = PipelineRunner(tmp_path / "state.json")

    business = runner.business_state(
        bottleneck="verified consumer pain/opportunity evidence",
        capital_required=0.0,
        next_action="execute product-review-analyze-skill",
    )

    assert business.stage == "IDEA"
    assert business.progress_percent == 0
    assert business.current_gate == "IDEA"
    assert business.bottleneck == "verified consumer pain/opportunity evidence"
    assert business.capital_required == 0.0
    assert business.next_action == "execute product-review-analyze-skill"
    assert business.status == "OPEN"
