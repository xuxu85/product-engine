from pipeline.manager import ProjectManager
from pipeline.state import PipelineState, Stage, Decision


def test_pain_selects_review_workflow():
    plan = ProjectManager().plan(
        PipelineState(stage=Stage.PAIN),
        available_mechanisms={"product-review-analyze-skill"},
    )
    assert plan.blocked is False
    assert plan.lane == "FINDER"
    assert plan.mechanism == "product-review-analyze-skill"
    assert plan.bottleneck == "PAIN"


def test_pain_blocks_when_review_mechanism_missing():
    plan = ProjectManager().plan(PipelineState(stage=Stage.PAIN))
    assert plan.blocked is True
    assert "review-analysis" in plan.blocking_reason.lower()


def test_market_does_not_fake_h10_when_not_active():
    plan = ProjectManager().plan(
        PipelineState(stage=Stage.MARKET),
        available_mechanisms={"product-opportunity-finder-skill"},
        paid_dependencies={"h10": False},
    )
    assert plan.blocked is True
    assert plan.capital_required == 0.0
    assert "h10" in plan.blocking_reason.lower()


def test_pass_is_the_only_advancing_decision():
    assert ProjectManager.can_route(Decision.PASS) is True
    assert ProjectManager.can_route(Decision.FAIL) is False
    assert ProjectManager.can_route(Decision.PIVOT) is False
