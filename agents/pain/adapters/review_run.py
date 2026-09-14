from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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
