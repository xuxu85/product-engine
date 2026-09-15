# BUILD v0.1 MECHANISM CONTRACT

## Purpose

Provide one stable execution contract between the Product Engine pipeline and external/ready BUILD mechanisms.

The Product Engine owns orchestration, gates, provenance and decisions. A mechanism owns the domain work it is selected to perform.

## Input

A BUILD request contains:

- `product_thesis`
- `product_spec` when already available
- `market`
- `consumer`
- `positioning`
- `constraints`
- `target_economics` when known
- `evidence`
- `mechanism_id`

No mechanism may silently invent missing business facts. Missing inputs must be returned as `UNKNOWN` or `BLOCKED`.

## Mechanism interface

Each mechanism must expose:

- `id`
- `version`
- `capabilities`
- `required_inputs`
- `run(input)`
- `validate(output)`

## Current registry

### `aws-food-concepts`
Role: food/beverage concept, recipe, BOM and related product-development generation.
Status: `CANDIDATE`

### `openmix`
Role: formulation, constraints, validation and optimization.
Status: `CANDIDATE`

### `forkable-factory`
Role: execution-repository/stage-gate structure reference.
Status: `REFERENCE`

No candidate is production-approved until the BUILD handoff test passes.

## Output

The mechanism must return a machine-readable BUILD result containing:

- `concept`
- `formula`
- `bom`
- `spec`
- `compliance`
- `economics`
- `rfq_brief`
- `gate`
- `evidence`
- `invalidation_conditions`
- `unknowns`
- `blockers`

Each field may be populated, `UNKNOWN`, or `BLOCKED` with an explicit reason and next action.

## Enforcement

- No fabricated supplier, regulatory, cost or market facts.
- Quantitative external facts require source, date/period, region/marketplace, method and verification status.
- Generated assumptions must remain labeled as assumptions.
- A missing capability is a GAP, not a guessed result.
- BUILD cannot advance a gate without the required evidence.

## Gate

`PASS`: output package is internally consistent and all required fields are verified or explicitly resolved.

`FAIL`: a required condition cannot be satisfied.

`PIVOT`: evidence requires changing the product thesis/specification.

Every non-terminal result must include at least one measurable invalidation condition.
