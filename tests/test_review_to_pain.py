from agents.pain.adapters.review_evidence import reviews_to_evidence
from agents.pain.workflow import run
from pipeline.contracts import AgentRequest
from pipeline.state import Decision, Stage


def test_amazon_reviews_can_enter_pain_gate_without_pretending_cross_source_validation():
    reviews = {
        "ASIN-001": {
            "critical": [
                {"source": "Amazon", "title": "Breaks quickly", "body": "Stopped working after two weeks.", "intensity": 8},
                {"source": "Amazon", "title": "Poor durability", "body": "Material tore on the second trip.", "intensity": 7},
            ]
        },
        "ASIN-002": {
            "critical": [
                {"source": "Amazon", "title": "Breaks quickly", "body": "Stopped working after a short time.", "intensity": 9},
            ]
        },
    }

    evidence = reviews_to_evidence(reviews)
    request = AgentRequest(
        stage=Stage.PAIN,
        input={"consumer": "Amazon category consumer", "target_price": 29.0},
        constraints={"minimum_evidence": 3, "minimum_independent_sources": 1},
        evidence=evidence,
    )

    result = run(request)

    assert result.decision == Decision.PASS
    assert result.output["pain_verified"] is True
    assert result.output["opportunity"]["evidence_count"] == 3
    assert result.output["opportunity"]["evidence_sources"] == ["Amazon"]
    assert "willingness to pay" in " ".join(result.invalidation_conditions).lower()
