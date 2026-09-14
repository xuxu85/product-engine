from pipeline.contracts import AgentRequest
from pipeline.runner import PipelineRunner
from pipeline.state import Stage
from agents.pain.mock_agent import run as run_pain_agent


def test_pain_mock_agent_routes_to_opportunity(tmp_path):
    runner = PipelineRunner(tmp_path / "state.json")
    state = runner.load_state()
    state.stage = Stage.PAIN
    runner.save_state(state)

    request = AgentRequest(
        stage=Stage.PAIN,
        input={"category": "example"},
        constraints={"minimum_evidence": 3},
        evidence=[
            {"source": "Amazon", "pain": "recurring issue"},
            {"source": "Reddit", "pain": "recurring issue"},
            {"source": "Interview", "pain": "recurring issue"},
        ],
    )

    result = run_pain_agent(request)
    final_state = runner.apply(result)

    assert result.decision.value == "PASS"
    assert result.output["pain_verified"] is True
    assert final_state.stage == Stage.OPPORTUNITY
    assert final_state.decision.value == "PASS"
    assert final_state.history[-1]["stage"] == "PAIN"
    assert final_state.history[-1]["decision"] == "PASS"
