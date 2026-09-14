from adapters.h10.adapter import normalize
from agents.finder.interface import FinderInput, build_request
from agents.finder.mock_agent import run as finder
from pipeline.state import Stage


def test_normalized_provider_data_builds_market_request():
    payload = {
        "products": [
            {
                "ASIN": "B000TEST01",
                "market": "amazon.es",
                "product_title": "Synthetic Product",
                "current_price": 24.99,
                "estimated_monthly_sales": 1200,
                "estimated_monthly_revenue": 29988,
                "number_of_reviews": 340,
                "stars": 4.3,
                "provider": "h10",
            }
        ]
    }

    candidates = normalize(payload)
    request = build_request(candidates)

    assert request.stage is Stage.MARKET
    assert request.input["candidates"][0]["asin"] == "B000TEST01"
    assert request.input["candidates"][0]["monthly_sales"] == 1200


def test_finder_accepts_provider_independent_request():
    request = FinderInput().build(
        [
            {
                "candidate_id": "c-1",
                "marketplace": "amazon.es",
                "asin": "B001",
                "title": "Product",
                "price": 19.0,
                "monthly_sales": 500,
                "monthly_revenue": 9500,
                "review_count": 100,
                "rating": 4.5,
                "source": "h10",
            }
        ]
    )

    result = finder(request)

    assert result.status == "SUCCESS"
    assert result.decision.value == "PASS"
    assert result.next_stage.value == "PAIN"
    assert result.output["candidates"][0]["asin"] == "B001"


def test_finder_interface_rejects_non_list_candidates():
    try:
        build_request({"not": "a list"})
    except TypeError as exc:
        assert "candidates must be a list" in str(exc)
    else:
        raise AssertionError("Finder interface must reject non-list candidates")
