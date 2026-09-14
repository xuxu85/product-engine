# Agent Pipeline Contract Matrix v0.1

Purpose: architecture gate before connecting real H10 data. All rows below are interface contracts/fixtures, not business validation.

| Gate | Worker | Required input | Output handoff | Real evidence required for business PASS |
|---|---|---|---|---|
| MARKET | finder | market candidate data | candidates | Yes |
| PAIN | pain | canonical customer evidence | pain + evidence | Yes |
| OPPORTUNITY | opportunity | opportunity card | opportunity | Yes |
| PRODUCT_THESIS | product_thesis | opportunity | product thesis | Yes |
| DEMAND_VALIDATION | demand_validation | product thesis + validation result | demand validation | Yes |
| PRODUCT_SPEC | product_spec | validated product direction | product spec | Yes |
| FORMULA | formula | product spec | formula/prototype requirements | Yes |
| ECONOMICS | economics | product + cost inputs | unit economics | Yes |
| MANUFACTURING | manufacturing | product spec + economics | supplier/manufacturing plan | Yes |
| PILOT | pilot | manufacturing plan | pilot result | Yes |
| SALES | sales | pilot-ready product | sales result | Yes |
| REPEAT | repeat | customer/sales results | repeat-purchase result | Yes |
| SCALE | pipeline gate | repeat result | terminal scale state | Yes |

## Rules

1. The pipeline state machine remains authoritative for transitions.
2. Agents return `AgentResult`; agents never authorize capital or override gate policy.
3. Missing required input must produce `ERROR`/`FAIL`, not a fabricated PASS.
4. Every result must contain at least one testable invalidation condition.
5. Synthetic fixtures prove only interface/routing integrity.
6. H10 is an external data adapter. It must be replaceable without changing the pipeline core.
7. No production, inventory, advertising, or other material capital is implied by a synthetic PASS.

## Pre-H10 gate

`PRE-H10 INFRASTRUCTURE PASS` requires:

- MARKET → PAIN → OPPORTUNITY → PRODUCT THESIS → DEMAND VALIDATION → PRODUCT SPEC → FORMULA → ECONOMICS → MANUFACTURING → PILOT → SALES → REPEAT routing to work with fixtures;
- invalid transitions rejected by the Router;
- missing inputs rejected by workers;
- real-data adapters isolated from pipeline state and gate logic.

Only after this infrastructure gate should H10 Diamond be evaluated as the real data-layer purchase.
