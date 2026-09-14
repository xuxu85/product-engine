from agents.pain.adapters.review_run import convert_reviews_to_evidence
from agents.pain.workflow import run as run_pain_workflow
from pipeline.contracts import AgentRequest
from pipeline.state import Stage, Decision


def test_review_skill_output_enters_pain_workflow_without_bypassing_gate(tmp_path):
    raw_path = tmp_path / "reviews-raw.json"
    evidence_path = tmp_path / "customer-evidence.json"
    raw_path.write_text(
        '{"ASIN-001":{"critical":[{"title":"Bad taste","body":"The taste is unpleasant."}]},'
        '"ASIN-002":{"critical":[{"title":"Bad taste","body":"The taste is unpleasant."}]}}',
        encoding="utf-8",
    )

    evidence = convert_reviews_to_evidence(raw_path, evidence_path)
    request = AgentRequest(
        stage=Stage.PAIN,
        input={"consumer": "electrolyte water buyer"},
        constraints={"minimum_evidence": 3, "minimum_independent_sources": 3},
        evidence=evidence,
        agent_id="product-review-analyze-skill",
    )

    result = run_pain_workflow(request)

    assert result.decision is Decision.FAIL
    assert result.output["pain_verified"] is False
    assert result.agent_id == "pain.workflow"
