from agents.finder.interface import FinderInput
from agents.finder.mock_agent import run as run_finder
from agents.pain.workflow import run as run_pain
from adapters.h10.adapter import H10Adapter
from pipeline.router import route
from pipeline.state import Decision, Stage


def test_h10_to_opportunity_synthetic_e2e():
    raw = {
        "candidates": [
            {"asin": "B001", "title": "Example Product", "source": "synthetic"},
            {"asin": "B002", "title": "Example Product 2", "source": "synthetic"},
        ]
    }
    normalized = H10Adapter().normalize(raw)
    request = FinderInput().build(normalized["candidates"], evidence=normalized["evidence"])
    finder_result = run_finder(request)
    assert finder_result.decision == Decision.PASS
    assert finder_result.next_stage == Stage.PAIN

    pain_request = route(request, finder_result)
    pain_result = run_pain(pain_request)
    assert pain_result.decision in {Decision.PASS, Decision.FAIL}
