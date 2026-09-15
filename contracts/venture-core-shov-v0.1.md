# Product Engine ↔ Product Venture Core — SHOV Contract v0.1

## Purpose
A minimal, versioned boundary between the business orchestration layer (`product-engine`) and the reusable execution core (`product-venture-core`). Repositories remain independent.

## Ownership
- `product-engine`: business state, gate decisions, bottleneck, capital controls, routing, ONE CLEAR NEXT ACTION.
- `product-venture-core`: reusable execution contracts, stage interfaces, workers/adapters and technical execution.
- External providers/tools: evidence acquisition; neither repository becomes a replacement for them.

## Transport contract
### Engine → Core
Canonical `AgentRequest`:
- `stage`: target execution stage (`PAIN`, `FINDER`, `BUILDER`, `SELLER`, etc.)
- `input`: structured stage input
- `constraints`: execution constraints
- `evidence`: verified evidence objects where applicable
- `task_id`: stable task identifier
- `agent_id`: selected execution agent
- `agent_version`: version of the execution interface

For PAIN, the core currently normalizes `evidence[]` into `AgentRequest(stage=PAIN, input={evidence: evidence})`.

### Core → Engine
Canonical `AgentResult` (or equivalent versioned result contract) must return:
- task_id
- stage
- status / execution outcome
- structured output
- evidence references
- errors / blockers
- mechanism and version metadata

## Business interpretation
`product-engine` is the only authority for PASS / FAIL / PIVOT and stage transition. Core execution success is not automatically a business PASS.

## Evidence rule
Synthetic fixtures may prove interfaces/routing only. Business PASS requires real, verified evidence with source, period, marketplace, method and verification where quantitative claims are involved.

## Change rule
Breaking contract changes require a version increment and contract-test update. Non-breaking implementation changes remain inside the owning repository.

## Current PAIN seam
```text
Amazon / BrowserAct / other verified acquisition
        ↓
 evidence[]
        ↓
 product-engine
        ↓
 SHOV / AgentRequest
        ↓
 product-venture-core / PAIN
        ↓
 AgentResult / pain evidence
        ↓
 product-engine gate
        ↓
 PASS / FAIL / PIVOT
```

## Non-goals
- No repository merge.
- No shared database.
- No second state machine.
- No n8n/Cloudflare dependency merely for transport.
- No duplication of Amazon/review research mechanisms.
