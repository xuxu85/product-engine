from agents.pain.adapters.review_evidence import reviews_to_evidence


def test_three_critical_reviews_become_three_customer_evidence_records():
    reviews = {
        "ASIN-001": {
            "critical": [
                {
                    "source": "Amazon",
                    "source_url": "https://amazon.es/review/1",
                    "consumer_context": "daily use",
                    "title": "Breaks quickly",
                    "body": "It stopped working after two weeks.",
                    "intensity": 8,
                    "frequency_signal": "repeated",
                },
                {
                    "source": "Amazon",
                    "source_url": "https://amazon.es/review/2",
                    "consumer_context": "travel",
                    "title": "Poor durability",
                    "body": "The material tore on the second trip.",
                    "intensity": 7,
                    "frequency_signal": "repeated",
                },
            ]
        },
        "ASIN-002": {
            "critical": [
                {
                    "source": "Amazon",
                    "source_url": "https://amazon.es/review/3",
                    "consumer_context": "home use",
                    "title": "Difficult to clean",
                    "body": "Cleaning takes much longer than expected.",
                    "intensity": 6,
                    "frequency_signal": "repeated",
                }
            ]
        },
    }

    evidence = reviews_to_evidence(reviews)

    assert len(evidence) == 3
    assert all(item["source"] == "Amazon" for item in evidence)
    assert all(item["pain_statement"] for item in evidence)
    assert all(item["verbatim"] for item in evidence)
    assert {item["item_id"] for item in evidence} == {"ASIN-001", "ASIN-002"}


def test_non_critical_reviews_are_not_promoted_to_customer_evidence():
    reviews = {
        "ASIN-001": {
            "critical": [],
            "positive": [{"title": "Great", "body": "Works well."}],
        }
    }

    assert reviews_to_evidence(reviews) == []


def test_empty_review_is_skipped():
    reviews = {"ASIN-001": {"critical": [{"title": "", "body": ""}]}}

    assert reviews_to_evidence(reviews) == []
