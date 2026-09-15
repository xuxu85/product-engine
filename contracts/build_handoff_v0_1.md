# BUILD v0.1 HANDOFF CONTRACT

## Objective

Prove that a Product Thesis can move through ready mechanisms without re-entering the same business facts manually.

## Input

Required:
- product thesis ID
- category
- target market
- target consumer / job-to-be-done
- positioning
- product constraints
- target economics, when known
- evidence/provenance references

For the current test case:
- category: water + electrolytes / electrolyte water
- market: to be explicitly supplied by the test run

## Output package

The BUILD lane must produce or explicitly mark unavailable:

1. `concept.json` — selected concept and rationale
2. `formula.json` — ingredients, quantities, units, constraints, formulation status
3. `bom.yaml` — ingredients/materials, quantities, supplier fields, cost fields
4. `spec.md` — product requirements and target user/use case
5. `compliance.yaml` — applicable requirements and evidence status
6. `economics.json` — COGS assumptions, target price, margin assumptions
7. `rfq_brief.md` — supplier/co-packer brief, MOQ, packaging, process and questions
8. `gate.json` — PASS / FAIL / PIVOT plus blockers and evidence

## Provenance

Every externally sourced quantitative value must retain:

`source + date/period + marketplace/region + method + verification status`

Generated assumptions must be labeled as assumptions and cannot be promoted to verified evidence without validation.

## Handoff rules

- Concept output must be sufficient to start formulation.
- Formula output must be sufficient to draft the BOM.
- Spec/BOM must be sufficient to identify compliance and economics work.
- Compliance/economics must be sufficient to prepare an RFQ brief.
- Missing supplier/co-packer capability is a GAP, not a fabricated result.

## Gate

`PASS` only when the package is internally consistent and every required field is either populated with provenance or explicitly marked `UNKNOWN / BLOCKED` with a concrete next action.
