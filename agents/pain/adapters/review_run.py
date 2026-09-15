from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipeline.contracts import AgentRequest

from .review_evidence import reviews_to_evidence


def load_reviews(path: str | Path) -> dict[str, dict[str, Any]]:
    """Load structured review-analysis output produced by an upstream workflow."""
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError("Review input must be a JSON object keyed by item/ASIN.")

    return payload


def convert_reviews_to_evidence(
    input_path: str | Path,
    output_path: str | Path,
) -> list[dict[str, Any]]:
    """Convert upstream review output into canonical CUSTOMER EVIDENCE."""
    reviews = load_reviews(input_path)
    evidence = reviews_to_evidence(reviews)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(evidence, handle, ensure_ascii=False, indent=2)

    return evidence


def request_from_review_output(
    request: AgentRequest,
    input_path: str | Path,
) -> AgentRequest:
    """Attach converted review evidence to the canonical PAIN request.

    The upstream review skill remains responsible for collection and analysis;
    this adapter only translates its structured artifact into our contract.
    """
    evidence = reviews_to_evidence(load_reviews(input_path))
    return AgentRequest(
        stage=request.stage,
        input=request.input,
        constraints=request.constraints,
        evidence=evidence,
        task_id=request.task_id,
        agent_id=request.agent_id,
        agent_version=request.agent_version,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert Amazon review-analysis output into CUSTOMER EVIDENCE."
    )
    parser.add_argument(
        "input",
        help="Path to reviews-raw.json or equivalent structured review output.",
    )
    parser.add_argument(
        "output",
        help="Path for canonical customer-evidence.json.",
    )

    args = parser.parse_args()

    evidence = convert_reviews_to_evidence(args.input, args.output)

    print(f"Converted {len(evidence)} critical reviews into CUSTOMER EVIDENCE.")
    print(f"Output: {args.output}")
