from pipeline.runner import PipelineRunner
from pipeline.state import PipelineState, Stage


def test_runner_builds_request_from_pm_plan(tmp_path):
    runner = PipelineRunner(tmp_path / "state.json")
    runner.save_state(PipelineState(stage=Stage.PAIN))

    request = runner.request(
        available_mechanisms={"product-review-analyze-skill"},
        input={"scope": "electrolyte water"},
    )

    assert request.stage == Stage.PAIN
    assert request.agent_id == "product-review-analyze-skill"
    assert request.input == {"scope": "electrolyte water"}
    assert request.constraints["mechanism"] == "product-review-analyze-skill"
    assert request.constraints["bottleneck"] == "PAIN"


def test_runner_refuses_blocked_plan(tmp_path):
    runner = PipelineRunner(tmp_path / "state.json")
    runner.save_state(PipelineState(stage=Stage.PAIN))

    try:
        runner.request()
    except RuntimeError as exc:
        assert "review-analysis" in str(exc).lower()
    else:
        raise AssertionError("runner must refuse a blocked execution plan")
