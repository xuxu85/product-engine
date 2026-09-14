# Product Engine

Minimal execution and decision layer for building and selling a consumer product.

## Goal

Find a commercially viable product → validate demand → prototype → pilot → first real sale → repeat purchase → scale.

**Primary metric:** TIME → FIRST REAL SALE

This repository is intentionally **not** a Product Intelligence Engine. It orchestrates existing research/data mechanisms and the business pipeline; it does not become an Amazon database, review platform, scraper, or sourcing marketplace.

## Operating architecture

```text
                    USER / CEO
                       │
                business decisions
                       │
                       ▼
            PROJECT MANAGER / ORCHESTRATOR
            ├─ reads current pipeline state
            ├─ identifies the bottleneck
            ├─ selects the execution lane
            ├─ enforces gate + evidence policy
            ├─ checks ready mechanisms first
            ├─ blocks unsupported quantitative work
            ├─ routes PASS → next gate
            ├─ records dependencies / capital
            └─ returns ONE CLEAR NEXT ACTION
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       FINDER       BUILDER       SELLER
       market       spec/formula  launch/sales
       pain/gap     prototype     feedback/repeat
       thesis       economics     scale
          │            │            │
          └────────────┼────────────┘
                       ▼
             EXISTING TOOLS / SKILLS
        Amazon · H10/MCP · Reddit · Trends
        review workflows · RFQ · sourcing
                       │
                       ▼
               PIPELINE CORE
        contracts · state · gates · router

                 NOTION = CONTROL PLANE
                 GITHUB = CODE / VERSION
                 LOCAL = EXECUTION
```

The user does not need to become a permanent researcher or engineer. The Project Manager determines what work is required; agents/workflows execute it; the pipeline decides whether the gate passes.

## Pipeline

```text
IDEA → MARKET → PAIN → OPPORTUNITY → PRODUCT_THESIS
→ DEMAND_VALIDATION → PRODUCT_SPEC → FORMULA → ECONOMICS
→ MANUFACTURING → PILOT → SALES → REPEAT → SCALE
```

Every gate returns exactly one of:

- `PASS`
- `FAIL`
- `PIVOT`

Every important thesis carries an explicit invalidation condition.

## System rules

1. **Real evidence before business PASS.** Synthetic fixtures prove interfaces/routing only.
2. **Ready mechanism first.** Reuse an existing tool, repository, skill, workflow, API, or MCP before building custom functionality.
3. **Provider-neutral core.** H10 is a data adapter, not the pipeline itself. Missing H10 must block only H10-dependent work, not unrelated work that can proceed with verified alternatives.
4. **No fabricated data.** Quantitative claims require source, period, marketplace, method, and verification.
5. **Capital is controlled at the decision layer.** Agents may estimate cost but never authorize material spend.
6. **No automatic stage skipping.** The Router is authoritative for transitions.
7. **One bottleneck at a time.** Research continues only when it closes the current decision gate.

## Current implementation

The repository already contains:

- deterministic pipeline state and gate routing;
- agent contracts and invalidation conditions;
- PAIN workflow and review-evidence adapter;
- stage workers for downstream gates;
- H10 adapter boundary;
- tests and CI workflow;
- progress model.

The next control-layer addition is the Project Manager / Orchestrator. It should remain thin: planning, routing, enforcement, and dependency control—not a replacement for existing research tools.

## Progress

Progress measures validated business progress, not code volume.

`[████░░░░░░░░░░░░░░░░] 20%`

Current bottleneck: **REAL CONSUMER PAIN / OPPORTUNITY EVIDENCE**.
