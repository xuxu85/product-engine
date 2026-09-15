from adapters.browseract.reviews import critical_reviews, extract_output


def test_extract_output_decodes_json_string():
    task = {"output": {"string": '[{"Rating": 1, "review Description": "bad"}]'}}
    assert extract_output(task)[0]["Rating"] == 1


def test_critical_reviews_keeps_only_one_and_two_star_records():
    reviews = [
        {"Rating": 5, "review Description": "great"},
        {"Rating": 2, "review Description": "poor"},
        {"Rating": 1, "review Description": "terrible"},
    ]
    result = critical_reviews(reviews)
    assert [item["Rating"] for item in result] == [2, 1]


def test_critical_reviews_does_not_make_business_conclusions():
    result = critical_reviews([{"Rating": 1, "review Description": "bad"}])
    assert "pain" not in result[0]
    assert "decision" not in result[0]
