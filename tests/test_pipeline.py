from pipeline.contracts import AgentResult, ProductSpec
from pipeline.gates import next_stage
from pipeline.policy import capital_allowed
from pipeline.router import Router
from pipeline.state import Decision, PipelineState, Stage


def test_pass_moves_forward():
    state = PipelineState(stage=Stage.PAIN)
    Router().apply(
        state,
        AgentResult(
            decision=Decision.PASS,
            output={"pain_verified": True},
            invalidation_conditions=["fewer than 3 independent evidence sources"],
        ),
    )
    assert state.stage == Stage.OPPORTUNITY


def test_fail_does_not_jump_forward():
    assert next_stage(Stage.PRODUCT_THESIS, Decision.FAIL) == Stage.OPPORTUNITY


def test_agent_cannot_override_gate_router():
    state = PipelineState(stage=Stage.PAIN)
    result = AgentResult(
        decision=Decision.PASS,
        next_stage=Stage.SALES,
        invalidation_conditions=["test"],
    )
    try:
        Router().apply(state, result)
    except ValueError as exc:
        assert "gate policy" in str(exc)
    else:
        raise AssertionError("Router accepted an invalid next_stage")


def test_invalidation_condition_is_required():
    result = AgentResult(decision=Decision.PASS)
    try:
        result.validate()
    except ValueError as exc:
        assert "invalidation" in str(exc)
    else:
        raise AssertionError("Missing invalidation condition was accepted")


def test_product_spec_economics_guard():
    spec = ProductSpec(
        product="test product",
        consumer="test consumer",
        problem="test problem",
        use_case="test use case",
        required_modification="none",
        bundle=(),
        target_price=30,
        max_landed_cost=10,
        initial_quantity=10,
        market="Amazon.es",
        validation_method="preorder",
        invalidation_condition="fewer than 5 paid orders",
    )
    spec.validate()


def test_capital_policy_blocks_meaningful_pre_validation_spend():
    assert capital_allowed(Stage.PRODUCT_THESIS, 250)
    assert not capital_allowed(Stage.PRODUCT_THESIS, 251)
    assert capital_allowed(Stage.FORMULA, 10000)
