"""Architecture-only synthetic E2E test.

This proves contracts and deterministic routing only.
Synthetic data MUST NOT be treated as market validation.
"""

from pipeline.contracts import AgentRequest, AgentResult
from pipeline.router import Router
from pipeline.state import Decision, PipelineState, Stage
from agents.finder.mock_agent import run as finder


def make_request(stage: Stage, payload: dict) -> AgentRequest:
    return AgentRequest(
        task_id=f"synthetic-{stage.value.lower()}",
        agent_id=f"fixture.{stage.value.lower()}",
        agent_version="0.1.0",
        stage=stage,
        input=payload,
        constraints={},
        evidence=[],
    )


def make_result(stage: Stage, next_stage: Stage) -> AgentResult:
    return AgentResult(
        task_id=f"synthetic-{stage.value.lower()}",
        agent_id=f"fixture.{stage.value.lower()}",
        agent_version="0.1.0",
        status="SUCCESS",
        decision=Decision.PASS,
        output={"fixture_stage": stage.value},
        evidence=[],
        confidence=1.0,
        invalidation_conditions=[
            f"FAIL if synthetic fixture for {stage.value} is used as real business evidence."
        ],
        next_stage=next_stage,
    )


def test_full_pipeline_market_to_scale():
    state = PipelineState(stage=Stage.MARKET)
    router = Router()

    result = finder(
        make_request(
            Stage.MARKET,
            {
                "candidates": [
                    {
                        "candidate_id": "synthetic-001",
                        "signal": "synthetic market signal",
                    }
                ]
            },
        )
    )

    state = router.apply(state, result)
    assert state.stage is Stage.PAIN

    chain = [
        (Stage.PAIN, Stage.OPPORTUNITY),
        (Stage.OPPORTUNITY, Stage.PRODUCT_THESIS),
        (Stage.PRODUCT_THESIS, Stage.DEMAND_VALIDATION),
        (Stage.DEMAND_VALIDATION, Stage.PRODUCT_SPEC),
        (Stage.PRODUCT_SPEC, Stage.FORMULA),
        (Stage.FORMULA, Stage.ECONOMICS),
        (Stage.ECONOMICS, Stage.MANUFACTURING),
        (Stage.MANUFACTURING, Stage.PILOT),
        (Stage.PILOT, Stage.SALES),
        (Stage.SALES, Stage.REPEAT),
        (Stage.REPEAT, Stage.SCALE),
    ]

    for stage, expected_next in chain:
        result = make_result(stage, expected_next)
        state = router.apply(state, result)
        assert state.stage is expected_next

    assert state.stage is Stage.SCALE
    assert len(state.history) == len(chain) + 1


def test_missing_input_does_not_pass():
    from agents.stage_workers import run_stage

    request = make_request(
        Stage.PRODUCT_THESIS,
        {},
    )

    result = run_stage(request)

    assert result.status == "ERROR"
    assert result.decision is Decision.FAIL
    assert result.next_stage is None
    assert result.invalidation_conditions


def test_wrong_next_stage_is_rejected():
    state = PipelineState(stage=Stage.OPPORTUNITY)
    router = Router()

    result = make_result(
        Stage.OPPORTUNITY,
        Stage.SALES,
    )

    try:
        router.apply(state, result)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Router must reject an agent next_stage that contradicts gate policy."
        )
