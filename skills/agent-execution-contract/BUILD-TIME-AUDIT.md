# BUILD-TIME EXECUTION AUDIT
## Mandatory Feature of Agent Execution Contract v1.0

This audit prevents agents from building downstream components against assumed or merely documented capabilities.

## REQUIRED BEFORE BUILD

Before creating or modifying any workflow, skill, adapter, schema, registry entry, or agent, audit the complete intended corridor:

INPUT → EXECUTOR → OUTPUT → JUDGE → PERSISTENCE → NEXT NODE

For every seam record:

- EXISTS?
- EXECUTABLE?
- VERIFIED?
- SCHEMA-COMPATIBLE?
- PERSISTED?
- CONSUMABLE?

## HARD STOP RULE

If an upstream executor or output is only documented, registered, or exposed as an interface, but has not been execution-verified:

STOP downstream implementation.

Allowed action: verification run or minimal repair only.

## REGISTRY SAFETY

A registry is discovery/routing metadata, not proof of capability.

Never promote a mechanism to ready/verified because:
- a repository exists;
- a README claims capability;
- an interface/schema exists;
- a registry entry exists;
- a prompt says it can do the task.

Verification requires execution evidence.

## LIFECYCLE

FOUND → EXECUTABLE → OUTPUT_VERIFIED → JUDGE_VERIFIED → END_TO_END_VERIFIED

If verification evidence is absent, status remains UNVERIFIED.

`AVAILABLE` must not mean verified.

## COMPLETION

Code existing is not completion.

Completion requires, as applicable:

IMPLEMENTED → TESTED → REAL INPUT VERIFIED → OUTPUT VERIFIED → JUDGE VERIFIED → PERSISTENCE VERIFIED → DOWNSTREAM CONSUMPTION VERIFIED

## REQUIRED BUILD RECORD

Before declaring a component complete, record:

COMPONENT:
CURRENT GATE:
UPSTREAM INPUT:
EXECUTOR:
EXPECTED OUTPUT:
ACTUAL OUTPUT:
JUDGE:
PERSISTENCE:
DOWNSTREAM CONSUMER:
VERIFICATION EVIDENCE:
STATUS:

If evidence is missing:

STATUS = IMPLEMENTED-NOT-VERIFIED

## EXAMPLE

Wrong:

Pain interface exists → build Pain → Trend.

Correct:

Pain interface exists → inspect executor → execute with real input → verify PainCard[] → verify Judge → persist → verify Trend can consume it → only then build/activate downstream seam.
