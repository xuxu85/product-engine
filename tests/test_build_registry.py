from build.registry import BuildMechanism, BuildMechanismRegistry


def test_registry_returns_blocked_for_missing_inputs() -> None:
    mechanism = BuildMechanism(
        id="aws-food-concepts",
        version="candidate",
        capabilities=("concept", "recipe", "bom"),
        required_inputs=("product_thesis", "market"),
        runner=lambda payload: {"gate": "PASS", "concept": payload["product_thesis"]},
    )
    result = mechanism.run({"product_thesis": "electrolyte water"})
    assert result["gate"] == "BLOCKED"
    assert result["unknowns"] == ["market"]


def test_registry_selects_registered_mechanism() -> None:
    mechanism = BuildMechanism(
        id="openmix",
        version="candidate",
        capabilities=("formulation", "validation", "optimization"),
        required_inputs=("product_thesis",),
        runner=lambda payload: {"gate": "PASS"},
    )
    registry = BuildMechanismRegistry([mechanism])
    assert registry.get("openmix").id == "openmix"
