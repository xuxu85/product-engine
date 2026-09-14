from pipeline.contracts import AgentRequest
from pipeline.state import Decision, Stage
from agents.pain.workflow import normalize_evidence, run


def test_normalize_evidence_maps_pain_to_canonical_shape():
    result = normalize_evidence([
        {"source": "Amazon", "pain": "product breaks quickly"},
    ])
    assert result[0]["pain_statement"] == "product breaks quickly"
    assert result[0]["source"] == "Amazon"


def test_pain_workflow_builds_opportunity_card():
    request = AgentRequest(
        stage=Stage.PAIN,
        input={"consumer": "busy parents", "target_price": 29.0},
        constraints={"minimum_evidence": 3},
        evidence=[
            {"source": "Amazon", "pain": "hard to clean", "intensity": 8},
            {"source": "Reddit", "pain": "hard to clean", "intensity": 7},
            {"source": "Interview", "pain": "hard to clean", "intensity": 9},
        ],
    )
    result = run(request)
    assert result.decision == Decision.PASS
    assert result.output["pain_verified"] is True
    assert result.output["opportunity"]["evidence_count"] == 3
    assert result.output["opportunity"]["pain"] == "hard to clean"
    assert result.output["opportunity"]["target_price"] == 29.0


def test_pain_workflow_fails_without_independent_sources():
    request = AgentRequest(
        stage=Stage.PAIN,
        input={},
        constraints={"minimum_evidence": 3},
        evidence=[
            {"source": "Amazon", "pain": "same issue"},
            {"source": "Amazon", "pain": "same issue"},
            {"source": "Amazon", "pain": "same issue"},
        ],
    )
    result = run(request)
    assert result.decision == Decision.FAIL
    assert result.output["pain_verified"] is False
