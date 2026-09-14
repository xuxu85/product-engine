# Product Engine

Minimal orchestration and decision layer for building and selling a consumer product.

## Goal

Find a commercially viable product → validate demand → prototype → pilot → first real sale → repeat purchase → scale.

**Primary metric:** TIME → FIRST REAL SALE

This repository is intentionally **not** a Product Intelligence Engine. It does not try to become an Amazon database, review platform, scraper, or sourcing marketplace.

## Architecture

```text
EXISTING DATA / TOOLS
  ├─ Amazon
  ├─ Helium 10 / MCP
  ├─ Reddit
  ├─ Google Trends
  └─ existing research workflows
          ↓
    AGENT / ADAPTER LAYER
          ↓
    PRODUCT ENGINE CORE
      ├─ contracts
      ├─ state machine
      ├─ decision gates
      └─ router
          ↓
    DECISION / EXECUTION
      ├─ Product Spec
      ├─ validation
      ├─ sourcing / RFQ
      ├─ economics
      ├─ prototype
      ├─ pilot
      └─ sales
```

## Core rule

Every gate returns exactly one of:

- `PASS`
- `FAIL`
- `PIVOT`

Every important thesis carries an explicit invalidation condition.

## Capital rule

No meaningful capital is committed before evidence of willingness to pay. Cheap validation is allowed; large inventory, production, marketing, or infrastructure spend is not.

## Current scope: v0.1

The first implementation contains only the contracts and state machine required to connect future agents/tools. Concrete adapters for Amazon, H10, Reddit, sourcing, and Notion are deliberately deferred until a real bottleneck is proven.
