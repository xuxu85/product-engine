from adapters.h10.adapter import H10Adapter, normalize


def sample_payload():
    return {
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


def test_h10_payload_normalizes_to_canonical_candidate():
    candidates = normalize(sample_payload())

    assert len(candidates) == 1
    candidate = candidates[0]

    assert candidate["candidate_id"] == "B000TEST01"
    assert candidate["marketplace"] == "amazon.es"
    assert candidate["asin"] == "B000TEST01"
    assert candidate["title"] == "Synthetic Product"
    assert candidate["price"] == 24.99
    assert candidate["monthly_sales"] == 1200
    assert candidate["monthly_revenue"] == 29988
    assert candidate["review_count"] == 340
    assert candidate["rating"] == 4.3
    assert candidate["source"] == "h10"


def test_adapter_accepts_candidates_shape():
    payload = {
        "candidates": [
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
    }

    assert H10Adapter().normalize(payload)[0]["asin"] == "B001"


def test_missing_required_field_is_rejected():
    payload = {
        "products": [
            {
                "ASIN": "B002",
                "marketplace": "amazon.es",
                "title": "Incomplete",
                "price": 10,
                "monthly_sales": 10,
                "monthly_revenue": 100,
                "review_count": 1,
                "rating": 4.0,
            }
        ]
    }

    try:
        normalize(payload)
    except ValueError as exc:
        assert "source" in str(exc)
    else:
        raise AssertionError("Incomplete provider records must be rejected")


def test_adapter_does_not_infer_business_conclusions():
    candidate = normalize(sample_payload())[0]

    assert "pain" not in candidate
    assert "demand_validation" not in candidate
    assert "willingness_to_pay" not in candidate
    assert "product_market_fit" not in candidate
