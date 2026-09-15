import pytest

from core.mechanism_contract import (
    FieldSpec,
    MechanismContract,
    require_valid,
    validate_inputs,
    validate_output,
)


CONTRACT = MechanismContract(
    mechanism="browseract-amazon-reviews-api",
    input_fields=(
        FieldSpec("Marketplace URL"),
        FieldSpec("ASIN"),
        FieldSpec("Review Count"),
    ),
    output_required_keys=("results",),
    output_item_required_keys=("asin", "review_text", "star_rating"),
)


def test_input_contract_blocks_missing_field():
    check = validate_inputs(CONTRACT, {"Marketplace URL": "https://www.amazon.es", "ASIN": "B0X"})
    assert not check.ok
    assert "Review Count" in " ".join(check.errors)


def test_input_contract_accepts_declared_inputs():
    check = validate_inputs(
        CONTRACT,
        {
            "Marketplace URL": "https://www.amazon.es",
            "ASIN": "B0X",
            "Review Count": "10",
        },
    )
    assert check.ok


def test_output_contract_blocks_schema_drift():
    check = validate_output(CONTRACT, {"results": [{"asin": "B0X"}]})
    assert not check.ok
    assert "review_text" in " ".join(check.errors)


def test_require_valid_raises_on_failed_contract():
    with pytest.raises(ValueError, match="INPUT contract failed"):
        require_valid(validate_inputs(CONTRACT, {}))
