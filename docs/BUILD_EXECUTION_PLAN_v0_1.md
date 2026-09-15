# BUILD v0.1 EXECUTION PLAN

## Objective

Turn an approved Product Thesis into a supplier/pilot-ready product package using ready mechanisms and the existing Product Engine state machine.

## Execution chain

`PRODUCT_THESIS → PRODUCT_SPEC → CONCEPT → FORMULA → BOM → COMPLIANCE → ECONOMICS → RFQ → PILOT`

The existing router remains authoritative for stage transitions. BUILD mechanisms do not own pipeline routing.

## Mechanism assignment

1. `aws-food-concepts` — concept / recipe / BOM generation where available.
2. `openmix` — formulation validation/optimization where its inputs and outputs match the contract.
3. `forkable-factory` — reference for execution artifact structure and stage gates; not treated as a beverage supplier integration.

## Minimal adapter rule

Build only an adapter required to translate an existing mechanism into `build_mechanism_v0_1`.

Do not build:

- a second orchestrator;
- a second state machine;
- a replacement formulation engine;
- a replacement product intelligence engine;
- a supplier database before the RFQ gate requires it.

## Test case

Current product territory: `water + electrolytes / electrolyte water`.

The first integration test must use one concrete approved thesis and produce the complete BUILD output package without manually re-entering the same business facts between mechanisms.

## Stop conditions requiring user decision

Execution stops and asks the user only when one of these is reached:

1. paid service / subscription purchase;
2. external credential or API authorization that cannot be supplied automatically;
3. irreversible external supplier/manufacturing commitment;
4. business PASS / FAIL / PIVOT decision requiring owner approval;
5. a mechanism conflict that cannot be resolved by the existing contracts without changing a closed decision.

Everything else should be implemented and tested automatically.

## Success criterion

BUILD v0.1 passes when one thesis produces a consistent machine-readable package with provenance and explicit unknowns/blockers, and the package can be handed to the next pipeline stage without manual reconstruction.
