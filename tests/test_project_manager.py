from core.project_manager import ProjectManager


def test_pain_uses_existing_review_workflow():
    d = ProjectManager().plan("PAIN")
    assert d.lane == "FINDER"
    assert d.status == "OPEN"
    assert d.execution_mechanism == "product-review-analyze-skill"


def test_missing_provider_blocks_only_dependent_work():
    d = ProjectManager().plan("DEMAND_VALIDATION", required_provider_ready=False)
    assert d.status == "BLOCKED"
    assert d.capital_required == 0.0
    assert "exact missing function" in d.next_action


def test_ready_gate_routes_forward():
    d = ProjectManager().plan("PAIN", evidence_ready=True)
    assert d.status == "PASS"
    assert "next gate" in d.next_action.lower()
