from adapters.h10.adapter import H10Adapter, normalize


def sample_record():
    return {
        "ASIN": "B0SYNTH001",
        "market": "Amazon.es",
        "product_title": "Synthetic Product",
        "current_price": 29.99,
        "estimated_monthly_sales": 1200,
        "estimated_monthly_revenue": 35988,
        "number_of_reviews": 84,
        "stars": 4.3,
        "provider": "h10",
        "metrics": {"competition": 0.42},
    }


def test_h10_adapter_normalizes_provider_shape():
    result = normalize({"results": [sample_record()]})

    assert len(result) == 1
    candidate = result[0]
    assert candidate["candidate_id"] == "B0SYNTH001"
    assert candidate["asin"] == "B0SYNTH001"
    assert candidate["marketplace"] == "Amazon.es"
    assert candidate["price"] == 29.99
    assert candidate["monthly_sales"] == 1200
    assert candidate["monthly_revenue"] == 35988
    assert candidate["review_count"] == 84
    assert candidate["rating"] == 4.3
    assert candidate["source"] == "h10"
    assert candidate["metrics"]["competition"] == 0.42


def test_h10_adapter_supports_facade():
    adapter = H10Adapter()
    result = adapter.normalize({"products": [sample_record()]})
    assert result[0]["asin"] == "B0SYNTH001"


def test_h10_adapter_rejects_missing_required_fields():
    broken = sample_record()
    broken.pop("current_price")

    try:
        normalize({"candidates": [broken]})
    except ValueError as exc:
        assert "price" in str(exc)
    else:
        raise AssertionError("Adapter must reject incomplete provider records")


def test_h10_adapter_does_not_infer_business_conclusions():
    candidate = normalize({"candidates": [sample_record()]})[0]

    assert "pain" not in candidate
    assert "demand_validation" not in candidate
    assert "willingness_to_pay" not in candidate
