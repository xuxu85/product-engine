# BUILD READY MECHANISMS — v0.1

## Purpose

BUILD must reuse ready mechanisms before custom implementation. This document records the current candidates for the physical-product execution lane. Candidates remain `NOT_VERIFIED` until the same Product Thesis can pass through their handoff contracts.

## Candidate stack

| Layer | Mechanism | Repository | Role | State |
|---|---|---|---|---|
| Concept | AWS Food Concepts | `aws-solutions-library-samples/guidance-for-generating-food-concepts-using-amazon-bedrock` | concept, recipe, BOM/cost, packaging, nutrition, pricing, export | NOT_VERIFIED |
| Formulation | OpenMix | `vijayvkrishnan/openmix` | formulation, constraints, validation, optimization | NOT_VERIFIED |
| Execution workspace | Forkable Factory Starter | `forkable-factory/starter` | spec, BOM, compliance, stage gates, agent tasks | NOT_VERIFIED |

## Target handoff

```text
PRODUCT THESIS
  -> CONCEPT
  -> FORMULATION
  -> PRODUCT SPEC
  -> BOM
  -> COMPLIANCE
  -> ECONOMICS
  -> RFQ / CO-PACKER
  -> PILOT
```

## Contract gate

A candidate cannot become `ADOPTED` from documentation alone. The test must prove:

1. input can be represented without manual re-entry of business facts;
2. output is machine-readable and preserves provenance;
3. output contains the fields required by the next stage;
4. failures are explicit and do not create a false PASS;
5. no paid or side-effecting action starts before preflight;
6. a beverage/electrolyte-water case can traverse the handoff.

## Decision states

- `NOT_VERIFIED` — repository inspected, runtime handoff not proven.
- `PASS` — contract and real execution handoff verified.
- `ADAPT` — mechanism is suitable but a minimal adapter is required.
- `REJECT` — mechanism cannot satisfy the gate without becoming a replacement system.

## Current rule

Do not search for more BUILD repositories unless all current candidates are rejected or a concrete capability gap is demonstrated.
