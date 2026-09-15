from build.registry import BuildMechanism, BuildMechanismRegistry
from build.runner import run_build


def test_product_spec_build_formula_handoff() -> None:
    product_spec = {
        "product_thesis": "electrolyte water",
        "market": "US",
        "format": "water",
    }

    mechanism = BuildMechanism(
        id="test-formulation",
        version="0.1",
        capabilities=("formulation", "validation"),
        required_inputs=("product_thesis", "market"),
        runner=lambda payload: {
            "gate": "PASS",
            "formula": {"format": payload["format"]},
            "next_stage": "FORMULA",
        },
    )
    registry = BuildMechanismRegistry([mechanism])

    result = run_build(registry, "test-formulation", product_spec)

    assert result["status"] == "COMPLETED"
    assert result["output"]["gate"] == "PASS"
    assert result["output"]["next_stage"] == "FORMULA"
