from adapters.h10.adapter import H10Adapter
from agents.finder.interface import FinderInput
from agents.finder.mock_agent import run as finder
from pipeline.router import Router
from pipeline.state import PipelineState, Stage


def test_h10_like_payload_flows_through_adapter_finder_and_router():
    provider_payload = {
        "products": [
            {
                "ASIN": "B00E2E001",
                "market": "amazon.es",
                "product_title": "Synthetic Consumer Product",
                "current_price": 29.90,
                "estimated_monthly_sales": 850,
                "estimated_monthly_revenue": 25415,
                "number_of_reviews": 210,
                "stars": 4.2,
                "provider": "h10",
            }
        ]
    }

    candidates = H10Adapter().normalize(provider_payload)
    request = FinderInput().build(candidates, task_id="e2e-provider-finder")
    result = finder(request)

    assert result.status == "SUCCESS"
    assert result.decision.value == "PASS"
    assert result.output["candidates"][0]["asin"] == "B00E2E001"

    state = PipelineState(stage=Stage.MARKET)
    state = Router().apply(state, result)

    assert state.stage is Stage.PAIN
    assert state.history[-1]["stage"] == "MARKET"
    assert state.history[-1]["decision"] == "PASS"


def test_provider_adapter_remains_business_neutral():
    payload = {
        "results": [
            {
                "asin": "B00NEUTRAL",
                "marketplace": "amazon.es",
                "title": "Neutral Product",
                "price": 20.0,
                "monthly_sales": 100,
                "monthly_revenue": 2000,
                "review_count": 20,
                "rating": 4.0,
                "source": "h10",
            }
        ]
    }

    candidate = H10Adapter().normalize(payload)[0]

    assert set(candidate).issuperset(
        {
            "candidate_id",
            "marketplace",
            "asin",
            "title",
            "price",
            "monthly_sales",
            "monthly_revenue",
            "review_count",
            "rating",
            "source",
        }
    )
    assert "pain" not in candidate
    assert "opportunity" not in candidate
    assert "willingness_to_pay" not in candidate
