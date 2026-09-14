import pytest

from pipeline.contracts import AgentRequest, AgentResult
from pipeline.state import Decision, Stage


def test_agent_request_coerces_stage_string():
    request = AgentRequest(stage="MARKET", input={})
    assert request.stage is Stage.MARKET


def test_agent_result_coerces_decision_and_next_stage_strings():
    result = AgentResult(
        decision="PASS",
        next_stage="PAIN",
        invalidation_conditions=["fewer than 3 independent pain signals"],
    )
    assert result.decision is Decision.PASS
    assert result.next_stage is Stage.PAIN


def test_agent_result_rejects_invalid_decision():
    with pytest.raises(ValueError, match="decision must be a valid Decision"):
        AgentResult(
            decision="MAYBE",
            invalidation_conditions=["invalid"],
        )


def test_agent_result_rejects_invalid_next_stage():
    with pytest.raises(ValueError, match="next_stage must be a valid Stage"):
        AgentResult(
            decision=Decision.PASS,
            next_stage="NOT_A_STAGE",
            invalidation_conditions=["invalid"],
        )
